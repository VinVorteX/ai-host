from openai import OpenAI
from config import OPENAI_API_KEY, WHISPER_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_with_whisper(wav_path):
    """
    Transcribe audio file to text using OpenAI Whisper.
    
    Args:
        wav_path (str): Path to audio file
    
    Returns:
        str: Transcribed text
    """
    print("🔄 Transcribing with OpenAI Whisper...")
    try:
        with open(wav_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file
            )
        text = transcription.text.strip()
        print(f"📝 Transcript: {text}")
        return text
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        raise