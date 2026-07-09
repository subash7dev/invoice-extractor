import fitz


class PDFTextExtractor:
    """
    Production-grade digital PDF text extractor.
    """

    MIN_TEXT_LENGTH = 20

    @classmethod
    def extract(cls, pdf_path: str) -> str:

        document = fitz.open(pdf_path)

        pages = []

        for page in document:

            text = cls.extract_page(page)

            if text:
                pages.append(text)

        document.close()

        return "\n\n".join(pages)

    @classmethod
    def extract_page(cls, page) -> str:

        text = page.get_text("text")

        if len(text.strip()) < cls.MIN_TEXT_LENGTH:

            return ""

        return cls.clean(text)

    @staticmethod
    def clean(text: str) -> str:

        lines = []

        previous = None

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if line == previous:
                continue

            previous = line

            lines.append(line)

        return "\n".join(lines)

    @classmethod
    def extract_pages(cls, pdf_path: str):

        document = fitz.open(pdf_path)

        pages = []

        for index, page in enumerate(document):

            pages.append({

                "page": index + 1,

                "text": cls.extract_page(page)

            })

        document.close()

        return pages

    @classmethod
    def has_text(cls, pdf_path: str) -> bool:

        document = fitz.open(pdf_path)

        for page in document:

            if len(page.get_text().strip()) >= cls.MIN_TEXT_LENGTH:

                document.close()

                return True

        document.close()

        return False

    @classmethod
    def extract_by_page_types(cls, pdf_path: str, page_types: list) -> str:
        """
        Extract text from specific pages based on type.
        page_types: list of dicts with 'page' and 'type' keys
        """
        document = fitz.open(pdf_path)

        texts = []

        for page_info in page_types:

            page_num = page_info["page"] - 1  # 0-indexed
            page_type = page_info["type"]

            if page_type == "digital":

                page = document[page_num]

                text = cls.extract_page(page)

                if text:
                    texts.append(text)

        document.close()

        return "\n\n".join(texts)