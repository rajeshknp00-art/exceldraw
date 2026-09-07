# Healthcare AI Triage Assistant

## Overview
AI-powered triage system with voice-based symptom checker, RAG on medical guidelines, guardrails, multi-language support, and triage report generation.

## Architecture

### Layer 1: Presentation (Frontend)
- Next.js 14 with App Router
- Tailwind CSS for styling
- shadcn/ui component library
- Voice input via Web Speech API
- Multi-language accessibility

### Layer 2: Application (Backend)
- FastAPI (Python) with JWT authentication
- PostgreSQL for persistent data storage
- Redis for caching and rate limiting
- RESTful API endpoints

### Layer 3: AI/ML Intelligence
- **Voice AI**: Speech-to-Text (STT) + Text-to-Speech (TTS)
- **RAG**: Retrieval-Augmented Generation with medical guidelines
- **Guardrails**: Safety compliance, PII redaction, diagnosis prevention
- **Knowledge Graph**: Medical entity relationships
- **Multi-language**: i18n support for 6 languages

### Layer 4: Infrastructure
- Docker Compose for deployment
- Multi-service orchestration (API, DB, Redis, RAG)
- CI/CD pipeline ready

## GenAI Techniques Integrated

1. **Voice AI** - STT + TTS for accessible symptom input
2. **RAG** - Medical guidelines for evidence-based triage
3. **Guardrails** - No diagnosis, liability protection, PII redaction
4. **Multi-language** - Accessibility across 6 languages
5. **Knowledge Graph** - Entity relationships for medical concepts
6. **Content Generation** - Triage report generation

## Tech Stack

- **Frontend**: Next.js 14, Tailwind CSS, shadcn/ui, React
- **Backend**: FastAPI, Python, PostgreSQL, Redis
- **AI/ML**: OpenAI, ElevenLabs, Milvus/Milvus for RAG, NetworkX for knowledge graph
- **DevOps**: Docker, Docker Compose, GitHub Actions
- **Authentication**: JWT (JSON Web Tokens)

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend)
- PostgreSQL (if not using Docker)
- OpenAI API key (for AI features)
- ElevenLabs API key (for TTS)

## Quick Start

```bash
# 1. Clone and install
git clone <repo-url>
cd healthcare-triage
cp .env.example .env

# 2. Start infrastructure
docker-compose up -d

# 3. Wait for services to be ready
#    - API: http://localhost:8000
#    - Frontend: http://localhost:3000
#    - DB: localhost:5432

# 4. Run migrations and seed data
cd backend && python -m alembic upgrade head
python seed_database.py

# 5. Access the application
#    - Open http://localhost:3000 in your browser
#    - Select language and describe symptoms
#    - View triage results and generate reports
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET /` | Root | Welcome message |
| `POST /api/v1/triage` | Submit symptoms and get triage result |
| `POST /api/v1/auth/register` | Register new patient |
| `POST /api/v1/auth/login` | Login and get JWT token |
| `POST /api/v1/triage/report/generate` | Generate triage report |
| `GET /api/v1/health` | Health check |

## Authentication

JWT-based authentication with registration and login routes. Protected routes require valid `Bearer` token in Authorization header.

## Seed Data

Run `python seed_database.py` to populate initial medical guidelines, entities, and sample patient data for demo purposes.

## Demo

- **Demo Video**: 5-10 minute walkthrough of the system
- **Test Scenario**: Enter symptoms in English/Spanish, observe triage result, generate PDF report
- **Guardrails Test**: Verify no diagnosis claims are made, PII is redacted

## Project Structure

```
healthcare-triage/
├── backend/          # FastAPI application
│   ├── api/          # API routes
│   ├── auth/         # JWT authentication
│   ├── rag/          # Retrieval-Augmented Generation
│   ├── guardrails/   # Safety compliance
│   └── knowledge-graph/  # Medical entity graph
├── frontend/         # Next.js application
│   ├── src/components/  # UI components
│   ├── src/pages/       # Page routes
│   └── src/lib/         # Utility functions
├── docker-compose.yml  # Service orchestration
├── .env.example      # Environment variables
└── README.md         # This file
```

## Clean Git History

This project follows conventional commits and requires 15+ commits for clean history. See GIT_HISTORY.md for commit guidelines.

## Documentation

- **ARCHITECTURE**: See architecture diagram above
- **TECH STACK**: See tech stack section
- **GEN AI TECHNIQUES**: See integrated techniques section
- **API**: See API endpoints table
- **AUTH**: See authentication section
- **QUICK START**: See quick start guide