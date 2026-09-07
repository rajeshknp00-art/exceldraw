"""
Healthcare AI Triage Assistant - FastAPI Backend
Main entry point for the API server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from api.routes import auth, triage, reports, guidelines, health
from auth.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Healthcare AI Triage Assistant",
    description="AI-powered triage system with voice-based symptom checker, RAG on medical guidelines, guardrails, multi-language support, and triage report generation.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(triage.router, prefix="/api/v1/triage", tags=["triage"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(guidelines.router, prefix="/api/v1/guidelines", tags=["guidelines"])

@app.get("/")
async def root():
    return {
        "message": "Healthcare AI Triage Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
