from copy import deepcopy


class InvoiceValidator:
    """
    Production-grade invoice validator.
    """

    REQUIRED_FIELDS = [

        "invoice_number",

        "vendor_name",

        "invoice_date",

        "total"
    ]

    @classmethod
    def validate(cls, invoice: dict):

        invoice = deepcopy(invoice)

        errors = []

        warnings = []

        invoice = cls.normalize(invoice)

        cls.validate_required(
            invoice,
            errors
        )

        cls.validate_amounts(
            invoice,
            warnings
        )

        cls.validate_items(
            invoice,
            warnings
        )

        status = "SUCCESS"

        if errors:

            status = "FAILED"

        elif warnings:

            status = "WARNING"

        return {

            "status": status,

            "errors": errors,

            "warnings": warnings,

            "invoice": invoice
        }

    @classmethod
    def normalize(cls, invoice):

        defaults = [

            "invoice_number",

            "invoice_date",

            "due_date",

            "purchase_order",

            "vendor_name",

            "customer",

            "retailer",

            "state",

            "gstin",

            "currency",

            "subtotal",

            "tax",

            "shipping",

            "discount",

            "service_charge",

            "balance_due",

            "total",

            "items"

        ]

        for field in defaults:

            if field not in invoice:

                invoice[field] = None

        if invoice["items"] is None:

            invoice["items"] = []

        return invoice

    @classmethod
    def validate_required(

        cls,

        invoice,

        errors

    ):

        for field in cls.REQUIRED_FIELDS:

            value = invoice.get(field)

            if value in [

                None,

                "",

                []

            ]:

                errors.append(

                    f"{field} is missing"

                )

    @classmethod
    def validate_amounts(

        cls,

        invoice,

        warnings

    ):

        subtotal = invoice.get("subtotal")

        tax = invoice.get("tax") or 0

        shipping = invoice.get("shipping") or 0

        discount = invoice.get("discount") or 0

        total = invoice.get("total")

        if subtotal is None:

            return

        if total is None:

            return

        expected = (

            subtotal

            + tax

            + shipping

            - discount

        )

        if abs(expected - total) > 0.05:

            warnings.append(

                "Total does not match subtotal + tax + shipping - discount"

            )

    @classmethod
    def validate_items(

        cls,

        invoice,

        warnings

    ):

        items = invoice.get("items", [])

        for index, item in enumerate(items):

            qty = item.get("quantity")

            unit = item.get("unit_price")

            amount = item.get("amount")

            if None in [

                qty,

                unit,

                amount

            ]:

                continue

            expected = qty * unit

            if abs(expected - amount) > 0.05:

                warnings.append(

                    f"Item {index + 1}: Amount mismatch"

                )