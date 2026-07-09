from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from services.pipeline import InvoicePipeline

router = APIRouter(prefix="/api", tags=["Invoice"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".tif",
    ".bmp",
    ".webp"
}


@router.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):

    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}"
        )

    filename = f"{uuid4().hex}{suffix}"

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:

        buffer.write(await file.read())

    try:

        pipeline = InvoicePipeline()

        result = pipeline.process(str(file_path))

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass