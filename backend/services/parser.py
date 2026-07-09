import re
from typing import Dict


class InvoiceParser:
    """
    Generic rule-based parser.

    Used to extract high-confidence fields before sending
    the text to the LLM.
    """

    @staticmethod
    def _search(patterns, text):

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.MULTILINE
            )

            if match:

                groups = match.groups()

                if not groups:
                    continue

                value = groups[0].strip()

                if value:
                    return value

        return None

    @staticmethod
    def _money(value):

        if value is None:
            return None

        value = value.replace(",", "")

        value = value.replace("INR", "")

        value = value.replace("USD", "")

        value = value.replace("$", "")

        value = value.strip()

        try:
            return float(value)

        except Exception:
            return None

    @classmethod
    def extract(cls, text: str) -> Dict:

        data = {}

        data["invoice_number"] = cls._search(

            [

                r"Invoice\s*(?:No|Number|#)\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

                r"Invoice\s*Number\s*\n+([A-Za-z0-9\-\/]+)",

                r"Ref#([A-Za-z0-9\-\/]+)"

            ],

            text

        )

        data["invoice_date"] = cls._search(

            [

                r"Invoice\s*Date\s*[:\-]?\s*([0-9/\-.]+)",

                r"Date\s*[:\-]?\s*([0-9/\-.]+)"

            ],

            text

        )

        data["due_date"] = cls._search(

            [

                r"Due\s*Date\s*[:\-]?\s*([0-9/\-.]+)",

                r"Due\s*On\s*Receipt"

            ],

            text

        )

        data["purchase_order"] = cls._search(

            [

                r"Purchase\s*Order\s*[:\-]?\s*([A-Za-z0-9\-]+)",

                r"PO\s*[:\-]?\s*([A-Za-z0-9\-]+)"

            ],

            text

        )

        data["gstin"] = cls._search(

            [

                r"GSTIN\s*[:\-]?\s*([A-Z0-9]{15})"

            ],

            text

        )

        data["currency"] = cls._search(

            [

                r"\b(INR|USD|EUR|GBP)\b"

            ],

            text

        )

        subtotal = cls._search(

            [

                r"Subtotal\s*(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)"

            ],

            text

        )

        tax = cls._search(

            [

                r"(?:GST|Tax).*?(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)"

            ],

            text

        )

        shipping = cls._search(

            [

                r"Shipping.*?(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)"

            ],

            text

        )

        discount = cls._search(

            [

                r"Discount.*?(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)"

            ],

            text

        )

        total = cls._search(

            [

                r"Grand\s*Total\s*(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)",

                r"Total\s*Amount\s*(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)",

                r"Total\s*(?:INR|USD|\$)?\s*([\d,]+\.\d+|[\d,]+)"

            ],

            text

        )

        data["subtotal"] = cls._money(subtotal)

        data["tax"] = cls._money(tax)

        data["shipping"] = cls._money(shipping)

        data["discount"] = cls._money(discount)

        data["total"] = cls._money(total)

        return data