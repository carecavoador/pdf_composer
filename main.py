"""main.py"""
import sys
from pathlib import Path

from PyPDF2 import PdfReader

from distribuidor import distribuir, orienta_pagina
from identificador import identificar_layout_externo


def main():
    """Início do programa."""

    argumentos = sys.argv[1:]
    layouts: list[Path] = []

    if not argumentos:
        print("Favor especificar os itens a serem distribuidos.")
        sys.exit()
    for arg in argumentos:
        item = Path(arg)
        if not item.exists():
            continue
        if item.is_file() and item.suffix.lower() == ".pdf":
            layouts.append(item)
        else:
            layouts.extend(
                [layout for layout in item.iterdir() if layout.suffix.lower() == ".pdf"]
            )

    if layouts:
        paginas = [
            identificar_layout_externo(
                pagina=orienta_pagina(PdfReader(pdf).pages[0]), identificador=pdf.name
            )
            for pdf in layouts
        ]
        if paginas:
            distribuir(paginas=paginas)
        else:
            print("Não foi possível identificar nenhum item.")
    else:
        print("Sem itens para distribuir.")


if __name__ == "__main__":
    main()
