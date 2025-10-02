# from pydub import AudioSegment
# from pydub.playback import play
# import simpleaudio as sa

# def play_audio(path):
#     """
#     Play audio file with fallback options.
    
#     Args:
#         path (str): Path to audio file
#     """
#     print("🎵 Playing audio...")
#     try:
#         audio = AudioSegment.from_file(path)
#         play(audio)
#         print("✅ Playback completed.")
#     except Exception as e:
#         print(f"❌ Pydub playback failed: {e}")
#         # Fallback to simpleaudio for wav files
#         if path.endswith('.wav'):
#             try:
#                 wave_obj = sa.WaveObject.from_wave_file(path)
#                 play_obj = wave_obj.play()
#                 play_obj.wait_done()
#                 print("✅ Playback completed with simpleaudio.")
#             except Exception as e2:
#                 print(f"❌ Simpleaudio playback failed: {e2}")

# from pydub import AudioSegment
# from pydub.playback import play
# import simpleaudio as sa
# import threading
# import time

# def play_audio_safe(path):
#     """
#     Safe audio playback with multiple fallbacks and threading.
#     """
#     print("🎵 Playing audio...")
    
#     def _play_with_pydub():
#         try:
#             audio = AudioSegment.from_file(path)
#             play(audio)
#             return True
#         except Exception as e:
#             print(f"❌ Pydub playback failed: {e}")
#             return False
    
#     def _play_with_simpleaudio():
#         try:
#             if path.endswith('.wav'):
#                 wave_obj = sa.WaveObject.from_wave_file(path)
#                 play_obj = wave_obj.play()
#                 play_obj.wait_done()
#                 return True
#             else:
#                 # Convert to WAV first
#                 audio = AudioSegment.from_file(path)
#                 with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
#                     wav_path = tmp.name
#                 audio.export(wav_path, format="wav")
#                 wave_obj = sa.WaveObject.from_wave_file(wav_path)
#                 play_obj = wave_obj.play()
#                 play_obj.wait_done()
#                 os.unlink(wav_path)
#                 return True
#         except Exception as e:
#             print(f"❌ Simpleaudio playback failed: {e}")
#             return False
    
#     def _play_with_system():
#         try:
#             import subprocess
#             if path.endswith('.mp3'):
#                 subprocess.run(['mpg123', '-q', path], check=True)
#             else:
#                 subprocess.run(['aplay', path], check=True)
#             return True
#         except Exception as e:
#             print(f"❌ System audio playback failed: {e}")
#             return False
    
#     # Try playback methods in order
#     methods = [_play_with_simpleaudio, _play_with_pydub, _play_with_system]
    
#     for method in methods:
#         try:
#             if method():
#                 print("✅ Playback completed successfully.")
#                 return
#         except Exception as e:
#             print(f"❌ {method.__name__} failed: {e}")
#             continue
    
#     print("❌ All audio playback methods failed.")
#     print("💡 Response was generated but couldn't play audio.")

# # Alias for backward compatibility
# play_audio = play_audio_safe

import os
import tempfile
import subprocess
import sys
from pydub import AudioSegment

def play_audio(path):
    """
    Robust audio playback with multiple fallback methods.
    This is the safest approach for Linux systems.
    """
    print("🎵 Playing audio...")
    
    # Method 1: Try system audio players (most reliable)
    if try_system_players(path):
        print("✅ Playback completed with system player.")
        return
    
    # Method 2: Try simpleaudio for WAV files
    if try_simpleaudio(path):
        print("✅ Playback completed with simpleaudio.")
        return
    
    # Method 3: Convert to WAV and try again
    if convert_and_play(path):
        print("✅ Playback completed after conversion.")
        return
    
    # Final fallback
    print("❌ All audio playback methods failed.")
    print("💡 Audio was generated but couldn't be played.")

def try_system_players(path):
    """Try using system audio players - most reliable on Linux"""
    try:
        if path.endswith('.mp3'):
            # Try mpg123 first (lightweight MP3 player)
            result = subprocess.run(['which', 'mpg123'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['mpg123', '-q', path], check=True)
                return True
            
            # Try ffplay (from ffmpeg)
            result = subprocess.run(['which', 'ffplay'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['ffplay', '-autoexit', '-nodisp', path], check=True)
                return True
            
            # Try vlc
            result = subprocess.run(['which', 'cvlc'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['cvlc', '--play-and-exit', path], check=True)
                return True
        
        else:  # For WAV files
            # Try aplay (ALSA player)
            result = subprocess.run(['which', 'aplay'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['aplay', path], check=True)
                return True
            
            # Try paplay (PulseAudio player)
            result = subprocess.run(['which', 'paplay'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['paplay', path], check=True)
                return True
            
            # Try play (from sox)
            result = subprocess.run(['which', 'play'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['play', path], check=True)
                return True
        
        return False
        
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"❌ System player error: {e}")
        return False

def try_simpleaudio(path):
    """Try using simpleaudio (only for WAV files)"""
    try:
        # Only attempt for WAV files
        if not path.endswith('.wav'):
            return False
            
        import simpleaudio as sa
        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        return True
        
    except ImportError:
        print("💡 simpleaudio not available")
        return False
    except Exception as e:
        print(f"❌ simpleaudio error: {e}")
        return False

def convert_and_play(path):
    """Convert audio to WAV and try to play"""
    try:
        # Convert to WAV using pydub
        audio = AudioSegment.from_file(path)
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            wav_path = tmp_file.name
        
        # Export as WAV
        audio.export(wav_path, format='wav')
        
        # Try system players with the WAV file
        if try_system_players(wav_path):
            # Clean up temporary file
            os.unlink(wav_path)
            return True
        
        # Try simpleaudio with the WAV file
        if try_simpleaudio(wav_path):
            os.unlink(wav_path)
            return True
        
        # Clean up if all failed
        os.unlink(wav_path)
        return False
        
    except Exception as e:
        print(f"❌ Audio conversion error: {e}")
        # Clean up temporary file if it was created
        if 'wav_path' in locals() and os.path.exists(wav_path):
            os.unlink(wav_path)
        return False

def check_audio_dependencies():
    """Check what audio players are available on the system"""
    players = ['mpg123', 'ffplay', 'cvlc', 'aplay', 'paplay', 'play']
    available = []
    
    for player in players:
        result = subprocess.run(['which', player], capture_output=True)
        if result.returncode == 0:
            available.append(player)
    
    print(f"🎵 Available audio players: {available}")
    return available