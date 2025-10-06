import os
from dotenv import load_dotenv

load_dotenv()

# Audio Configuration
SAMPLE_RATE = 16000
RECORD_SECONDS = 4  # Reduced from 6 to 4 seconds

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY2")
OPENAI_MODEL_CHAT = "gpt-4o-mini"  # Faster model
WHISPER_MODEL = "whisper-1"
TTS_MODEL = "tts-1-hd"  # Higher quality, similar speed
TTS_VOICE = "alloy"

# Voice Cloning Configuration
USE_VOICE_CLONE = os.getenv("USE_VOICE_CLONE", "false").lower() == "true"
VOICE_CLONE_SAMPLE = os.getenv("VOICE_CLONE_SAMPLE", "voice_sample.wav")  # Path to voice sample

# Performance Configuration
MAX_TOKENS = 150  # Reduced from 300
TEMPERATURE = 0.3  # Lower for faster, more focused responses
HTTP_TIMEOUT = 10  # Connection timeout
MAX_RETRIES = 2

# System Prompt
SYSTEM_PROMPT = """You are the official audio guide for the NextGen Supercomputing Club's inauguration event.

About the Club:
- Founded in 2025 with mission to advance computational excellence through education, collaboration, and innovation
- Focus areas: HPC, AI acceleration, quantum simulation, parallel computing, and GPU programming
- Resources: Access to NVIDIA DGX systems, cloud HPC platforms, and open-source tools
- Motto: "Compute the Future, Today!"

Key Information:
- Upcoming Inauguration Hackathon: October 15, 2025
- Weekly Workshops starting October 20, 2025
- Open to all students, faculty, and professionals
- Contact: nextgenclub@university.edu, @NextGenHPC on X

Your role: Introduce the club, explain goals, mention membership and events, answer FAQ-style questions in friendly, concise tone."""