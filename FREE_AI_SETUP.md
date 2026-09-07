# Healthcare AI Triage Assistant - Free AI Services Setup

## 🎯 **FREE AI SERVICES STACK**

We've replaced all paid AI services with **completely free alternatives**:

| Service | Previous (Paid) | New (FREE) | Free Tier Limits |
|---------|-----------------|------------|------------------|
| **LLM (Chat/Reasoning)** | OpenAI GPT-4 ($$) | **Groq** | 30 req/min, 6K tokens/min, 30K tokens/day |
| **STT (Speech-to-Text)** | OpenAI Whisper ($$) | **Groq Whisper** | 100 req/min, 25MB/file |
| **TTS (Text-to-Speech)** | ElevenLabs ($$$) | **Edge TTS** (Microsoft) | Completely FREE |
| **Real-time Audio** | Custom WebRTC | **LiveKit** | 1000 participant min/mo |
| **Embeddings** | OpenAI ($$$) | **Groq Embeddings** | Free tier |
| **Vector DB** | Pinecone ($$$) | **Milvus** (self-hosted) | FREE |

---

## 🔑 **REQUIRED FREE API KEYS**

### 1. **Groq API Key** (Primary LLM + Whisper STT + Embeddings)
- **Get it free**: https://console.groq.com/keys
- **Free tier**: 30 req/min, 6,000 tokens/min, 30,000 tokens/day
- **Models available**: 
  - `llama-3.3-70b-versatile` (best for reasoning)
  - `mixtral-8x7b-32768` (great for multilingual)
  - `gemma2-9b-it` (fast, efficient)
- **Whisper STT included**: 100 req/min, 25MB max file

### 2. **LiveKit** (Optional - Real-time Audio)
- **Cloud Free**: https://livekit.io/cloud
- **Free tier**: 1,000 participant minutes/month
- **Self-hosted**: Fully free (open source)
- Used for: Real-time STT/TTS streaming, WebRTC

### 3. **Edge TTS** (Microsoft - Completely Free)
- No API key needed!
- Built into `edge-tts` Python package
- High-quality neural voices in 6 languages
- No rate limits, no API key needed

---

## 📋 **ENVIRONMENT VARIABLES (`.env`)**

```bash
# ============================================
# FREE AI SERVICES (Replace OpenAI/ElevenLabs)
# ============================================

# Groq API Key (FREE - https://console.groq.com/keys)
# Free tier: 30 req/min, 6000 tokens/min, 30K tokens/day
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama-3.3-70b-versatile  # Best for reasoning

# LiveKit (FREE Cloud - https://livekit.io/cloud)
# Or self-hosted LiveKit (open source)
# Free tier: 1000 monthly participant minutes
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret

# Use LiveKit for STT/TTS (optional, can use Groq Whisper + Edge TTS instead)
USE_LIVEKIT_STT=false
USE_LIVEKIT_TTS=false

# Groq Whisper STT (already included in GROQ_API_KEY)
STT_SERVICE=groq

# ============================================
# OPTIONAL: Legacy/OpenAI (if you want to use them)
# ============================================
# OPENAI_API_KEY=sk-...
# ELEVENLABS_API_KEY=your-elevenlabs-key
# STT_SERVICE=openai
```

---

## 🚀 **HOW TO RUN (FREE)**

### 1. Get Free API Keys
```bash
# 1. Groq API Key (REQUIRED)
# Go to: https://console.groq.com/keys
# Create API key → Copy to .env

# 2. LiveKit (Optional - for real-time audio)
# Go to: https://livekit.io/cloud
# Create project → Copy credentials to .env
```

### 2. Run with Docker (Recommended)
```bash
git clone https://github.com/rajeshknp00-art/exceldraw.git
cd exceldraw/healthcare-triage
cp .env.example .env
# Edit .env with your GROQ_API_KEY
docker-compose up -d
```

### 3. Local Development (No Docker)
```bash
# Backend
cd healthcare-triage/backend
cp .env.example .env
# Edit .env with your keys
pip install -r requirements.txt
python main.py  # http://localhost:8000

# Frontend (separate terminal)
cd ../frontend
cp .env.example .env.local
npm install
npm run dev  # http://localhost:3000
```

---

## 🎯 **WHAT'S FREE vs WHAT NEEDS KEYS**

| Component | Free? | Needs API Key? | Notes |
|-----------|-------|----------------|-------|
| **Groq LLM** | ✅ Yes | ✅ Yes (free) | llama-3.3-70b-versatile |
| **Groq Whisper STT** | ✅ Yes | ✅ Yes (same key) | 100 req/min |
| **Groq Embeddings** | ✅ Yes | ✅ Yes (same key) | nomic-embed-text |
| **Edge TTS** | ✅ Yes | ❌ No key needed | Microsoft Edge TTS |
| **LiveKit STT/TTS** | ✅ Free tier | ✅ Yes (free tier) | Optional |
| **Milvus Vector DB** | ✅ Self-hosted | ❌ No | Docker |
| **Milvus/Pgvector** | ✅ Self-hosted | ❌ No | Docker |
| **PostgreSQL** | ✅ Free | ❌ No | Docker |
| **Redis** | ✅ Free | ❌ No | Docker |

---

## 🔧 **COST SUMMARY**

| Service | Monthly Cost | Setup Time |
|---------|-------------|------------|
| **Groq** | $0 | 2 min |
| **LiveKit Cloud** | $0 (1000 min/mo) | 3 min |
| **Edge TTS** | $0 | 0 min (built-in) |
| **Milvus/PostgreSQL/Redis** | $0 (Docker) | 0 min |
| **Total** | **$0/month** | **~5 minutes** |

---

## 🚨 **IMPORTANT NOTES**

1. **Groq Rate Limits**: 30 req/min, 6K tokens/min. For production, consider caching.
2. **Groq Whisper**: 25MB max file size, 100 req/min.
3. **Edge TTS**: No rate limits, high quality, 6 languages supported.
4. **LiveKit Free**: 1000 participant minutes/month. Self-host for unlimited.
5. **No PostgreSQL needed locally** - uses SQLite by default.
6. **No OpenAI/ElevenLabs keys needed** - completely replaced!

---

## 🚀 **QUICK START**

```bash
# 1. Get Groq API key (2 min)
# https://console.groq.com/keys

# 2. Clone & configure
git clone https://github.com/rajeshknp00-art/exceldraw.git
cd exceldraw/healthcare-triage
cp .env.example .env
# Edit .env → add GROQ_API_KEY

# 3. Run
docker-compose up -d

# 4. Test
curl http://localhost:8000/api/v1/health
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

---

## 📞 **SUPPORT**

- **Groq Docs**: https://console.groq.com/docs
- **LiveKit Docs**: https://docs.livekit.io
- **Edge TTS**: https://github.com/rany2/edge-tts
- **Project Repo**: https://github.com/rajeshknp00-art/exceldraw

---

**Total Cost: $0/month** 🎉
**All AI services completely free!**