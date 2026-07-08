# 📄 Invoice Extractor

An AI-powered invoice extraction system that uses **OCR (Optical Character Recognition)** and **Large Language Models (LLMs)** to extract structured information from invoice images and PDFs. The application returns clean, validated JSON output suitable for ERP systems, accounting software, and document automation workflows.

---

## 🚀 Features

- Upload invoices in JPG, PNG, or PDF format
- OCR-based text extraction
- AI-powered invoice field extraction
- Automatic JSON generation
- Validation of extracted fields
- Multi-page PDF support
- REST API built with FastAPI
- Simple Streamlit frontend

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- OpenAI GPT
- Tesseract OCR / EasyOCR
- Pillow
- pdf2image
- Pydantic

### Frontend

- Streamlit

---

# 📁 Project Structure

```text
invoice-extractor/
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   │
│   ├── prompts/
│   │   └── invoice_prompt.txt
│   │
│   ├── routes/
│   │   └── invoice.py
│   │
│   ├── services/
│   │   ├── cleanup.py
│   │   ├── llm.py
│   │   ├── ocr.py
│   │   ├── parser.py
│   │   ├── prompt.py
│   │   └── validator.py
│   │
│   └── uploads/
│       ├── sample_invoice.pdf
│       ├── page_1.png
│       └── page_2.png
│
├── frontend/
│   └── app.py
│
├── uploads/
│
├── requirements.txt
├── README.md
└── .env.example
```

---

# ⚙️ Solution Architecture

```text
User Uploads Invoice
        │
        ▼
Image Preprocessing
        │
        ▼
OCR Text Extraction
        │
        ▼
LLM Processing
        │
        ▼
Field Extraction
        │
        ▼
Validation
        │
        ▼
JSON Response
```

---

# 📋 Extracted Fields

The system extracts:

- Vendor Name
- Vendor Address
- Invoice Number
- Invoice Date
- Due Date
- Purchase Order
- Customer Details
- Items
- Quantity
- Unit Price
- Amount
- GST / Tax
- Shipping
- Discount
- Grand Total
- Currency
- Payment Terms

---

# 📄 Example Output

```json
{
  "invoice_number": "INV-1001",
  "vendor_name": "ABC Electronics Pvt. Ltd.",
  "invoice_date": "07/07/2026",
  "subtotal": 126000,
  "tax": 22680,
  "shipping": 1500,
  "discount": null,
  "total": 148180,
  "currency": "INR",
  "items": [
    {
      "description": "Laptop",
      "quantity": 2,
      "unit_price": 60000,
      "amount": 120000
    }
  ]
}
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/subash7dev/invoice-extractor.git
cd invoice-extractor
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the project root.

```env
OPENAI_API_KEY=your_api_key
```

---

# ▶️ Run Backend

Navigate to the backend directory:

```bash
cd backend
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Frontend

Open a new terminal.

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at:

```
http://localhost:8501
```

---

# 🔄 Processing Workflow

1. Upload invoice image or PDF.
2. PDF pages are converted to images (if applicable).
3. OCR extracts text from the document.
4. The extracted text is cleaned and parsed.
5. The LLM identifies invoice fields.
6. Validation ensures required fields and totals are correct.
7. The API returns structured JSON.

---

# 📷 Supported Formats

- JPG
- JPEG
- PNG
- PDF

---

# 📌 Future Improvements

- Batch invoice processing
- Multi-language invoices
- Handwritten invoice support
- Confidence scores
- Database storage
- Docker deployment
- Authentication
- Cloud deployment

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Subash Chandra Bose G**

GitHub: https://github.com/subash7dev

---

⭐ If you found this project useful, consider giving it a star on GitHub.