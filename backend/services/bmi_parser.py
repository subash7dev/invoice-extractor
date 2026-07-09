import re


class BMIParser:
    """
    Vendor-specific parser for BMI invoices.
    """

    @staticmethod
    def extract(text: str):

        invoice = {}

        invoice["invoice_number"] = BMIParser.invoice_number(text)

        invoice["invoice_date"] = BMIParser.invoice_date(text)

        invoice["due_date"] = BMIParser.due_date(text)

        invoice["vendor_name"] = "BMI Brand Services"

        invoice["retailer"] = BMIParser.retailer(text)

        invoice["state"] = BMIParser.state(text)

        invoice["customer"] = BMIParser.customer(text)

        invoice["currency"] = "USD"

        invoice["subtotal"] = BMIParser.subtotal(text)

        invoice["service_charge"] = BMIParser.service_charge(text)

        invoice["balance_due"] = BMIParser.balance_due(text)

        invoice["total"] = BMIParser.total(text)

        invoice["purchase_order"] = None

        return invoice

    @staticmethod
    def invoice_number(text):

        patterns = [

            r"Ref#([A-Za-z0-9\-]+)",

            r"Invoice\s*Number\s*([A-Za-z0-9\-]+)",

            r"Invoice\s*Number\s*\n([A-Za-z0-9\-]+)"
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

        match = re.search(

            r"Invoice\s*Date\s*([0-9/]+)",

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1)

        return None

    @staticmethod
    def due_date(text):

        match = re.search(

            r"Due\s*On\s*Receipt|Due\s*Date\s*([0-9/]+)",

            text,

            re.IGNORECASE

        )

        if match:

            if match.lastindex:

                return match.group(1)

            return "Due On Receipt"

        return None

    @staticmethod
    def retailer(text):

        match = re.search(

            r"Retailer:\s*([^\n]+)",

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1).strip()

        return None

    @staticmethod
    def state(text):

        match = re.search(

            r"State:\s*([A-Z]{2})",

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1)

        return None

    @staticmethod
    def customer(text):

        match = re.search(

            r"Infinium Spirits Inc\.(.*?)Due On Receipt",

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
    def subtotal(text):

        values = BMIParser.usd_values(text)

        if len(values) >= 2:

            return values[-2]

        return None

    @staticmethod
    def balance_due(text):

        values = BMIParser.usd_values(text)

        if values:

            return values[-1]

        return None

    @staticmethod
    def total(text):

        values = BMIParser.usd_values(text)

        if values:

            return max(values)

        return None

    @staticmethod
    def service_charge(text):

        match = re.search(

            r"Service Charge\s+([\d]+\.\d+)",

            text,

            re.IGNORECASE

        )

        if match:

            return float(match.group(1))

        return None

    @staticmethod
    def usd_values(text):

        matches = re.findall(

            r"USD\s*([\d]+\.\d{2})",

            text,

            re.IGNORECASE

        )

        values = []

        for value in matches:

            try:

                values.append(float(value))

            except Exception:

                pass

        return values