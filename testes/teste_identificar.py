import sys

sys.path.insert(0, "..")

from PyPDF2 import PdfReader, PdfWriter

from ..identificador import identificar_layout_externo


pdf = PdfReader(r"C:\Users\Everton Souza\python\composer\pdfs_exemplo\menor.pdf")
pagina = pdf.pages[0]

nova_pagina = identificar_layout_externo(
    pagina=pagina, identificador="123456 v12 Teste"
)

writer = PdfWriter()
writer.add_page(nova_pagina)
with open("teste_identificar.pdf", "wb") as f:
    writer.write(f)
