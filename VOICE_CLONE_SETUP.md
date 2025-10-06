# Voice Cloning Setup

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install elevenlabs requests
   ```

2. **Get ElevenLabs API key:**
   - Sign up at https://elevenlabs.io
   - Get your API key from settings

3. **Option A - Use existing voice:**
   Add to `.env`:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ELEVENLABS_VOICE_ID=voice_id_here
   USE_VOICE_CLONE=true
   ```

4. **Option B - Clone a new voice:**
   ```bash
   python setup_voice_clone.py
   ```
   - Provide 1-3 audio samples (WAV, 30s-5min each)
   - Script will output the config for your `.env`

## Usage

Voice cloning activates automatically when `USE_VOICE_CLONE=true` in `.env`

Falls back to OpenAI TTS if cloning fails.
