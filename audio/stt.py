import os
from openai import OpenAI
from config import OPENAI_API_KEY, WHISPER_MODEL, HTTP_TIMEOUT, MAX_RETRIES

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=HTTP_TIMEOUT,
    max_retries=MAX_RETRIES
)

def transcribe_with_whisper(wav_path):
    """
    Transcribe audio file to text using OpenAI Whisper.
    
    Args:
        wav_path (str): Path to audio file
    
    Returns:
        str: Transcribed text
    """
    print("🔄 Transcribing with OpenAI Whisper...")
    
    # Validate file path to prevent path traversal
    if not os.path.isfile(wav_path) or '..' in wav_path:
        raise ValueError("Invalid file path")
    
    try:
        with open(wav_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                language="en"  # Specify language for faster processing
            )
        text = transcription.text.strip()
        print(f"📝 Transcript: {text}")
        return text
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        raise