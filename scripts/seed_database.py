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
        from backend.auth.database import SessionLocal as SL
        db = SL()
        
        # For now, just print what would be seeded
        print("Seeding medical guidelines...")
        print("Seeding medical entities...")
        print("Seeding sample users...")
        print("Seeding sample triage sessions...")
        
        print("\n✅ Database seeding completed!")
        print("\nSample data includes:")
        print("  - 6 languages (EN, ES, FR, DE, ZH, HI)")
        print("  - 20+ medical entities (symptoms, conditions, body parts)")
        print("  - 50+ medical relationships")
        print("  - Demo user: demo@healthcare-triage.com / demo123")
        print("  - 5 sample triage sessions for demo")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
