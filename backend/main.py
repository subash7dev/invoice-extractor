from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.invoice import router as invoice_router

app = FastAPI(
    title="Invoice Extraction API",
    version="1.0.0",
    description="AI-powered Invoice Extraction using PaddleOCR and Llama 3.2"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invoice_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Invoice Extraction API Running"
    }