from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Invoice Item
# ==========================================================

class InvoiceItem(BaseModel):

    description: Optional[str] = Field(
        default=None,
        description="Product or service description"
    )

    quantity: Optional[float] = Field(
        default=None,
        ge=0,
        description="Quantity"
    )

    unit_price: Optional[float] = Field(
        default=None,
        ge=0,
        description="Unit price"
    )

    amount: Optional[float] = Field(
        default=None,
        ge=0,
        description="Line total"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Laptop",
                "quantity": 2,
                "unit_price": 60000,
                "amount": 120000
            }
        }
    )


# ==========================================================
# Invoice
# ==========================================================

class Invoice(BaseModel):

    invoice_number: Optional[str] = None

    invoice_date: Optional[str] = None

    due_date: Optional[str] = None

    purchase_order: Optional[str] = None

    vendor_name: Optional[str] = None

    customer: Optional[str] = None

    retailer: Optional[str] = None

    state: Optional[str] = None

    gstin: Optional[str] = None

    currency: Optional[str] = None

    subtotal: Optional[float] = None

    tax: Optional[float] = None

    shipping: Optional[float] = None

    discount: Optional[float] = None

    service_charge: Optional[float] = None

    balance_due: Optional[float] = None

    total: Optional[float] = None

    items: List[InvoiceItem] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invoice_number": "INV-1001",
                "invoice_date": "07/07/2026",
                "due_date": "14/07/2026",
                "vendor_name": "ABC Electronics Pvt. Ltd.",
                "customer": "XYZ Solutions Pvt. Ltd.",
                "currency": "INR",
                "subtotal": 126000,
                "tax": 22680,
                "total": 148680,
                "items": [
                    {
                        "description": "Laptop",
                        "quantity": 2,
                        "unit_price": 60000,
                        "amount": 120000
                    }
                ]
            }
        }
    )


# ==========================================================
# Confidence
# ==========================================================

class Confidence(BaseModel):

    confidence: int = Field(
        ge=0,
        le=100
    )

    confidence_level: str


# ==========================================================
# Invoice Response
# ==========================================================

class InvoiceResponse(BaseModel):

    status: str

    errors: List[str] = Field(default_factory=list)

    warnings: List[str] = Field(default_factory=list)

    invoice: Invoice

    confidence: int

    confidence_level: str

    vendor: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "SUCCESS",
                "errors": [],
                "warnings": [],
                "invoice": {
                    "invoice_number": "INV-1001",
                    "invoice_date": "07/07/2026",
                    "total": 148680,
                    "currency": "INR",
                    "items": []
                },
                "confidence": 96,
                "confidence_level": "Excellent",
                "vendor": "ABC Electronics"
            }
        }
    )