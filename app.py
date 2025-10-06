from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor
from audio.stt import transcribe_with_whisper
from audio.tts import tts_with_openai
from ai.chat import ask_chatgpt
import base64
from functools import lru_cache

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

executor = ThreadPoolExecutor(max_workers=4)

# Simple response cache
response_cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/api/process', methods=['POST'])
def process_audio():
    """Process audio from web interface with parallel execution"""
    try:
        audio_data = request.json.get('audio')
        if not audio_data:
            return jsonify({'error': 'No audio data'}), 400
        
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_bytes)
            wav_path = f.name
        
        # Transcribe
        user_text = executor.submit(transcribe_with_whisper, wav_path).result()
        os.unlink(wav_path)
        
        if not user_text:
            return jsonify({'error': 'No speech detected'}), 400
        
        # Check cache
        cache_key = user_text.lower().strip()
        if cache_key in response_cache:
            return jsonify(response_cache[cache_key])
        
        # Get response and generate TTS in parallel
        response_future = executor.submit(ask_chatgpt, user_text)
        response_text = response_future.result()
        
        tts_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        asyncio.run(tts_with_openai(response_text, tts_path))
        
        with open(tts_path, 'rb') as f:
            audio_response = base64.b64encode(f.read()).decode()
        os.unlink(tts_path)
        
        result = {
            'transcript': user_text,
            'response': response_text,
            'audio': f'data:audio/mp3;base64,{audio_response}'
        }
        
        # Cache result
        if len(response_cache) < 50:
            response_cache[cache_key] = result
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text', methods=['POST'])
def process_text():
    """Process text input with caching"""
    try:
        user_text = request.json.get('text')
        if not user_text:
            return jsonify({'error': 'No text provided'}), 400
        
        cache_key = user_text.lower().strip()
        if cache_key in response_cache:
            return jsonify(response_cache[cache_key])
        
        response_text = executor.submit(ask_chatgpt, user_text).result()
        
        tts_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        asyncio.run(tts_with_openai(response_text, tts_path))
        
        with open(tts_path, 'rb') as f:
            audio_response = base64.b64encode(f.read()).decode()
        os.unlink(tts_path)
        
        result = {
            'response': response_text,
            'audio': f'data:audio/mp3;base64,{audio_response}'
        }
        
        if len(response_cache) < 50:
            response_cache[cache_key] = result
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
