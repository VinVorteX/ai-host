import os
import asyncio
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from config import OPENAI_API_KEY, RECORD_SECONDS
from audio.recorder import record_to_wav
from audio.stt import transcribe_with_whisper
from audio.tts import tts_with_pyttsx3  # ✅ fast local TTS for low latency
from ai.chat import ask_chatgpt_stream, get_faq_stats  # ✅ streaming chat
from utils.audio_player import check_audio_dependencies


async def process_interaction():
    """Process one full interaction cycle with real-time low-latency streaming"""
    # Record user voice
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpwav:
        wav_path = tmpwav.name

    record_to_wav(wav_path, seconds=RECORD_SECONDS)

    # Use thread pool for CPU-bound tasks
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Speech to text (Whisper)
        try:
            user_text = await asyncio.get_event_loop().run_in_executor(
                executor, transcribe_with_whisper, wav_path
            )
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            os.unlink(wav_path)
            return None

        if not user_text:
            print("❌ No speech detected.")
            os.unlink(wav_path)
            return None

        print(f"\n🎯 User question: '{user_text}'")

    # Delete temp audio asynchronously
    cleanup_task = asyncio.create_task(asyncio.to_thread(os.unlink, wav_path))

    # --- STREAMING RESPONSE PHASE ---
    print("\n🧠 Streaming AI response (real-time, low latency)...\n")
    response_chunks = []
    last_speak_time = 0.0
    speak_delay = 0.25  # small delay for smooth speech pacing

    try:
        for chunk in ask_chatgpt_stream(user_text):
            if not chunk:
                continue

            # 🧩 show text in real-time
            print(chunk, end="", flush=True)
            response_chunks.append(chunk)

            # 🗣️ speak with minimal latency
            now = time.time()
            if now - last_speak_time > speak_delay:
                await asyncio.to_thread(tts_with_pyttsx3, chunk)
                last_speak_time = now

        print("\n\n✅ Response complete!\n")

    except Exception as e:
        print(f"\n❌ Streaming error: {e}")

    await cleanup_task
    return "".join(response_chunks)


def show_faq_stats():
    """Display FAQ system statistics"""
    stats = get_faq_stats()
    print(f"\n📊 FAQ System Stats:")
    print(f"   Total FAQs: {stats['total_faqs']}")
    if stats["faq_questions"]:
        print(f"   Sample questions: {', '.join(stats['faq_questions'][:3])}...")
    else:
        print("   No FAQs found.")


async def main_loop():
    """Main voice assistant loop"""
    print("=== NextGen Supercomputing Club — Enhanced RAG AI Host ===")
    print("🚀 Real-time streaming AI with ultra-low latency response!\n")

    available_players = check_audio_dependencies()
    if not available_players:
        print("⚠️ No audio players detected. Audio playback may not work.")
        print("💡 Install: sudo apt install mpg123 ffmpeg vlc alsa-utils")
    else:
        print(f"✅ Audio players available: {', '.join(available_players)}")

    show_faq_stats()

    while True:
        print("\n" + "=" * 60)
        print("Options:")
        print("1. 🎤 Ask a question (press Enter)")
        print("2. 📊 Show FAQ stats")
        print("3. ❌ Exit")

        cmd = input("\nChoose option (1, 2, 3): ").strip()

        if cmd == "3" or cmd.lower() == "quit":
            break
        elif cmd == "2":
            show_faq_stats()
        elif cmd == "1" or cmd == "":
            await process_interaction()
        else:
            print("❌ Invalid option. Please choose 1, 2, or 3.")

    print("\n👋 Goodbye! Thank you for visiting the NextGen Supercomputing Club!")


if __name__ == "__main__":
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    try:
        import sklearn
        print("✅ Enhanced RAG system ready!")
    except ImportError:
        print("⚠️ scikit-learn not found, installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "scikit-learn"])
        print("✅ scikit-learn installed successfully!")

    asyncio.run(main_loop())
