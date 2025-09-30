# #!/usr/bin/env python3
# """
# NextGen Supercomputing Club AI Host - Modular Version
# Main entry point for the application
# """

# import os
# import asyncio
# import tempfile
# from config import OPENAI_API_KEY
# from audio.recorder import record_to_wav
# from audio.stt import transcribe_with_whisper
# from audio.tts import tts_with_openai, tts_with_pyttsx3
# from ai.chat import ask_chatgpt
# from utils.audio_player import play_audio

# async def process_interaction():
#     """
#     Process one complete interaction cycle:
#     Record → Transcribe → Generate Response → Speak
#     """
#     # Record audio
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpwav:
#         wav_path = tmpwav.name
    
#     record_to_wav(wav_path)
    
#     # Transcribe
#     try:
#         user_text = transcribe_with_whisper(wav_path)
#     except Exception as e:
#         print(f"❌ Transcription failed: {e}")
#         return None
    
#     if not user_text:
#         print("❌ No speech detected.")
#         return None
    
#     # Generate response
#     response_text = ask_chatgpt(user_text)
    
#     # Generate TTS
#     out_audio = None
#     try:
#         # Try OpenAI TTS first
#         tts_out = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
#         await tts_with_openai(response_text, tts_out)
#         out_audio = tts_out
#     except Exception as e:
#         print("❌ OpenAI TTS failed, trying pyttsx3...")
#         try:
#             tts_out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
#             tts_with_pyttsx3(response_text, tts_out)
#             out_audio = tts_out
#         except Exception as e2:
#             print(f"❌ All TTS methods failed: {e2}")
#             print("📝 Response text:")
#             print(response_text)
#             return response_text
    
#     # Play audio
#     if out_audio:
#         play_audio(out_audio)
    
#     # Cleanup
#     try:
#         os.unlink(wav_path)
#         if out_audio and os.path.exists(out_audio):
#             os.unlink(out_audio)
#     except:
#         pass  # Cleanup is best effort
    
#     return response_text

# async def main_loop():
#     """
#     Main application loop
#     """
#     print("=== NextGen Supercomputing Club — Inauguration AI Host ===")
#     print("Press Enter to record a question (or type 'quit' to exit).")
    
#     while True:
#         cmd = input("\n🎤 Press Enter to record (or type 'quit'): ").strip().lower()
#         if cmd == 'quit':
#             break
        
#         await process_interaction()
    
#     print("\n👋 Goodbye! Thank you for visiting the NextGen Supercomputing Club!")

# if __name__ == "__main__":
#     # Check API key
#     if not OPENAI_API_KEY:
#         raise RuntimeError("OPENAI_API_KEY environment variable not set")
    
#     asyncio.run(main_loop())


import os
import asyncio
import tempfile
from config import OPENAI_API_KEY
from audio.recorder import record_to_wav
from audio.stt import transcribe_with_whisper
from audio.tts import tts_with_openai, tts_with_pyttsx3
from ai.chat import ask_chatgpt, add_new_faq, get_faq_stats
from utils.audio_player import play_audio

async def process_interaction():
    """Process one complete interaction cycle"""
    # Record audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpwav:
        wav_path = tmpwav.name
    
    record_to_wav(wav_path)
    
    # Transcribe
    try:
        user_text = transcribe_with_whisper(wav_path)
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return None
    
    if not user_text:
        print("❌ No speech detected.")
        return None
    
    print(f"🎯 User question: '{user_text}'")
    
    # Generate response (now uses enhanced RAG)
    response_text = ask_chatgpt(user_text)
    
    # Generate TTS
    out_audio = None
    try:
        # Try OpenAI TTS first
        tts_out = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        await tts_with_openai(response_text, tts_out)
        out_audio = tts_out
    except Exception as e:
        print("❌ OpenAI TTS failed, trying pyttsx3...")
        try:
            tts_out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            tts_with_pyttsx3(response_text, tts_out)
            out_audio = tts_out
        except Exception as e2:
            print(f"❌ All TTS methods failed: {e2}")
            print("📝 Response text:")
            print(response_text)
            return response_text
    
    # Play audio
    if out_audio:
        play_audio(out_audio)
    
    # Cleanup
    try:
        os.unlink(wav_path)
        if out_audio and os.path.exists(out_audio):
            os.unlink(out_audio)
    except:
        pass
    
    return response_text

def show_faq_stats():
    """Display FAQ system statistics"""
    stats = get_faq_stats()
    print(f"\n📊 FAQ System Stats:")
    print(f"   Total FAQs: {stats['total_faqs']}")
    print(f"   Questions: {', '.join(stats['faq_questions'][:3])}..." if stats['faq_questions'] else "   No FAQs")

async def main_loop():
    """Main application loop"""
    print("=== NextGen Supercomputing Club — Enhanced RAG AI Host ===")
    print("🚀 Now with smart FAQ matching using TF-IDF!")
    show_faq_stats()
    
    while True:
        print("\n" + "="*60)
        print("Options:")
        print("1. 🎤 Ask a question (press Enter)")
        print("2. 📊 Show FAQ stats")
        print("3. ❌ Exit")
        
        cmd = input("\nChoose option (1, 2, 3): ").strip()
        
        if cmd == '3' or cmd == 'quit':
            break
        elif cmd == '2':
            show_faq_stats()
            continue
        elif cmd == '1' or cmd == '':
            await process_interaction()
        else:
            print("❌ Invalid option. Please choose 1, 2, or 3.")
    
    print("\n👋 Goodbye! Thank you for visiting the NextGen Supercomputing Club!")

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    
    # Check if scikit-learn is available for TF-IDF
    try:
        import sklearn
        print("✅ Enhanced RAG system ready!")
    except ImportError:
        print("❌ scikit-learn not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "scikit-learn"])
        print("✅ scikit-learn installed!")
    
    asyncio.run(main_loop())