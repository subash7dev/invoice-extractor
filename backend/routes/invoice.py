from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from services.llm import extract_invoice as llm_extract_invoice
from services.parser import pdf_to_images
from services.ocr import extract_text
from services.cleanup import clean_text
from services.validator import validate_invoice

router = APIRouter(tags=["Invoice"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/extract")
async def extract_invoice_route(file: UploadFile = File(...)):
    allowed_types = {
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/jpg",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG and JPG files are supported."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------------------------
    # OCR
    # ---------------------------
    extracted_text = ""

    if file.content_type == "application/pdf":
        images = pdf_to_images(str(file_path))

        for image in images:
            extracted_text += extract_text(image)
            extracted_text += "\n"
    else:
        extracted_text = extract_text(str(file_path))

    # ---------------------------
    # Clean OCR Text
    # ---------------------------
    cleaned_text = clean_text(extracted_text)

    # ---------------------------
    # LLM Extraction
    # ---------------------------
    raw_json = llm_extract_invoice(cleaned_text)

    # ---------------------------
    # Validate & Normalize JSON
    # ---------------------------
    try:
        invoice = validate_invoice(raw_json)
    except Exception as e:
        return {
            "error": "Failed to parse LLM response",
            "details": str(e),
            "raw_output": raw_json
        }

    # ---------------------------
    # Response
    # ---------------------------
    return {
        "filename": file.filename,
        "invoice": invoice
    }