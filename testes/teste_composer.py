from pathlib import Path
from PyPDF2 import PdfReader
from xcomposer import distribuir, LARGURA_ROLO


def testa_composer():
    lista_pdfs = Path("pdfs_exemplo").iterdir()
    lista_paginas = [PdfReader(pdf).pages[0] for pdf in lista_pdfs]
    # lista_paginas.extend([PdfReader(pdf).pages[0] for pdf in lista_pdfs])
    distribuir(lista_paginas, LARGURA_ROLO)


if __name__ == "__main__":
    testa_composer()
