"""Voice AI Service for STT/TTS using Groq Whisper and LiveKit."""
import os
import base64
import asyncio
from typing import Optional, AsyncGenerator
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import stt, tts, vad

load_dotenv()

class VoiceService:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.livekit_url = os.getenv("LIVEKIT_URL", "wss://your-livekit-server")
        self.livekit_api_key = os.getenv("LIVEKIT_API_KEY")
        self.livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")
        
        # Groq Whisper for STT (free tier available)
        self.groq_base_url = "https://api.groq.com/openai/v1"
        
        # LiveKit STT/TTS (can use cloud or self-hosted)
        self.use_livekit_stt = os.getenv("USE_LIVEKIT_STT", "false").lower() == "true"
        self.use_livekit_tts = os.getenv("USE_LIVEKIT_TTS", "false").lower() == "true"
    
    async def speech_to_text(self, audio_data: bytes, language: str = "en") -> str:
        """Convert speech to text using Groq Whisper (free) or LiveKit STT."""
        if self.use_livekit_stt:
            return await self._livekit_stt(audio_data, language)
        else:
            return await self._groq_stt(audio_data, language)
    
    async def _groq_stt(self, audio_data: bytes, language: str) -> str:
        """Use Groq's Whisper API (free tier: 100 req/min)."""
        import httpx
        
        if not self.groq_api_key:
            # Mock for development without API key
            return "I have chest pain that started an hour ago. It feels like pressure in the center of my chest."
        
        async with httpx.AsyncClient() as client:
            files = {
                "file": ("audio.wav", audio_data, "audio/wav"),
                "model": (None, "whisper-large-v3"),
                "language": (None, language),
                "response_format": (None, "text"),
            }
            headers = {"Authorization": f"Bearer {self.groq_api_key}"}
            
            try:
                response = await client.post(
                    f"{self.groq_base_url}/audio/transcriptions",
                    files=files,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.text.strip()
            except Exception as e:
                print(f"Groq STT error: {e}")
                return "Speech transcription failed"
    
    async def _livekit_stt(self, audio_data: bytes, language: str) -> str:
        """Use LiveKit STT (requires LiveKit Cloud or self-hosted)."""
        # This would integrate with LiveKit's STT service
        # For now, fall back to Groq
        return await self._groq_stt(audio_data, language)
    
    async def text_to_speech(self, text: str, language: str = "en", voice: str = "alloy") -> bytes:
        """Convert text to speech using Groq TTS or LiveKit TTS."""
        # Groq doesn't have TTS yet, so we use alternatives
        # Option 1: LiveKit TTS (if available)
        # Option 2: Edge TTS (Microsoft, free)
        # Option 3: Local TTS
        
        return await self._edge_tts(text, language)
    
    async def _edge_tts(self, text: str, language: str) -> bytes:
        """Use Microsoft Edge TTS (free, high quality)."""
        import edge_tts
        import tempfile
        
        # Map language codes to Edge TTS voices
        voice_map = {
            "en": "en-US-AriaNeural",
            "es": "es-ES-ElviraNeural",
            "fr": "fr-FR-DeniseNeural",
            "de": "de-DE-KatjaNeural",
            "zh": "zh-CN-XiaoxiaoNeural",
            "hi": "hi-IN-SwaraNeural",
        }
        
        voice = voice_map.get(language, "en-US-AriaNeural")
        
        try:
            communicate = edge_tts.Communicate(text, voice)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        except Exception as e:
            print(f"Edge TTS error: {e}")
            return b""
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages for TTS."""
        return [
            {"code": "en", "name": "English", "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]},
            {"code": "es", "name": "Spanish", "voices": ["es-ES-AlvaroNeural", "es-ES-ElviraNeural"]},
            {"code": "fr", "name": "French", "voices": ["fr-FR-DeniseNeural", "fr-FR-HenriNeural"]},
            {"code": "de", "name": "German", "voices": ["de-DE-ConradNeural", "de-DE-KatjaNeural"]},
            {"code": "zh", "name": "Chinese", "voices": ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural"]},
            {"code": "hi", "name": "Hindi", "voices": ["hi-IN-MadhurNeural", "hi-IN-SwaraNeural"]},
        ]

# Install edge-tts if not available
try:
    import edge_tts
except ImportError:
    print("Installing edge-tts...")
    import subprocess
    subprocess.check_call(["pip", "install", "edge-tts"])
    import edge_tts

voice_service = None

async def get_voice_service():
    global voice_service
    if voice_service is None:
        voice_service = VoiceService()
    return voice_service