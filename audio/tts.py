import asyncio
import pyttsx3
from openai import OpenAI
from config import OPENAI_API_KEY, TTS_MODEL, TTS_VOICE

client = OpenAI(api_key=OPENAI_API_KEY)

async def tts_with_openai(text, out_path):
    """
    Generate speech from text using OpenAI TTS.
    
    Args:
        text (str): Text to convert to speech
        out_path (str): Path to save audio file
    
    Returns:
        str: Path to saved audio file
    """
    print("🔊 Generating TTS via OpenAI...")
    try:
        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text
        )
        response.stream_to_file(out_path)
        print(f"✅ TTS saved to {out_path}")
        return out_path
    except Exception as e:
        print(f"❌ OpenAI TTS failed: {e}")
        raise

def tts_with_pyttsx3(text, out_path):
    """
    Generate speech from text using pyttsx3 (offline fallback).
    
    Args:
        text (str): Text to convert to speech
        out_path (str): Path to save audio file
    
    Returns:
        str: Path to saved audio file
    """
    print("🔊 Generating TTS via pyttsx3...")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.8)
        
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        engine.save_to_file(text, out_path)
        engine.runAndWait()
        print(f"✅ Pyttsx3 TTS saved to {out_path}")
        return out_path
    except Exception as e:
        print(f"❌ Pyttsx3 TTS failed: {e}")
        raise