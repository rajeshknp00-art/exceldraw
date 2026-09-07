"""RAG Pipeline for medical guidelines retrieval using Groq embeddings."""
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class MedicalRAGPipeline:
    def __init__(self):
        self.milvus_uri = os.getenv("MILVUS_URI", "http://localhost:19530")
        self.milvus_token = os.getenv("MILVUS_TOKEN", "root")
        self.collection_name = "medical_guidelines"
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Use Groq for embeddings (free tier available)
        # Groq supports embedding models like nomic-embed-text
        self.groq_base_url = "https://api.groq.com/openai/v1"
        
    async def initialize(self):
        """Initialize the RAG pipeline with medical guidelines."""
        pass
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding using Groq's embedding API."""
        if not self.groq_api_key:
            # Return mock embedding for development
            import hashlib
            import random
            random.seed(hash(text))
            return [random.uniform(-1, 1) for _ in range(768)]
        
        import httpx
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.groq_api_key}"}
            response = await client.post(
                f"https://api.groq.com/openai/v1/embeddings",
                json={
                    "model": "nomic-embed-text-v1.5",
                    "input": text
                },
                headers={"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
    
    async def search_guidelines(self, query: str, top_k: int = 5) -> List[dict]:
        """Search medical guidelines for relevant content."""
        # In production, this would use Milvus/vector DB
        # For now, return mock data with medical guidelines
        return [
            {
                "guideline_id": "WHO-2023-001",
                "title": "Acute Abdominal Pain Assessment",
                "content": "Assess for peritonitis signs: rebound tenderness, guarding, rigidity. Check vital signs. Consider imaging (CT abdomen) if surgical cause suspected. Early surgical consultation for suspected perforation or ischemia.",
                "source": "WHO Clinical Guidelines 2023",
                "relevance_score": 0.92,
                "citations": ["WHO-2023", "CDC-2022"]
            },
            {
                "guideline_id": "CDC-2022-045",
                "title": "Chest Pain Triage Protocol",
                "content": "Immediate ECG within 10 minutes of arrival. Troponin at 0 and 3 hours. Consider HEART score for risk stratification. Aspirin 325mg chewed if ACS suspected. Nitroglycerin for ongoing pain. Immediate cardiology consultation for STEMI.",
                "source": "CDC Emergency Protocols 2022",
                "relevance_score": 0.87,
                "citations": ["CDC-2022", "AHA-2021"]
            },
            {
                "guideline_id": "WHO-2023-012",
                "title": "Headache Red Flags Assessment",
                "content": "Thunderclap headache: consider subarachnoid hemorrhage. New headache in >50: consider temporal arteritis. Headache with fever/stiff neck: consider meningitis. Papilledema: consider IIH or mass lesion. Progressive worsening: imaging indicated.",
                "source": "WHO Neurology Guidelines 2023",
                "relevance_score": 0.82,
                "citations": ["WHO-2023", "IHS-2018"]
            }
        ]
    
    async def get_guideline_by_id(self, guideline_id: str) -> dict:
        """Get full guideline by ID."""
        guidelines = {
            "WHO-2023-001": {
                "guideline_id": "WHO-2023-001",
                "title": "Acute Abdominal Pain Assessment",
                "full_text": "Complete guideline text for abdominal pain assessment...",
                "sections": ["Assessment", "Red Flags", "Investigations", "Management"],
                "citations": ["WHO-2023", "CDC-2022"]
            },
            "CDC-2022-045": {
                "guideline_id": "CDC-2022-045",
                "title": "Chest Pain Triage Protocol",
                "full_text": "Complete guideline text for chest pain triage...",
                "sections": ["Initial Assessment", "ECG Criteria", "Biomarkers", "Risk Stratification", "Disposition"],
                "citations": ["CDC-2022", "AHA-2021"]
            }
        }
        return guidelines.get(guideline_id, {
            "guideline_id": guideline_id,
            "title": "Guideline Not Found",
            "full_text": "Guideline not found in database",
            "sections": [],
            "citations": []
        })

# Singleton instance
rag_pipeline = None

async def get_rag_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = MedicalRAGPipeline()
        await rag_pipeline.initialize()
    return rag_pipeline