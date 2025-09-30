from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa

def play_audio(path):
    """
    Play audio file with fallback options.
    
    Args:
        path (str): Path to audio file
    """
    print("🎵 Playing audio...")
    try:
        audio = AudioSegment.from_file(path)
        play(audio)
        print("✅ Playback completed.")
    except Exception as e:
        print(f"❌ Pydub playback failed: {e}")
        # Fallback to simpleaudio for wav files
        if path.endswith('.wav'):
            try:
                wave_obj = sa.WaveObject.from_wave_file(path)
                play_obj = wave_obj.play()
                play_obj.wait_done()
                print("✅ Playback completed with simpleaudio.")
            except Exception as e2:
                print(f"❌ Simpleaudio playback failed: {e2}")