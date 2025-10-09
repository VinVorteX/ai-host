from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import asyncio
import tempfile
import os
import base64
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# --- IMPORTANT: Import the new streaming function ---
from ai.chat import ask_chatgpt_stream
from audio.stt import transcribe_with_whisper
from audio.tts import tts_with_openai

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# --- Use a more robust cache for audio data ---
# This will store the generated base64 audio string
audio_cache = {}

# Thread pool for background tasks
executor = ThreadPoolExecutor(max_workers=4)

def generate_and_cache_audio(text: str, cache_key: str):
    """
    Generates TTS audio in a background thread and stores it in the cache.
    """
    try:
        print(f"INFO: Starting TTS generation for cache key: {cache_key}")
        # Need to create a new event loop for a new thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tts_path = f.name
        
        loop.run_until_complete(tts_with_openai(text, tts_path))
        
        with open(tts_path, 'rb') as f:
            audio_response = base64.b64encode(f.read()).decode()
        os.unlink(tts_path)
        
        audio_cache[cache_key] = f'data:audio/mp3;base64,{audio_response}'
        print(f"INFO: TTS generation complete for cache key: {cache_key}")
    except Exception as e:
        print(f"ERROR: Failed to generate TTS audio: {e}")
        audio_cache[cache_key] = "error"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Receives audio data, transcribes it, and returns the transcript.
    This is a fast, synchronous endpoint.
    """
    try:
        audio_data = request.json.get('audio')
        if not audio_data:
            return jsonify({'error': 'No audio data provided'}), 400
        
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_bytes)
            wav_path = f.name
        
        user_text = transcribe_with_whisper(wav_path)
        os.unlink(wav_path)
        
        if not user_text:
            return jsonify({'error': 'No speech detected in audio'}), 400
            
        return jsonify({'transcript': user_text})

    except Exception as e:
        print(f"ERROR: Transcription failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/text_stream', methods=['POST'])
def process_text_stream():
    """
    Processes text input, streams the text response, and generates audio in the background.
    """
    user_text = request.json.get('text')
    if not user_text:
        return Response("No text provided", status=400)
    
    cache_key = user_text.lower().strip()

    def text_and_audio_generator():
        # 1. Stream the text response to the client
        full_response_text = []
        for chunk in ask_chatgpt_stream(user_text):
            yield chunk
            full_response_text.append(chunk)
        
        # 2. Once text is complete, start audio generation in the background
        final_text = "".join(full_response_text)
        task = partial(generate_and_cache_audio, text=final_text, cache_key=cache_key)
        executor.submit(task)

    return Response(text_and_audio_generator(), mimetype='text/plain')

@app.route('/api/get_audio/<cache_key>', methods=['GET'])
def get_audio(cache_key: str):
    """
    Endpoint for the client to fetch the generated audio.
    """
    cache_key = cache_key.lower().strip()
    audio_data = audio_cache.get(cache_key)

    if audio_data:
        if audio_data != "processing":
             del audio_cache[cache_key]
        return jsonify({'status': 'ready', 'audio': audio_data})
    else:
        # If audio is not ready, mark it as processing for subsequent checks
        audio_cache[cache_key] = "processing"
        return jsonify({'status': 'processing'}), 202

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

