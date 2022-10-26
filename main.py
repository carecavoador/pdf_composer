from pathlib import Path
from decimal import Decimal

from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation
from PyPDF2.generic import RectangleObject


# 72 pontos por polegada (resolução padrão de um arquivo .PDF)
# 1 pol == 25.4 mm
POL = Decimal(72)
MM = POL / Decimal(25.4)
LARGURA_ROLO = 2592
ALTURA_MAX = 1200 * MM


def sort_paginas(_pagina: PageObject) -> Decimal:
    """Retorna a altura da página"""
    return _pagina.mediabox.height


def atualiza_boxes(_pagina: PageObject, novo_retangulo: RectangleObject) -> PageObject:
    """Atualiza todos os boxes de uma página com o retângulo informado."""
    _pagina.update({"/MediaBox": novo_retangulo})
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
            .translate(-largura / 2, -altura / 2,)
            .rotate(90)
            .translate(altura / 2, largura / 2,)
        )
        _pagina = atualiza_boxes(_pagina, RectangleObject([0, 0, altura, largura]))
        pagina_rotacionada.merge_page(_pagina)
        return pagina_rotacionada
    return _pagina


def main():
    """Início do programa."""
    lista_pdfs = Path("pdfs_exemplo").iterdir()
    lista_paginas = [PdfReader(pdf).pages[0] for pdf in lista_pdfs]
    lista_paginas = [orienta_pagina(pagina) for pagina in lista_paginas]

    # Ordena a lista de págidas da maior para a menor.
    paginas_ordenadas = sorted(lista_paginas, key=sort_paginas, reverse=True)

    # Cria uma nova página com a largura do rolo e a altura da maior página.
    altura = min(ALTURA_MAX, paginas_ordenadas[0].mediabox.height)
    nova_pagina = PageObject().create_blank_page(None, LARGURA_ROLO, altura)

    largura_total = 0.0

    for idx, pagina in enumerate(paginas_ordenadas):
        largura_pagina, altura_pagina = float(pagina.mediabox.width), float(pagina.mediabox.height)
        if idx == 0:
            # Se for a primeira página, não aplica nenhuma transformação. Somente mescla na coordenada 0, 0.
            nova_pagina.merge_page(pagina)
        else:
            # Aplica a transformação para as páginas subsequentes (se houver).
            pagina.add_transformation(
                Transformation()
                .translate(tx=largura_total, ty=0)
            )
            pagina = atualiza_boxes(pagina, RectangleObject([largura_total, 0, largura_total + largura_pagina, altura_pagina]))
            nova_pagina.merge_page(pagina)
        largura_total += largura_pagina

    writer = PdfWriter()
    writer.add_page(nova_pagina)

    with open("novo.pdf", "wb") as novo:
        writer.write(novo)


if __name__ == "__main__":
    main()
