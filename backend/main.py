from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.database import engine
from backend.db import models 
from backend.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Skepti-Scan API is starting up...")
    models.Base.metadata.create_all(bind=engine)
    print("Database tables verified/created.")
    yield
    print("Skepti-Scan API is shutting down...")

app = FastAPI(
    title="Skepti-Scan API",
    description="RAG-based fact-checking and verification system.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "skepti-scan-api"}
