import re


class TextCleaner:
    """
    Production-grade OCR text cleaner.
    """

    @staticmethod
    def clean(text: str) -> str:

        if not text:
            return ""

        text = TextCleaner.normalize_unicode(text)

        text = TextCleaner.remove_control_characters(text)

        text = TextCleaner.normalize_spaces(text)

        text = TextCleaner.remove_duplicate_lines(text)

        text = TextCleaner.fix_currency(text)

        text = TextCleaner.normalize_dates(text)

        return text.strip()

    @staticmethod
    def normalize_unicode(text: str) -> str:

        replacements = {

            "₹": "INR ",

            "$": "USD ",

            "€": "EUR ",

            "£": "GBP ",

            "Rs.": "INR ",

            "Rs": "INR ",

            "GSTIN:": "GSTIN ",

            "GST No.": "GSTIN ",

            "GST No": "GSTIN "
        }

        for old, new in replacements.items():

            text = text.replace(old, new)

        return text

    @staticmethod
    def remove_control_characters(text: str) -> str:

        return re.sub(
            r"[\x00-\x1F\x7F]",
            "",
            text
        )

    @staticmethod
    def normalize_spaces(text: str) -> str:

        lines = []

        for line in text.splitlines():

            line = re.sub(
                r"\s+",
                " ",
                line
            ).strip()

            if line:
                lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def remove_duplicate_lines(text: str) -> str:

        unique = []

        previous = None

        for line in text.splitlines():

            if line == previous:
                continue

            unique.append(line)

            previous = line

        return "\n".join(unique)

    @staticmethod
    def fix_currency(text: str) -> str:

        text = re.sub(
            r"USD\s+USD",
            "USD",
            text
        )

        text = re.sub(
            r"INR\s+INR",
            "INR",
            text
        )

        return text

    @staticmethod
    def normalize_dates(text: str) -> str:

        text = re.sub(

            r"(\d{1,2})-(\d{1,2})-(\d{2,4})",

            r"\1/\2/\3",

            text
        )

        return text

    @staticmethod
    def split_lines(text: str):

        return [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

    @staticmethod
    def to_lower(text: str):

        return text.lower()

    @staticmethod
    def remove_empty(text: str):

        return "\n".join(

            line

            for line in text.splitlines()

            if line.strip()

        )