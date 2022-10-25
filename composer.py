from pathlib import Path
from decimal import Decimal

from PyPDF2 import PdfReader, PdfWriter, PageObject

POL = 72
CM = Decimal(POL / 2.54)
MARGEM = 2 * CM
ROLO = 90 * CM
ALTURA_MIN = 30 * CM

arquivos = [Path("arquivos/A3.pdf"), Path("arquivos/A4.pdf"), Path("arquivos/T.pdf")]


def altura(_arquivo: Path) -> int:
    """Retorna a altura do mediabox."""
    if _arquivo.suffix.lower() == ".pdf":
        _reader = PdfReader(open(_arquivo, "rb"))
        _pagina = _reader.pages[0]
        return _pagina.mediabox.height
    else:
        return 0


arquivos.sort(reverse=True, key=altura)


with open("arquivos/composto.pdf", "wb") as pdf:
    nova_pagina = PageObject.create_blank_page(None, ROLO, ALTURA_MIN)
    largura_total = Decimal()

    for arquivo in arquivos:
        reader = PdfReader(open(arquivo, "rb"))
        pagina = reader.pages[0]
        mb = pagina.mediabox

        # O primeiro arquivo não precisa de Translate, vai na posição 0,0.
        if arquivos.index(arquivo) == 0:
            nova_pagina.merge_page(pagina, expand=True)
        else:
            # op = Transformation().translate(tx=largura_total, ty=0)
            # pagina.add_transformation(op)
            # nova_pagina.merge_page(pagina, expand=True)
            nova_pagina.mergeTranslatedPage(pagina, tx=largura_total, ty=0, expand=True)

        largura_total += pagina.mediabox.width + MARGEM

    gravador = PdfWriter()
    gravador.add_page(nova_pagina)
    gravador.write(pdf)
