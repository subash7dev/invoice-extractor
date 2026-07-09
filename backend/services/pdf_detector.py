import fitz


class PDFDetector:
    """
    Detects whether a PDF is:

    - Digital
    - Scanned
    - Hybrid
    """

    @staticmethod
    def analyze(pdf_path: str) -> dict:

        document = fitz.open(pdf_path)

        total_pages = len(document)

        digital_pages = 0
        scanned_pages = 0

        page_info = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text().strip()

            if len(text) > 20:

                page_type = "digital"
                digital_pages += 1

            else:

                page_type = "scanned"
                scanned_pages += 1

            page_info.append({

                "page": page_number,

                "type": page_type,

                "characters": len(text)

            })

        document.close()

        if digital_pages == total_pages:

            pdf_type = "digital"

        elif scanned_pages == total_pages:

            pdf_type = "scanned"

        else:

            pdf_type = "hybrid"

        return {

            "pdf_type": pdf_type,

            "total_pages": total_pages,

            "digital_pages": digital_pages,

            "scanned_pages": scanned_pages,

            "pages": page_info
        }

    @staticmethod
    def is_digital(pdf_path: str) -> bool:

        return PDFDetector.analyze(pdf_path)["pdf_type"] == "digital"

    @staticmethod
    def is_scanned(pdf_path: str) -> bool:

        return PDFDetector.analyze(pdf_path)["pdf_type"] == "scanned"

    @staticmethod
    def is_hybrid(pdf_path: str) -> bool:

        return PDFDetector.analyze(pdf_path)["pdf_type"] == "hybrid"