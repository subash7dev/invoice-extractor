import json


def _to_number(value):
    """Convert numeric strings to int/float where possible."""
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        value = value.replace(",", "").replace("₹", "").replace("Rs.", "").strip()

        if value == "":
            return None

        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    return value


def validate_invoice(invoice_json: str):
    """
    Parse and normalize LLM JSON output.
    """

    data = json.loads(invoice_json)

    # Numeric fields
    numeric_fields = [
        "subtotal",
        "tax",
        "discount",
        "shipping",
        "total"
    ]

    for field in numeric_fields:
        data[field] = _to_number(data.get(field))

    # Items
    items = data.get("items", [])

    for item in items:
        item["quantity"] = _to_number(item.get("quantity"))
        item["unit_price"] = _to_number(item.get("unit_price"))
        item["amount"] = _to_number(item.get("amount"))

    data["items"] = items

    return data