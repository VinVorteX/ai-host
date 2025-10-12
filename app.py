from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import tempfile
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import uvicorn

from ai.chat import ask_chatgpt_stream
from audio.stt import transcribe_with_whisper
from audio.tts import tts_with_openai

app = FastAPI(title="Riva AI Assistant", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Serve React build
try:
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
except:
    pass  # Dev mode

# Thread pool for CPU-bound tasks
executor = ThreadPoolExecutor(max_workers=2)

# Audio cache
audio_cache = {}

# Pydantic models
class AudioRequest(BaseModel):
    audio: str

class TextRequest(BaseModel):
    text: str

@app.get("/")
async def index():
    try:
        return FileResponse("frontend/dist/index.html")
    except:
        return {"message": "Run: cd frontend && npm run build"}

@app.get("/favicon.ico")
async def favicon():
    return {"status": "ok"}

@app.post("/api/transcribe")
async def transcribe_audio(request: AudioRequest):
    try:
        if not request.audio:
            raise HTTPException(status_code=400, detail="No audio data provided")
        
        audio_bytes = base64.b64decode(request.audio.split(',')[1])
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_bytes)
            wav_path = f.name
        
        # Run transcription in thread pool
        loop = asyncio.get_event_loop()
        user_text = await loop.run_in_executor(executor, transcribe_with_whisper, wav_path)
        
        try:
            os.unlink(wav_path)
        except:
            pass
        
        if not user_text:
            raise HTTPException(status_code=400, detail="No speech detected")
            
        return {"transcript": user_text}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Transcription error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

async def generate_and_cache_audio(text: str, cache_key: str):
    """Generate TTS audio in background"""
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tts_path = f.name
        
        await tts_with_openai(text, tts_path)
        
        with open(tts_path, 'rb') as f:
            audio_response = base64.b64encode(f.read()).decode()
        
        os.unlink(tts_path)
        audio_cache[cache_key] = f'data:audio/mp3;base64,{audio_response}'
        
    except Exception as e:
        print(f"TTS Error: {e}")
        audio_cache[cache_key] = "error"

@app.post("/api/text_stream")
async def process_text_stream(request: TextRequest):
    if not request.text or len(request.text) > 1000:
        raise HTTPException(status_code=400, detail="Invalid text")
    
    cache_key = request.text.lower().strip()
    
    async def stream_generator():
        full_response = []
        
        # Stream text response
        for chunk in ask_chatgpt_stream(request.text):
            yield chunk
            full_response.append(chunk)
        
        # Start audio generation in background
        final_text = "".join(full_response)
        asyncio.create_task(generate_and_cache_audio(final_text, cache_key))
    
    return StreamingResponse(stream_generator(), media_type="text/plain")

@app.get("/api/get_audio/{cache_key}")
async def get_audio(cache_key: str):
    cache_key = cache_key.lower().strip()
    audio_data = audio_cache.get(cache_key)
    
    if audio_data and audio_data != "processing":
        audio_cache.pop(cache_key, None)  # Clean up
        return {"status": "ready", "audio": audio_data}
    elif not audio_data:
        audio_cache[cache_key] = "processing"
        return {"status": "processing"}
    else:
        return {"status": "processing"}

if __name__ == "__main__":
    print("✅ Loaded FAQs")
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=False,
        workers=1,
        log_level="info"
    )