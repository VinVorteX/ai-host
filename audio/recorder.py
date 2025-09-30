import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from config import SAMPLE_RATE

def record_to_wav(filename, seconds=6, sample_rate=SAMPLE_RATE):
    """
    Record audio from microphone and save as WAV file.
    
    Args:
        filename (str): Path to save the recording
        seconds (int): Duration of recording
        sample_rate (int): Audio sample rate
    
    Returns:
        str: Path to the saved audio file
    """
    print(f"🎤 Recording for {seconds} seconds... Speak now.")
    recording = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    wavfile.write(filename, sample_rate, recording)
    print(f"✅ Recording saved to {filename}")
    return filename