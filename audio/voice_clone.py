import os
import requests
from typing import Optional

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

def clone_voice_tts(text: str, output_path: str, voice_id: Optional[str] = None) -> str:
    """Generate TTS using ElevenLabs voice cloning"""
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not set")
    
    voice_id = voice_id or ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM"  # Default voice
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text[:350],
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.7
        }
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    return output_path

def create_cloned_voice(name: str, audio_files: list) -> str:
    """Create a new cloned voice from audio samples"""
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not set")
    
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    files = [('files', open(f, 'rb')) for f in audio_files]
    data = {'name': name}
    
    response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
    response.raise_for_status()
    
    for _, f in files:
        f.close()
    
    return response.json()['voice_id']
