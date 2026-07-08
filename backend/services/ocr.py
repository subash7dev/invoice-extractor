from paddleocr import PaddleOCR

# Initialize OCR once
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)


def extract_text(image_path: str) -> str:
    """
    Extract text from an image using PaddleOCR 2.8.1
    """
    result = ocr.ocr(image_path, cls=True)

    extracted_text = []

    if result:
        for line in result[0]:
            extracted_text.append(line[1][0])

    return "\n".join(extracted_text)