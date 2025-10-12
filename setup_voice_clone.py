#!/usr/bin/env python3
"""Setup script for voice cloning"""
import os
from audio.voice_clone import create_cloned_voice

def setup_voice():
    """Interactive setup for voice cloning"""
    print("=== Voice Cloning Setup ===\n")
    
    import getpass
    api_key = getpass.getpass("Enter your ElevenLabs API key: ").strip()
    if not api_key:
        print("❌ API key required")
        return
    
    os.environ["ELEVENLABS_API_KEY"] = api_key
    
    print("\nProvide 1-3 audio samples (WAV format, 30s-5min each)")
    audio_files = []
    
    for i in range(3):
        path = input(f"Audio sample {i+1} path (or press Enter to skip): ").strip()
        if not path:
            break
        if os.path.exists(path):
            audio_files.append(path)
        else:
            print(f"⚠️  File not found: {path}")
    
    if not audio_files:
        print("❌ At least one audio sample required")
        return
    
    name = input("\nVoice name: ").strip() or "CustomVoice"
    
    print(f"\n🔄 Creating cloned voice '{name}'...")
    try:
        voice_id = create_cloned_voice(name, audio_files)
        print(f"\n✅ Voice cloned successfully!")
        print(f"\nAdd to your .env file:")
        print(f"ELEVENLABS_API_KEY={api_key[:8]}...{api_key[-4:]}")
        print(f"ELEVENLABS_VOICE_ID={voice_id}")
        print(f"USE_VOICE_CLONE=true")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    setup_voice()
