from pathlib import Path
from typing import List

import fitz


class PDFToImage:
    """
    Converts PDF pages into high-resolution PNG images.
    """

    DEFAULT_DPI = 300

    @classmethod
    def convert(
        cls,
        pdf_path: str,
        output_dir: str
    ) -> List[str]:

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        document = fitz.open(pdf_path)

        image_paths = []

        zoom = cls.DEFAULT_DPI / 72

        matrix = fitz.Matrix(zoom, zoom)

        for page_number, page in enumerate(document, start=1):

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_file = output_path / f"page_{page_number}.png"

            pixmap.save(str(image_file))

            image_paths.append(str(image_file))

        document.close()

        return image_paths

    @classmethod
    def convert_page(
        cls,
        pdf_path: str,
        page_number: int,
        output_dir: str
    ) -> str:

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        document = fitz.open(pdf_path)

        if page_number < 1 or page_number > len(document):
            raise ValueError("Invalid page number.")

        zoom = cls.DEFAULT_DPI / 72

        matrix = fitz.Matrix(zoom, zoom)

        page = document.load_page(page_number - 1)

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        image_file = output_path / f"page_{page_number}.png"

        pixmap.save(str(image_file))

        document.close()

        return str(image_file)

    @classmethod
    def page_count(cls, pdf_path: str) -> int:

        document = fitz.open(pdf_path)

        count = len(document)

        document.close()

        return count