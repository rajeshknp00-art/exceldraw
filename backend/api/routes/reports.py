"""Triage report generation endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

router = APIRouter()

class ReportRequest(BaseModel):
    triage_id: str
    format: str = "pdf"  # pdf, html, text
    include_citations: bool = True
    language: str = "en"

class ReportResponse(BaseModel):
    success: bool
    report_id: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None

@router.post("/generate", response_model=dict)
async def generate_report(report_request: dict):
    """Generate a triage report in PDF, HTML, or text format."""
    try:
        triage_id = report_request.get("triage_id")
        format_type = report_request.get("format", "pdf")
        language = report_request.get("language", "en")
        
        if not triage_id:
            raise HTTPException(status_code=400, detail="triage_id is required")
        
        report_id = str(uuid.uuid4())[:8]
        
        # Mock report generation
        return {
            "success": True,
            "report_id": str(uuid.uuid4())[:8],
            "download_url": f"/api/v1/reports/download/{str(uuid.uuid4())[:8]}",
            "format": format_type,
            "language": language,
            "created_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/download/{report_id}")
async def download_report(report_id: str):
    """Download a generated report."""
    # Mock implementation
    return {"message": f"Download report {report_id}"}

@router.get("/templates")
async def get_report_templates():
    """Get available report templates."""
    return {
        "templates": [
            {"id": "standard", "name": "Standard Triage Report", "description": "Standard triage assessment report"},
            {"id": "detailed", "name": "Detailed Medical Report", "description": "Comprehensive report with all details"},
            {"id": "patient", "name": "Patient Summary", "description": "Simplified summary for patients"}
        ]
    }
