from ollama import chat

response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": """
You are an invoice extraction assistant.

Return ONLY valid JSON.
Do not explain anything.
Do not generate Python code.
Do not use markdown.

Return this format:

{
    "invoice_number": "",
    "vendor_name": "",
    "invoice_date": "",
    "due_date": "",
    "subtotal": null,
    "tax": null,
    "total": null,
    "currency": "",
    "items": []
}
"""
        },
        {
            "role": "user",
            "content": """
Invoice No: INV-1001
Vendor: ABC Pvt Ltd
Total: ₹12,500
Date: 07/07/2026
"""
        }
    ]
)

print(response["message"]["content"])