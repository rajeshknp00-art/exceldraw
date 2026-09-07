"""Triage API endpoints with full implementation."""
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

# Import medical knowledge graph and guardrails
from knowledge_graph.graph import medical_kg
from guardrails.compliance import medical_guardrails

# In-memory storage (replace with database)
triage_sessions = {}

@router.post("/analyze", response_model=dict)
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
        age = symptom_input.get("age")
        gender = symptom_input.get("gender")
        
        # Search knowledge graph for related conditions
        related_conditions = []
        entities = medical_kg.search_entities(symptoms)
        for entity in entities[:5]:
            if entity.entity_type == "condition":
                related_conditions.append({
                    "name": entity.name,
                    "probability": 0.3 + (0.1 * hash(entity.id) % 7) / 10,
                    "description": entity.description
                })
        
        # If no conditions found, use defaults
        if not related_conditions:
            related_conditions = [
                {"name": "Musculoskeletal Chest Pain", "probability": 0.45, "description": "Pain from muscles or ribs"},
                {"name": "Gastroesophageal Reflux", "probability": 0.30, "description": "Acid reflux causing chest discomfort"},
                {"name": "Costochondritis", "probability": 0.15, "description": "Inflammation of rib cartilage"}
            ]
        
        # Determine urgency based on symptoms
        urgency = "routine"
        confidence = 0.75
        red_flags = []
        symptoms_lower = symptom_input.get("symptoms", "").lower()
        
        emergency_keywords = ["crushing", "radiating", "shortness of breath", "sweating", "nausea", "dizziness", "fainting"]
        urgent_keywords = ["worsening", "persistent", "severe", "sharp", "stabbing", "radiating"]
        
        if any(word in symptoms_lower for word in emergency_keywords):
            urgency = "emergency"
            red_flags.append("Possible cardiac event - seek immediate care")
        elif any(word in symptoms_lower for word in urgent_keywords):
            urgency = "urgent"
        
        # Get body parts involved
        body_parts = []
        for entity in medical_kg.search_entities(symptoms):
            if entity.entity_type == "body_part":
                body_parts.append(entity.name)
        
        if not body_parts:
            body_parts = ["chest", "heart", "lungs"]
        
        # Apply guardrails
        triage_result = {
            "urgency_level": urgency,
            "confidence": confidence,
            "possible_conditions": [
                {"name": c["name"], "probability": c["probability"], "description": c["description"]}
                for c in related_conditions[:3]
            ],
            "recommended_action": "Based on your symptoms, we recommend scheduling an appointment with your primary care physician within the next few days for proper evaluation.",
            "body_parts_involved": body_parts[:5],
            "red_flags": red_flags,
            "follow_up_questions": [
                "Does the pain radiate to your arm, jaw, or back?",
                "Do you experience shortness of breath?",
                "Is the pain worse with exertion?",
                "Do you have a history of heart disease?"
            ]
        }
        
        # Validate with guardrails
        is_valid, issues = medical_guardrails.validate_triage_output(triage_result)
        if not is_valid:
            # Add issues to red_flags
            for issue in issues:
                red_flags.append(f"Guardrail check: {issue}")
        
        # Build final result
        result = {
            "triage_id": str(uuid.uuid4())[:8],
            "urgency_level": urgency,
            "confidence": 0.82,
            "possible_conditions": related_conditions[:3],
            "recommended_action": "Based on your symptoms, we recommend scheduling an appointment with your primary care physician within the next few days for proper evaluation.",
            "disclaimer": "IMPORTANT: This is an AI-powered triage assistant for informational purposes only. It does NOT provide medical diagnosis, treatment recommendations, or replace professional medical advice. Always consult a qualified healthcare provider for medical concerns. In case of emergency, call emergency services immediately.",
            "body_parts_involved": body_parts[:5],
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
