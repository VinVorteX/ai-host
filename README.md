# 🤖 Riva - NextGen AI Assistant

Riva is an intelligent voice-powered AI assistant with RAG (Retrieval-Augmented Generation), voice cloning, and ultra-low latency. Built for the NextGen Supercomputing Club.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎤 **Voice Interaction** - Speak naturally, get instant AI responses
- 🧠 **Smart FAQ System** - TF-IDF powered semantic matching with caching
- 🗣️ **Voice Cloning** - Clone any voice using ElevenLabs API
- ⚡ **Ultra-Low Latency** - Optimized pipeline with concurrent processing
- 🌐 **Cross-Platform** - Works on Windows, Linux, and macOS
- 🎨 **JARVIS-Style UI** - Circular wave animations with React
- 🔄 **Fallback Systems** - Multiple TTS/STT options for reliability
- 🚀 **FastAPI Backend** - High-performance async API

## 🎯 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for React frontend)
- OpenAI API key
- Microphone access

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd ai-host

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Setup environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY2
```

### Run Development Mode

```bash
# Start both backend and frontend
./start_dev.sh

# Frontend: http://localhost:3000
# Backend:  http://localhost:5000
# API Docs: http://localhost:5000/docs
```

### Run Production Mode

```bash
# Build React frontend
cd frontend && npm run build && cd ..

# Start FastAPI server
python start.py
# Open http://localhost:5000
```

## 🎨 Web Interface

Modern React frontend with JARVIS-style animations:
- **⚛️ React 18** with Hooks and modern patterns
- **⚡ Vite** for lightning-fast development
- **🎯 JARVIS-style circular waves** - Blue (idle), Red (recording), Green (processing)
- **💫 Glowing "RIVA" text** in center
- **🎤 Voice recording** with visual feedback
- **🔊 Real-time streaming** responses
- **📱 Fully responsive** design

## 🔧 Configuration

Edit `config.py` or `.env`:

```env
# Required
OPENAI_API_KEY2=your_openai_key

# Optional - Voice Cloning
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id
USE_VOICE_CLONE=true

# Performance Tuning
RECORD_SECONDS=3
MAX_TOKENS=100
TEMPERATURE=0.2
```

## 🗣️ Voice Cloning Setup

```bash
# Interactive setup
python setup_voice_clone.py

# Or manually configure in .env
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=voice_id
USE_VOICE_CLONE=true
```

See [VOICE_CLONE_SETUP.md](VOICE_CLONE_SETUP.md) for details.

## 📁 Project Structure

```
ai-host/
├── ai/                 # AI & RAG logic
│   ├── chat.py        # ChatGPT integration
│   └── knowledge.py   # FAQ system with TF-IDF
├── audio/             # Audio processing
│   ├── recorder.py    # Microphone recording
│   ├── stt.py         # Speech-to-text
│   ├── tts.py         # Text-to-speech
│   └── voice_clone.py # Voice cloning
├── frontend/          # React frontend
│   ├── src/
│   │   ├── App.jsx    # Main app with JARVIS UI
│   │   └── styles/    # CSS files
│   ├── package.json
│   └── vite.config.js
├── utils/             # Utilities
│   └── audio_player.py # Cross-platform audio playback
├── app.py            # FastAPI application
├── start.py          # Production startup script
├── start_dev.sh      # Development startup script
└── config.py         # Configuration
```

## 🎯 Usage

### Web Mode

1. Open browser to `http://localhost:3000` (dev) or `http://localhost:5000` (prod)
2. Click the center RIVA button
3. Speak your question
4. Get instant AI response with voice

### CLI Mode

```bash
python main.py

# Options:
# 1. Ask a question (voice)
# 2. Show FAQ stats
# 3. Exit
```

### API Mode

```python
from ai.chat import ask_chatgpt

response = ask_chatgpt("What is supercomputing?")
print(response)
```

## 🔊 Audio Requirements

### Windows
- Built-in audio support ✅

### macOS
- Built-in `afplay` ✅

### Linux
Install audio players:
```bash
# Debian/Ubuntu
sudo apt install mpg123 ffmpeg alsa-utils

# Fedora/RHEL
sudo dnf install mpg123 ffmpeg alsa-utils

# Arch
sudo pacman -S mpg123 ffmpeg alsa-utils
```

## ⚡ Performance Optimizations

- **FastAPI** - 40-60% faster than Flask
- **3-second recording** for quick responses
- **gpt-4o-mini** for 3x faster responses
- **Connection pooling** for API calls
- **Concurrent processing** with ThreadPoolExecutor
- **FAQ caching** for instant repeated queries
- **Reduced token limits** for faster generation

## 🛠️ Troubleshooting

### No audio playback
```bash
# Check available players
python -c "from utils.audio_player import check_audio_dependencies; check_audio_dependencies()"

# Install missing dependencies (Linux)
sudo apt install mpg123 ffmpeg
```

### Microphone not working
```bash
# Test recording
python -c "from audio.recorder import record_to_wav; record_to_wav('test.wav', 3)"
```

### API errors
- Verify API key in `.env`
- Check internet connection
- Ensure sufficient API credits

## 📊 FAQ System

The assistant uses TF-IDF semantic matching to find relevant FAQs before querying ChatGPT, reducing latency and API costs.

Add custom FAQs:
```python
from ai.chat import add_new_faq

add_new_faq(
    "What are office hours?",
    "Office hours are Monday-Friday, 2-4 PM in Room 301."
)
```

## 🚀 API Documentation

FastAPI provides automatic interactive API docs:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Whisper
- ElevenLabs for voice cloning
- FastAPI for high-performance backend
- React for modern frontend
- NextGen Supercomputing Club

## 📧 Support

- Email: nextgenclub@university.edu
- Twitter: @NextGenHPC
- Issues: GitHub Issues

---

**Built with ❤️ by NextGen Supercomputing Club**
