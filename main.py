from pathlib import Path
from decimal import Decimal

from PyPDF2 import PdfReader, PdfWriter, PageObject


# 72 pontos por polegada (resolução padrão de um arquivo .PDF)
pol = Decimal(72)
# 1 pol == 25.4 mm
mm = pol / Decimal(25.4)


def sort_paginas(pagina: PageObject) -> Decimal:
    """Retorna a altura da página"""
    return pagina.mediaBox.height


lista_pdfs = list(Path("pdfs_exemplo").iterdir())

paginas = [PdfReader(pdf).pages[0] for pdf in lista_pdfs]

# Ordena a lista de págidas da maior para a menor.
paginas_sorted = sorted(paginas, key=sort_paginas, reverse=True)


