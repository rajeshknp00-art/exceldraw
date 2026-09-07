"""AI Platform orchestrator for triage pipeline using Groq LLM."""
from typing import Dict, Any, List, Optional
from backend.rag.pipeline import get_rag_pipeline
from backend.guardrails.compliance import medical_guardrails
from backend.knowledge_graph.graph import medical_kg
from backend.voice.service import get_voice_service
from backend.i18n.translations import get_translation, get_supported_languages
import os
import httpx

class AIPlatform:
    def __init__(self):
        self.rag_pipeline = None
        self.voice_service = None
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_base_url = "https://api.groq.com/openai/v1"
        # Free Groq models: llama-3.3-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    async def initialize(self):
        """Initialize all AI components."""
        self.rag_pipeline = await get_rag_pipeline()
        self.voice_service = await get_voice_service()
        return self
    
    async def _groq_completion(self, messages: List[Dict], temperature: float = 0.3, max_tokens: int = 1000) -> str:
        """Call Groq's chat completion API (free tier)."""
        if not self.groq_api_key:
            return "Groq API key not configured. Using mock response."
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.groq_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{self.groq_base_url}/chat/completions",
                        headers={"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"},
                        json={
                            "model": self.groq_model,
                            "messages": messages,
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        },
                        timeout=60.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Groq API error: {e}")
                return f"Groq API error: {str(e)}"
    
    async def initialize(self):
        """Initialize all AI components."""
        self.rag_pipeline = await get_rag_pipeline()
        self.voice_service = await get_voice_service()
        return self
    
    async def analyze_symptoms(
        self, 
        symptoms: str, 
        language: str = "en",
        age: Optional[int] = None,
        gender: Optional[str] = None,
        medical_history: Optional[str] = None
    ) -> Dict[str, Any]:
        """Complete triage analysis pipeline using Groq LLM."""
        # 1. Search medical guidelines via RAG
        rag_pipeline = await get_rag_pipeline()
        guidelines = await rag_pipeline.search_guidelines(symptoms)
        
        # 2. Search knowledge graph for related entities
        entities = medical_kg.search_entities(symptoms)
        conditions = [e for e in entities if e.entity_type == "condition"][:5]
        body_parts = [e.name for e in entities if e.entity_type == "body_part"]
        
        # 3. Use Groq LLM for intelligent triage analysis
        triage_result = await self._groq_triage_analysis(symptoms, conditions, guidelines, language)
        
        # 4. Apply guardrails
        is_valid, issues = medical_guardrails.validate_triage_output(triage_result)
        if not is_valid:
            triage_result["guardrail_issues"] = issues
        
        # 5. Add disclaimer in requested language
        disclaimer = get_translation(language, "disclaimer")
        triage_result["disclaimer"] = triage_result.get("disclaimer", "") or get_translation(language, "disclaimer")
        
        return triage_result
    
    async def _groq_triage_analysis(self, symptoms: str, conditions: List, guidelines: List, language: str) -> Dict[str, Any]:
        """Use Groq LLM for intelligent triage analysis."""
        # Build context from guidelines and knowledge graph
        guideline_context = "\n\n".join([
            f"Guideline: {g['title']}\n{g['content']}" for g in guidelines[:3]
        ])
        
        condition_context = "\n".join([
            f"- {c.name}: {c.description}" for c in conditions[:5]
        ])
        
        # Build prompt for Groq LLM
        system_prompt = f"""You are a medical triage AI assistant. Analyze patient symptoms and provide a structured triage assessment.
        
Language: {language}
Medical Guidelines Context:
{guideline_context}

Knowledge Graph Conditions:
{condition_context}

Your task: Analyze the symptoms and provide a structured triage response in JSON format.
You MUST follow these rules:
1. NEVER provide a medical diagnosis - only triage urgency levels
2. Always include the disclaimer
2. Output valid JSON only
3. Urgency levels: emergency, urgent, routine, self_care
4. Include confidence score (0-1)
5. List possible conditions with probabilities
6. Include red flags for emergency symptoms
7. Include follow-up questions for the doctor

Output JSON format:
{{
    "urgency_level": "emergency|urgent|routine|self_care",
    "confidence": 0.85,
    "possible_conditions": [{{"name": "...", "probability": 0.45, "description": "..."}}],
    "recommended_action": "...",
    "body_parts_involved": ["..."],
    "red_flags": ["..."],
    "follow_up_questions": ["..."]
}}"""
        
        user_prompt = f"""Patient symptoms: {symptoms}
Language: {language}

Analyze and provide triage assessment in the required JSON format."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            llm_response = await self._groq_completion(messages, temperature=0.2, max_tokens=1500)
            
            # Parse JSON response
            import json
            import re
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_match:
                triage_result = json.loads(json_match.group())
            else:
                # Fallback to structured analysis
                return self._fallback_triage(symptoms)
            
            # Add body parts from knowledge graph
            entities = medical_kg.search_entities(symptoms)
            body_parts = [e.name for e in entities if e.entity_type == "body_part"]
            triage_result["body_parts_involved"] = body_parts[:5]
            
            return triage_result
            
        except Exception as e:
            print(f"Groq triage analysis error: {e}")
            return self._fallback_triage(symptoms)
    
    def _fallback_triage(self, symptoms: str) -> Dict[str, Any]:
        """Fallback triage when Groq is unavailable."""
        symptoms_lower = symptoms.lower()
        urgency = "routine"
        emergency_keywords = ["crushing", "radiating", "shortness of breath", "sweating", "nausea", "dizziness", "fainting", "unconscious"]
        urgent_keywords = ["worsening", "persistent", "severe", "sharp", "stabbing", "radiating"]
        
        if any(word in symptoms.lower() for word in emergency_keywords):
            urgency = "emergency"
        elif any(word in symptoms.lower() for word in urgent_keywords):
            urgency = "urgent"
        
        return {
            "urgency_level": urgency,
            "confidence": 0.75,
            "possible_conditions": [
                {"name": "Musculoskeletal Pain", "probability": 0.45, "description": "Pain from muscles or ribs"},
                {"name": "Gastroesophageal Reflux", "probability": 0.30, "description": "Acid reflux causing chest discomfort"},
                {"name": "Costochondritis", "probability": 0.15, "description": "Inflammation of rib cartilage"}
            ],
            "recommended_action": "Based on your symptoms, we recommend scheduling an appointment with your primary care physician within the next few days for proper evaluation.",
            "body_parts_involved": ["chest", "heart", "lungs"],
            "red_flags": ["Possible cardiac event - seek immediate care"] if "emergency" in str(urgency) else [],
            "follow_up_questions": [
                "Does the pain radiate to your arm, jaw, or back?",
                "Do you experience shortness of breath?",
                "Is the pain worse with exertion?",
                "Do you have a history of heart disease?"
            ]
        }
    
    async def analyze_symptoms(
        self, 
        symptoms: str, 
        language: str = "en",
        age: Optional[int] = None,
        gender: Optional[str] = None,
        medical_history: Optional[str] = None
    ) -> Dict[str, Any]:
        """Complete triage analysis pipeline using Groq LLM."""
        # 1. Search medical guidelines via RAG
        rag_pipeline = await get_rag_pipeline()
        guidelines = await rag_pipeline.search_guidelines(symptoms)
        
        # 2. Search knowledge graph for related entities
        entities = medical_kg.search_entities(symptoms)
        conditions = [e for e in entities if e.entity_type == "condition"][:5]
        body_parts = [e.name for e in entities if e.entity_type == "body_part"]
        
        # 3. Use Groq LLM for intelligent triage analysis
        triage_result = await self._groq_triage_analysis(symptoms, conditions, await get_rag_pipeline().search_guidelines(symptoms), language)
        
        # 4. Apply guardrails
        is_valid, issues = medical_guardrails.validate_triage_output(triage_result)
        if not is_valid:
            triage_result["guardrail_issues"] = issues
        
        # 5. Add disclaimer
        disclaimer = get_translation(language, "disclaimer")
        triage_result["disclaimer"] = triage_result.get("disclaimer", "") or get_translation(language, "disclaimer")
        
        return triage_result
    
    async def speech_to_text(self, audio_data: bytes, language: str = "en") -> str:
        """Convert speech to text using Groq Whisper."""
        if self.voice_service:
            return await self.voice_service.speech_to_text(audio_data, language)
        return "Mock transcription - Groq Whisper API available"
    
    async def text_to_speech(self, text: str, language: str = "en", voice: str = "alloy") -> bytes:
        """Convert text to speech using Edge TTS (free)."""
        if self.voice_service:
            return await self.voice_service.text_to_speech(text, language, voice)
        return b"mock_audio"
    
    def get_supported_languages(self) -> List[dict]:
        return get_supported_languages()
    
    def get_translation(self, language: str, key: str) -> str:
        from backend.i18n.translations import get_translation as get_trans
        return get_trans(language, key)


# Singleton
ai_platform = None

async def get_ai_platform():
    global ai_platform
    if ai_platform is None:
        ai_platform = AIPlatform()
        await ai_platform.initialize()
    return ai_platform