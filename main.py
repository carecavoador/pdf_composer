from pathlib import Path
from decimal import Decimal

from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation
from PyPDF2.generic import RectangleObject


# 72 pontos por polegada (resolução padrão de um arquivo .PDF)
pol = Decimal(72)
# 1 pol == 25.4 mm
mm = pol / Decimal(25.4)

LARGURA_ROLO = 2592


def sort_paginas(pagina: PageObject) -> Decimal:
    """Retorna a altura da página"""
    return pagina.mediabox.height


lista_pdfs = Path("pdfs_exemplo").iterdir()

paginas = [PdfReader(pdf).pages[0] for pdf in lista_pdfs]

# Ordena a lista de págidas da maior para a menor.
paginas_sorted = sorted(paginas, key=sort_paginas, reverse=True)

nova_pagina = PageObject().create_blank_page(None, LARGURA_ROLO, paginas_sorted[0].mediabox.height)

largura_anterior = 0

for idx, pagina in enumerate(paginas_sorted):
    if idx > 0:
        largura_anterior += float(paginas_sorted[idx - 1].mediabox.width)
        op = Transformation().translate(tx=largura_anterior, ty=0)
        pagina.add_transformation(op)
        
        pagina.update({'/MediaBox': RectangleObject([largura_anterior, 0, pagina.mediabox.width, pagina.mediabox.height])})
        pagina.update({'/TrimBox': RectangleObject([largura_anterior, 0, pagina.mediabox.width, pagina.mediabox.height])})
        
        nova_pagina.merge_page(pagina)
    else:
        nova_pagina.merge_page(pagina)

writer = PdfWriter()
writer.add_page(nova_pagina)

with open("novo.pdf", "wb") as novo:
    writer.write(novo)
