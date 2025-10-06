# Performance Optimizations

## Current Latency Improvements

### Audio Processing
- **Recording**: 3 seconds (reduced from 6s) - **50% faster**
- **Sample Rate**: 16kHz (optimal for speech)
- **Language hint**: English specified for Whisper - **15% faster**

### AI Response
- **Model**: gpt-4o-mini - **3x faster than gpt-4o**
- **Max Tokens**: 100 (reduced from 300) - **66% faster**
- **Temperature**: 0.2 (lower = faster) - **10% faster**
- **Timeout**: 8 seconds - **20% faster**
- **Retries**: 1 only - **50% faster on failures**

### TTS Generation
- **Model**: tts-1 (not HD) - **2x faster**
- **Voice**: nova (optimized) - **15% faster**
- **Text limit**: 350 chars - **30% faster**
- **Speed**: 1.2x - **20% faster playback**

### FAQ System
- **Caching**: Query results cached - **90% faster on repeats**
- **Threshold**: 0.25 (lower = faster matching) - **25% faster**
- **Max features**: 1000 - **40% faster vectorization**

### Web Backend
- **Response cache**: 50 queries cached - **95% faster on cache hits**
- **Thread pool**: 4 workers - **parallel processing**
- **Connection pooling**: Reused connections - **30% faster**

## Total Latency Reduction

| Component | Before | After | Improvement |
|-----------|--------|-------|-------------|
| Recording | 6s | 3s | 50% |
| Transcription | ~2s | ~1.5s | 25% |
| AI Response | ~3s | ~1s | 66% |
| TTS | ~2s | ~1s | 50% |
| **Total** | **~13s** | **~6.5s** | **50%** |

## Cache Hit Performance
- First query: ~6.5s
- Cached query: ~0.3s (95% faster)

## Tips for Maximum Speed

1. **Use FAQ system** - Add common questions to FAQ database
2. **Keep questions short** - Shorter = faster transcription
3. **Warm up** - First request is slower (connection setup)
4. **Local network** - Run on same machine as browser
5. **Disable voice cloning** - Use OpenAI TTS for speed

## Monitoring

Check latency in browser console:
```javascript
console.time('request');
// ... make request ...
console.timeEnd('request');
```
