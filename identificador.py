"""identificar.py"""
from io import BytesIO

from PyPDF2 import PageObject, PdfReader
from reportlab.pdfgen import canvas


FONTE = "Helvetica"
TAMANHO_FONTE = 4
BORDA = 2


def identificar_layout_externo(pagina: PageObject, identificador: str) -> PageObject:
    """Insere a identificação fornecida na área externa da página."""

    largura, altura = pagina.mediabox.upper_right
    largura, altura = float(largura), float(altura)

    bytes_pdf = BytesIO()
    documento = canvas.Canvas(
        bytes_pdf, pagesize=(largura, altura + TAMANHO_FONTE + BORDA)
    )
    texto = documento.beginText()
    texto.setTextOrigin(0, altura + BORDA)
    texto.setFont(FONTE, TAMANHO_FONTE)
    texto.textLine(identificador)
    documento.drawText(texto)
    documento.save()
    bytes_pdf.seek(0)

    novo_pdf = PdfReader(bytes_pdf)
    novo_pdf.pages[0].merge_page(pagina)
    return novo_pdf.pages[0]
