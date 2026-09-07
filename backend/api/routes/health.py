"""Health check endpoints."""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "healthcare-triage-api",
        "version": "1.0.0"
    }

@router.get("/ready")
async def readiness_check():
    return {"status": "ready"}
