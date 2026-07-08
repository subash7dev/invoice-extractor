import fitz
from pathlib import Path

def pdf_to_images(pdf_path: str, output_dir="uploads"):
    doc = fitz.open(pdf_path)

    images = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image_path = Path(output_dir) / f"page_{i+1}.png"

        pix.save(str(image_path))

        images.append(str(image_path))

    return images