import sys

from pathlib import Path
from decimal import Decimal
from copy import copy

from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation


# 72 pontos por polegada (resolução padrão de um arquivo .PDF)
# 1 pol == 25.4 mm
POL = Decimal(72)
MM = POL / Decimal(25.4)
ALTURA_MAX = 1200 * MM
LARGURA_ROLO = 2592
MARGEM = float(20 * MM)


def sort_paginas(_pagina: PageObject) -> Decimal:
    """Retorna a altura da página"""
    return _pagina.mediabox.height


def atualiza_boxes(
    _pagina: PageObject, novo_retangulo: tuple[float, float, float, float]
) -> PageObject:
    """Atualiza todos os boxes de uma página com o retângulo informado."""
    _pagina.update({"/MediaBox": novo_retangulo})
    _pagina.update({"/TrimBox": novo_retangulo})
    _pagina.update({"/TrimBox": novo_retangulo})
    _pagina.update({"/ArtBox": novo_retangulo})
    _pagina.update({"/BleedBox": novo_retangulo})
    _pagina.update({"/CropBox": novo_retangulo})
    return _pagina


def orienta_pagina(_pagina: PageObject, vertical: bool = True) -> PageObject:
    """Gira a página para o sentido vertical, caso ela esteja na horizontal."""
    largura, altura = float(_pagina.mediabox.width), float(_pagina.mediabox.height)
    if not vertical:
        largura, altura = altura, largura
    if largura > altura:
        pagina_rotacionada = PageObject().create_blank_page(None, altura, largura)
        _pagina.add_transformation(
            Transformation()
            .translate(
                -largura / 2,
                -altura / 2,
            )
            .rotate(90)
            .translate(
                altura / 2,
                largura / 2,
            )
        )
        _pagina = atualiza_boxes(_pagina, (0, 0, altura, largura))
        pagina_rotacionada.merge_page(_pagina)
        return pagina_rotacionada
    return _pagina


def distribuir(lista_paginas: list[PageObject], largura_rolo: float) -> None:
    """Distribui uma lista de páginas em um rolo."""

    # Orienta as páginas na vertical
    lista_paginas = [orienta_pagina(pagina) for pagina in lista_paginas]

    # Ordena da página mais alta para a mais baixa
    paginas_ordenadas = sorted(lista_paginas, key=sort_paginas, reverse=True)

    numero_de_pagina = 1

    while paginas_ordenadas:
        maior_altura = paginas_ordenadas[0].mediabox.height
        altura_rolo = float(min(ALTURA_MAX, maior_altura)) + MARGEM
        nova_pagina = PageObject().create_blank_page(None, largura_rolo, altura_rolo)
        pos_x = MARGEM / 2

        for pagina in copy(paginas_ordenadas):
            largura_pagina = float(pagina.mediabox.width)
            altura_pagina = float(pagina.mediabox.height)
            pos_y = (altura_rolo - altura_pagina) / 2

            # TODO: implementar caso a página seja maior que o rolo

            # Página não cabe na montagem
            if (pos_x + largura_pagina + (MARGEM / 2)) > largura_rolo:
                break

            # Página cabe na montagem
            pagina.add_transformation(Transformation().translate(tx=pos_x, ty=pos_y))
            pagina = atualiza_boxes(
                pagina,
                (pos_x, pos_y, pos_x + largura_pagina, pos_y + altura_pagina),
            )
            nova_pagina.merge_page(pagina, expand=True)
            pos_x += largura_pagina + MARGEM
            paginas_ordenadas.remove(pagina)

        writer = PdfWriter()
        writer.add_page(nova_pagina)
        with open(f"montagem_rolo_{numero_de_pagina}.pdf", "wb") as f:
            writer.write(f)
        numero_de_pagina += 1


def main():
    """Início do programa."""
    argumentos = sys.argv[1:]
    # lista_pdfs = Path("pdfs_exemplo").iterdir()
    if argumentos:
        lista_pdfs = [
            Path(pdf) for pdf in argumentos if Path(pdf).suffix.lower() == ".pdf"
        ]
        lista_paginas = [PdfReader(pdf).pages[0] for pdf in lista_pdfs]
        lista_paginas = [orienta_pagina(pagina) for pagina in lista_paginas]
    else:
        sys.exit()

    dir_saida = lista_pdfs[0].parent

    # Ordena a lista de págidas da maior para a menor.
    paginas_ordenadas = sorted(lista_paginas, key=sort_paginas, reverse=True)

    num_paginas = 0

    while len(paginas_ordenadas) > 0:
        # Cria uma nova página com a largura do rolo e a altura da maior página.
        altura = min(ALTURA_MAX, paginas_ordenadas[0].mediabox.height)
        nova_pagina = PageObject().create_blank_page(
            None, float(LARGURA_ROLO), float(altura)
        )

        largura_total = 0.0

        for idx, pagina in enumerate(copy(paginas_ordenadas)):
            largura_pagina, altura_pagina = float(pagina.mediabox.width), float(
                pagina.mediabox.height
            )
            if (largura_total + largura_pagina + MARGEM) > LARGURA_ROLO:
                continue
            if idx == 0:
                # Se for a primeira página, não aplica nenhuma transformação.
                # Somente mescla na coordenada 0, 0.
                nova_pagina.merge_page(pagina, expand=True)
            else:
                # Aplica a transformação para as páginas subsequentes (se houver).
                pagina.add_transformation(
                    Transformation().translate(tx=largura_total, ty=0)
                )
                pagina = atualiza_boxes(
                    pagina,
                    (largura_total, 0, largura_total + largura_pagina, altura_pagina),
                )
                nova_pagina.merge_page(pagina, expand=True)
            largura_total += largura_pagina + MARGEM
            paginas_ordenadas.remove(pagina)

        writer = PdfWriter()
        writer.add_page(nova_pagina)
        num_paginas += 1
        with open(dir_saida.joinpath(f"pg_rolo_{num_paginas}.pdf"), "wb") as novo:
            writer.write(novo)


if __name__ == "__main__":
    main()
