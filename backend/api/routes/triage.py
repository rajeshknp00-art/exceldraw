"""Triage API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime

router = APIRouter()

class SymptomInput(BaseModel):
    symptoms: str = Field(..., min_length=5, max_length=2000, description="Patient's symptom description")
    language: str = Field(default="en", pattern="^(en|es|fr|de|zh|hi)$")
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    medical_history: Optional[str] = None
    medications: Optional[List[str]] = None

class TriageResult(BaseModel):
    triage_id: str
    urgency_level: str  # emergency, urgent, routine, self_care
    confidence: float
    possible_conditions: List[dict]
    recommended_action: str
    disclaimer: str
    body_parts_involved: List[str]
    red_flags: List[str]
    follow_up_questions: List[str]
    created_at: str

class TriageResponse(BaseModel):
    success: bool
    data: Optional[TriageResult] = None
    error: Optional[str] = None

# In-memory storage (replace with database)
triage_sessions = {}

@router.post("/analyze", response_model=TriageResponse)
async def analyze_symptoms(symptom_input: dict):
    """
    Analyze patient symptoms and provide triage assessment.
    """
    try:
        # Generate unique triage ID
        triage_id = str(uuid.uuid4())[:8]
        
        # Get symptoms
        symptoms = symptom_input.get("symptoms", "")
        language = symptom_input.get("language", "en")
        
        # Mock triage logic (replace with actual AI pipeline)
        urgency = "routine"
        confidence = 0.75
        conditions = [
            {"name": "Musculoskeletal Chest Pain", "probability": 0.45, "description": "Pain from muscles or ribs"},
            {"name": "Gastroesophageal Reflux", "probability": 0.30, "description": "Acid reflux causing chest discomfort"},
            {"name": "Costochondritis", "probability": 0.15, "description": "Inflammation of rib cartilage"}
        ]
        
        # Determine urgency based on keywords
        symptoms_lower = symptom_input.get("symptoms", "").lower()
        red_flags = []
        if any(word in symptom_input.get("symptoms", "").lower() for word in ["crushing", "radiating", "shortness of breath", "sweating", "nausea"]):
            urgency = "emergency"
            red_flags.append("Possible cardiac event - seek immediate care")
        elif any(word in symptom_input.get("symptoms", "").lower() for word in ["worsening", "persistent", "severe"]):
            urgency = "urgent"
        
        result = {
            "triage_id": triage_id,
            "urgency_level": urgency,
            "confidence": 0.82,
            "possible_conditions": conditions,
            "recommended_action": "Based on your symptoms, we recommend scheduling an appointment with your primary care physician within the next few days for proper evaluation.",
            "disclaimer": "IMPORTANT: This is an AI-powered triage assistant for informational purposes only. It does NOT provide medical diagnosis, treatment recommendations, or replace professional medical advice. Always consult a qualified healthcare provider for medical concerns. In case of emergency, call emergency services immediately.",
            "body_parts_involved": ["chest", "heart", "lungs"],
            "red_flags": red_flags,
            "follow_up_questions": [
                "Does the pain radiate to your arm, jaw, or back?",
                "Do you experience shortness of breath?",
                "Is the pain worse with exertion?",
                "Do you have a history of heart disease?"
            ],
            "created_at": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "data": result,
            "error": None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Triage analysis failed: {str(e)}"
        )

@router.get("/history/{patient_id}")
async def get_triage_history(patient_id: str):
    """Get triage history for a patient."""
    # Mock implementation
    return {
        "success": True,
        "data": [],
        "error": None
    }

@router.get("/{triage_id}")
async def get_triage_result(triage_id: str):
    """Get a specific triage result."""
    return {
        "success": True,
        "data": None,
        "error": "Not found"
    }
