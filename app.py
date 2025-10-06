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

app = Flask(__name__)
CORS(app)

executor = ThreadPoolExecutor(max_workers=3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_audio():
    """Process audio from web interface"""
    try:
        audio_data = request.json.get('audio')
        if not audio_data:
            return jsonify({'error': 'No audio data'}), 400
        
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_bytes)
            wav_path = f.name
        
        # Transcribe
        user_text = transcribe_with_whisper(wav_path)
        os.unlink(wav_path)
        
        if not user_text:
            return jsonify({'error': 'No speech detected'}), 400
        
        # Get response
        response_text = ask_chatgpt(user_text)
        
        # Generate TTS
        tts_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        asyncio.run(tts_with_openai(response_text, tts_path))
        
        # Read audio file
        with open(tts_path, 'rb') as f:
            audio_response = base64.b64encode(f.read()).decode()
        
        os.unlink(tts_path)
        
        return jsonify({
            'transcript': user_text,
            'response': response_text,
            'audio': f'data:audio/mp3;base64,{audio_response}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text', methods=['POST'])
def process_text():
    """Process text input"""
    try:
        user_text = request.json.get('text')
        if not user_text:
            return jsonify({'error': 'No text provided'}), 400
        
        response_text = ask_chatgpt(user_text)
        
        # Generate TTS
        tts_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        asyncio.run(tts_with_openai(response_text, tts_path))
        
        with open(tts_path, 'rb') as f:
            audio_response = base64.b64encode(f.read()).decode()
        
        os.unlink(tts_path)
        
        return jsonify({
            'response': response_text,
            'audio': f'data:audio/mp3;base64,{audio_response}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
