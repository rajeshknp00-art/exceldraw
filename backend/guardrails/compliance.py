"""Guardrails for medical AI safety compliance."""
import re
from typing import Dict, List, Tuple
import hashlib

class MedicalGuardrails:
    def __init__(self):
        self.diagnosis_patterns = [
            r"you have\s+\w+",
            r"diagnosis is\s+\w+",
            r"you are suffering from\s+\w+",
            r"this is\s+\w+\s+cancer",
            r"confirmed\s+\w+",
        ]
        self.pii_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
            (r"\b\d{10,}\b", "PHONE"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "EMAIL"),
            (r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "DOB"),
        ]
        self.disclaimer = (
            "IMPORTANT: This is an AI-powered triage assistant for informational purposes only. "
            "It does NOT provide medical diagnosis, treatment recommendations, or replace professional medical advice. "
            "Always consult a qualified healthcare provider for medical concerns. "
            "In case of emergency, call emergency services immediately."
        )
    
    def check_diagnosis_claims(self, text: str) -> Tuple[bool, List[str]]:
        """Check if text contains prohibited diagnosis claims."""
        violations = []
        for pattern in self.diagnosis_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                violations.extend(matches)
        return len(violations) > 0, violations
    
    def redact_pii(self, text: str) -> str:
        """Redact PII from text."""
        redacted = text
        for pattern, label in self.pii_patterns:
            redacted = re.sub(pattern, f"[{label}_REDACTED]", redacted)
        return redacted
    
    def add_disclaimer(self, text: str) -> str:
        """Add medical disclaimer to response."""
        return f"{text}\n\n{self.disclaimer}"
    
    def validate_triage_output(self, triage_result: dict) -> Tuple[bool, List[str]]:
        """Validate triage output for safety compliance."""
        issues = []
        
        # Check for diagnosis claims
        has_diagnosis, violations = self.check_diagnosis_claims(str(triage_result))
        if has_diagnosis:
            issues.append(f"Diagnosis claims detected: {violations}")
        
        # Check for required disclaimer
        if "disclaimer" not in str(triage_result).lower():
            issues.append("Missing medical disclaimer")
        
        # Check for confidence scores
        if "confidence" not in triage_result:
            issues.append("Missing confidence score")
        
        return len(issues) == 0, issues

# Singleton
medical_guardrails = MedicalGuardrails()
