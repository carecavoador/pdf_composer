from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation


MAX_WIDTH = 2592  # max page width (36 inches * 72 dpi = 2592 dots).
MIN_HEIGHT = 792  # minimum page height (11 inches * 72 dpi = 792 dots).
MARGIN = 72  # 1 inch (72 points) spacing between different items.

SAMPLE_FILES = [Path("files/A3.pdf"), Path("files/A4.pdf"), Path("files/other.pdf")]


def sort_height(pdf_file: Path) -> int:
    """Returns mediabox height to sort files by height."""
    _reader = PdfReader(open(pdf_file, "rb"))
    return _reader.pages[0].mediabox.height


def main() -> None:

    # Sort files from tallest to shortest.
    sorted_files = sorted(SAMPLE_FILES, key=sort_height, reverse=True)

    # New file name where all the files will be merged.
    merged_files = Path("files/merged.pdf")

    with open(merged_files, "wb") as new_file:
        new_page = PageObject.create_blank_page(None, MAX_WIDTH, MIN_HEIGHT)

        # Last X position to use in horizontal axis translation.
        last_x = 0

        for file in sorted_files:
            reader = PdfReader(open(file, "rb"))
            page_to_merge = reader.pages[0]

            # This works:
            # new_page.mergeTranslatedPage(page_to_merge, tx=last_x, ty=0, expand=True)

            # This does not work:
            op = Transformation().translate(tx=last_x, ty=0)
            page_to_merge.add_transformation(op)
            new_page.merge_page(page_to_merge, expand=True)

            last_x += page_to_merge.mediabox.width + MARGIN

        writer = PdfWriter()
        writer.add_page(new_page)
        writer.write(new_file)


if __name__ == "__main__":
    main()
