import re


class ScanAppsParser:
    """
    Vendor-specific parser for ScanApps invoices.
    """

    @staticmethod
    def extract(text: str):

        invoice = {}

        invoice["invoice_number"] = ScanAppsParser.invoice_number(text)

        invoice["invoice_date"] = ScanAppsParser.invoice_date(text)

        invoice["due_date"] = ScanAppsParser.due_date(text)

        invoice["purchase_order"] = ScanAppsParser.purchase_order(text)

        invoice["vendor_name"] = ScanAppsParser.vendor_name(text)

        invoice["customer"] = ScanAppsParser.customer(text)

        invoice["currency"] = ScanAppsParser.currency(text)

        invoice["subtotal"] = ScanAppsParser.subtotal(text)

        invoice["tax"] = ScanAppsParser.tax(text)

        invoice["shipping"] = ScanAppsParser.shipping(text)

        invoice["discount"] = ScanAppsParser.discount(text)

        invoice["total"] = ScanAppsParser.total(text)

        return invoice

    @staticmethod
    def search(patterns, text):

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.MULTILINE
            )

            if match:

                return match.group(1).strip()

        return None

    @staticmethod
    def money(patterns, text):

        value = ScanAppsParser.search(patterns, text)

        if value is None:
            return None

        value = value.replace(",", "")

        try:
            return float(value)

        except Exception:
            return None

    @staticmethod
    def invoice_number(text):

        return ScanAppsParser.search(

            [

                r"Invoice\s*No[:\s]+([A-Za-z0-9\-]+)",

                r"Invoice\s*Number[:\s]+([A-Za-z0-9\-]+)",

                r"Invoice\s*#[:\s]+([A-Za-z0-9\-]+)"

            ],

            text

        )

    @staticmethod
    def invoice_date(text):

        return ScanAppsParser.search(

            [

                r"Invoice\s*Date[:\s]+([0-9/\-]+)",

                r"Date[:\s]+([0-9/\-]+)"

            ],

            text

        )

    @staticmethod
    def due_date(text):

        return ScanAppsParser.search(

            [

                r"Due\s*Date[:\s]+([0-9/\-]+)"

            ],

            text

        )

    @staticmethod
    def purchase_order(text):

        return ScanAppsParser.search(

            [

                r"Purchase\s*Order[:\s]+([A-Za-z0-9\-]+)",

                r"PO[:\s]+([A-Za-z0-9\-]+)"

            ],

            text

        )

    @staticmethod
    def vendor_name(text):

        vendor = ScanAppsParser.search(

            [

                r"Vendor[:\s]+([^\n]+)",

                r"Supplier[:\s]+([^\n]+)"

            ],

            text

        )

        return vendor or "ScanApps"

    @staticmethod
    def customer(text):

        match = re.search(

            r"Bill To(.*?)Ship To",

            text,

            re.IGNORECASE | re.DOTALL

        )

        if not match:

            return None

        customer = match.group(1)

        customer = re.sub(r"\s+", " ", customer)

        customer = customer.replace("\n", ", ")

        return customer.strip(" ,")

    @staticmethod
    def currency(text):

        currency = ScanAppsParser.search(

            [

                r"\b(INR|USD|EUR|GBP)\b"

            ],

            text

        )

        return currency or "INR"

    @staticmethod
    def subtotal(text):

        return ScanAppsParser.money(

            [

                r"Subtotal[:\s₹$A-Z]*([\d,.]+)"

            ],

            text

        )

    @staticmethod
    def tax(text):

        return ScanAppsParser.money(

            [

                r"(?:GST|Tax|VAT)[:\s₹$A-Z]*([\d,.]+)"

            ],

            text

        )

    @staticmethod
    def shipping(text):

        return ScanAppsParser.money(

            [

                r"Shipping[:\s₹$A-Z]*([\d,.]+)"

            ],

            text

        )

    @staticmethod
    def discount(text):

        return ScanAppsParser.money(

            [

                r"Discount[:\s₹$A-Z-]*([\d,.]+)"

            ],

            text

        )

    @staticmethod
    def total(text):

        return ScanAppsParser.money(

            [

                r"Grand\s*Total[:\s₹$A-Z]*([\d,.]+)",

                r"Total\s*Amount[:\s₹$A-Z]*([\d,.]+)",

                r"Total[:\s₹$A-Z]*([\d,.]+)"

            ],

            text

        )