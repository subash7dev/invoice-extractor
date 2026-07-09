from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.invoice import router as invoice_router

app = FastAPI(

    title="Invoice Extraction API",

    version="2.0.0",

    description="Production-grade AI Invoice Extraction API"

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

app.include_router(invoice_router)


@app.get("/")
def root():

    return {

        "application": "Invoice Extraction API",

        "version": "2.0.0",

        "status": "running",

        "documentation": "/docs"

    }


@app.get("/health")
def health():

    return {

        "status": "healthy"

    }


@app.get("/version")
def version():

    return {

        "version": "2.0.0"

    }


@app.get("/ping")
def ping():

    return {

        "message": "pong"

    }