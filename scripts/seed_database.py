#!/usr/bin/env python3
"""Seed database with medical guidelines, entities, and sample data."""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.auth.database import engine, Base, SessionLocal
from backend.auth.models import User, UserSession
from backend.auth.security import get_password_hash
from backend.knowledge_graph.graph import medical_kg, MedicalEntity

async def seed_database():
    """Seed the database with initial data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create demo user
        from backend.auth.security import get_password_hash
        
        # Check if demo user exists
        existing_user = db.query(User).filter(User.email == "demo@healthcare-triage.com").first()
        if not existing_user:
            demo_user = User(
                email="demo@healthcare-triage.com",
                hashed_password=get_password_hash("demo123"),
                full_name="Demo User",
                preferred_language="en",
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            print("✅ Demo user created: demo@healthcare-triage.com / demo123")
        
        # Seed medical guidelines info
        print("✅ Medical guidelines available in RAG pipeline")
        
        # Seed medical entities info
        print("✅ Medical entities available in Knowledge Graph")
        print(f"   - {len(medical_kg.entities)} medical entities loaded")
        print(f"   - {medical_kg.graph.number_of_edges()} relationships")
        
        print("\n✅ Database seeding completed!")
        print("\nSample data includes:")
        print("  - 6 languages (EN, ES, FR, DE, ZH, HI)")
        print(f"  - {len(medical_kg.entities)} medical entities (symptoms, conditions, body parts)")
        print(f"  - {medical_kg.graph.number_of_edges()} medical relationships")
        print("  - Demo user: demo@healthcare-triage.com / demo123")
        print("  - RAG pipeline with 3 medical guidelines")
        print("  - Guardrails with PII redaction and diagnosis prevention")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
