class ConfidenceScorer:
    """
    Production-grade confidence scorer.

    Confidence is calculated using:
    - Required fields
    - Financial fields
    - Items
    - Warnings
    - Errors
    """

    REQUIRED_FIELDS = [

        "invoice_number",

        "vendor_name",

        "invoice_date",

        "total"

    ]

    OPTIONAL_FIELDS = [

        "due_date",

        "purchase_order",

        "customer",

        "currency",

        "subtotal",

        "tax",

        "shipping",

        "discount",

        "items"

    ]

    @classmethod
    def calculate(cls, result):

        invoice = result.get("invoice", {})

        errors = result.get("errors", [])

        warnings = result.get("warnings", [])

        score = 0

        # ---------------------------------------
        # Required Fields (60)
        # ---------------------------------------

        required_weight = 60 / len(cls.REQUIRED_FIELDS)

        for field in cls.REQUIRED_FIELDS:

            value = invoice.get(field)

            if value not in [

                None,

                "",

                []

            ]:

                score += required_weight

        # ---------------------------------------
        # Optional Fields (30)
        # ---------------------------------------

        optional_weight = 30 / len(cls.OPTIONAL_FIELDS)

        for field in cls.OPTIONAL_FIELDS:

            value = invoice.get(field)

            if value not in [

                None,

                "",

                []

            ]:

                score += optional_weight

        # ---------------------------------------
        # Items Bonus
        # ---------------------------------------

        items = invoice.get("items", [])

        if items:

            score += 10

        # ---------------------------------------
        # Penalties
        # ---------------------------------------

        score -= len(errors) * 15

        score -= len(warnings) * 5

        score = round(score)

        score = max(0, min(100, score))

        return {

            "confidence": score,

            "confidence_level": cls.level(score)

        }

    @staticmethod
    def level(score):

        if score >= 95:

            return "Excellent"

        if score >= 85:

            return "Very Good"

        if score >= 70:

            return "Good"

        if score >= 50:

            return "Fair"

        return "Poor"