from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.vector import init_qdrant, qdrant_client, embedding_model
from app.core.security import api_key_header
from app.core.llm import router as llm_router
from app.core.ocr import router as ingest_router
from app.core.vector import router as search_router, health_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jamb-ai")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting JAMB AI Tutor Pro v4.0")
    embedding_model.load()
    init_qdrant()
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="JAMB AI Tutor Pro v4.0",
    description="Nigeria's Most Powerful JAMB RAG Assistant — Built for 350+",
    version="4.0.0",
    lifespan=lifespan
)

# Security
app.dependency_overrides[api_key_header] = api_key_header

# Routers
app.include_router(ingest_router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(search_router, prefix="/api/v1", tags=["Search"])
app.include_router(llm_router, prefix="/api/v1", tags=["Ask"])
app.include_router(health_router, prefix="/api/v1", tags=["System"])

@app.get("/")
async def root():
    return {"message": "JAMB AI Tutor Pro v4.0 — Live & Ready", "docs": "/docs"}
