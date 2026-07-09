import re


class AmazonParser:
    """
    Vendor-specific parser for Amazon invoices.
    """

    @staticmethod
    def extract(text: str):

        invoice = {}

        invoice["invoice_number"] = AmazonParser.invoice_number(text)

        invoice["invoice_date"] = AmazonParser.invoice_date(text)

        invoice["due_date"] = AmazonParser.due_date(text)

        invoice["purchase_order"] = AmazonParser.purchase_order(text)

        invoice["vendor_name"] = "Amazon"

        invoice["customer"] = AmazonParser.customer(text)

        invoice["currency"] = AmazonParser.currency(text)

        invoice["subtotal"] = AmazonParser.subtotal(text)

        invoice["tax"] = AmazonParser.tax(text)

        invoice["shipping"] = AmazonParser.shipping(text)

        invoice["discount"] = AmazonParser.discount(text)

        invoice["total"] = AmazonParser.total(text)

        return invoice

    @staticmethod
    def invoice_number(text):

        patterns = [

            r"Invoice\s*Number[:\s]+([A-Za-z0-9\-]+)",

            r"Invoice\s*#[:\s]+([A-Za-z0-9\-]+)",

            r"Tax\s*Invoice[:\s]+([A-Za-z0-9\-]+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None

    @staticmethod
    def invoice_date(text):

        patterns = [

            r"Invoice\s*Date[:\s]+([0-9/\-]+)",

            r"Order\s*Date[:\s]+([0-9/\-]+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None

    @staticmethod
    def due_date(text):

        match = re.search(

            r"Due\s*Date[:\s]+([0-9/\-]+)",

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1).strip()

        return None

    @staticmethod
    def purchase_order(text):

        patterns = [

            r"Purchase\s*Order[:\s]+([A-Za-z0-9\-]+)",

            r"PO[:\s]+([A-Za-z0-9\-]+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None

    @staticmethod
    def customer(text):

        match = re.search(

            r"Bill To(.*?)Ship To",

            text,

            re.DOTALL | re.IGNORECASE

        )

        if not match:

            return None

        customer = match.group(1)

        customer = re.sub(r"\n+", ", ", customer)

        customer = re.sub(r"\s+", " ", customer)

        return customer.strip(" ,")

    @staticmethod
    def currency(text):

        match = re.search(

            r"\b(INR|USD|EUR|GBP)\b",

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1).upper()

        return "INR"

    @staticmethod
    def subtotal(text):

        return AmazonParser.money(

            r"Subtotal[:\s₹$A-Z]*([\d,]+\.\d{2})",

            text

        )

    @staticmethod
    def tax(text):

        return AmazonParser.money(

            r"(?:GST|IGST|CGST|SGST|Tax)[:\s₹$A-Z]*([\d,]+\.\d{2})",

            text

        )

    @staticmethod
    def shipping(text):

        return AmazonParser.money(

            r"Shipping[:\s₹$A-Z]*([\d,]+\.\d{2})",

            text

        )

    @staticmethod
    def discount(text):

        return AmazonParser.money(

            r"Discount[:\s₹$A-Z\-]*([\d,]+\.\d{2})",

            text

        )

    @staticmethod
    def total(text):

        patterns = [

            r"Grand\s*Total[:\s₹$A-Z]*([\d,]+\.\d{2})",

            r"Total[:\s₹$A-Z]*([\d,]+\.\d{2})"

        ]

        for pattern in patterns:

            value = AmazonParser.money(pattern, text)

            if value is not None:

                return value

        return None

    @staticmethod
    def money(pattern, text):

        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )

        if not match:

            return None

        value = match.group(1)

        value = value.replace(",", "")

        try:

            return float(value)

        except Exception:

            return None