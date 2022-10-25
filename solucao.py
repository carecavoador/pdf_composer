from PyPDF2 import PdfReader, Transformation, PdfWriter
from PyPDF2.generic import RectangleObject

a3_file = PdfReader('A3.pdf')
a3_page = a3_file.pages[0]

a4_file = PdfReader('A4.pdf')
a4_page = a4_file.pages[0]

# Rotate 'a4_page.pdf' 90 degrees and centers it on 'a3_page.pdf':
a4_page.add_transformation(
    Transformation()
    .translate(-float(a4_page.mediaBox.getWidth()) / 2, -float(a4_page.mediaBox.getHeight()) / 2)
    .rotate(90)
    .translate(float(a4_page.mediaBox.getHeight()) / 2, float(a3_page.mediaBox.getLowerLeft_y() + a4_page.mediaBox.getWidth() / 2))
)

# Manually update page boxes:
new_width = a4_page.mediaBox.getHeight()
new_heigth = a4_page.mediaBox.getWidth()
new_y = a3_page.mediaBox.getLowerLeft_y()

a4_page.update({'/MediaBox': RectangleObject([0, new_y, new_width, new_y + new_heigth])})
a4_page.update({'/TrimBox': RectangleObject([0, new_y, new_width, new_y + new_heigth])})
a4_page.update({'/ArtBox': RectangleObject([0, new_y, new_width, new_y + new_heigth])})
a4_page.update({'/BleedBox': RectangleObject([0, new_y, new_width, new_y + new_heigth])})
a4_page.update({'/CropBox': RectangleObject([0, new_y, new_width, new_y + new_heigth])})

a3_page.merge_page(a4_page)

writer = PdfWriter()
writer.add_page(a3_page)
with open('merged_a3.pdf', 'wb') as fo:
    writer.write(fo)