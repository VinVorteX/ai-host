import { useState, useRef } from 'react'
import axios from 'axios'
import './styles/App.css'

function App() {
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (e) => {
        audioChunksRef.current.push(e.data)
      }

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        await handleAudioMessage(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Microphone error:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      setIsProcessing(true)
    }
  }

  const handleAudioMessage = async (audioBlob) => {
    try {
      const reader = new FileReader()
      reader.readAsDataURL(audioBlob)
      reader.onloadend = async () => {
        const base64Audio = reader.result
        const response = await axios.post('/api/transcribe', { audio: base64Audio })
        
        if (response.data.transcript) {
          await handleTextMessage(response.data.transcript)
        }
        setIsProcessing(false)
      }
    } catch (error) {
      setIsProcessing(false)
      console.error('Transcription error:', error)
    }
  }

  const handleTextMessage = async (text) => {
    try {
      const response = await fetch('/api/text_stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        decoder.decode(value)
      }

      fetchAudio(text.toLowerCase().trim())
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const fetchAudio = async (cacheKey, retries = 10) => {
    if (retries <= 0) return

    try {
      const response = await axios.get(`/api/get_audio/${encodeURIComponent(cacheKey)}`)
      
      if (response.data.status === 'ready' && response.data.audio !== 'error') {
        const audio = new Audio(response.data.audio)
        audio.play().catch(e => console.error('Audio playback failed:', e))
      } else if (response.data.status === 'processing') {
        setTimeout(() => fetchAudio(cacheKey, retries - 1), 2000)
      }
    } catch (error) {
      console.error('Audio fetch error:', error)
    }
  }

  return (
    <div className="app">
      <div className="jarvis-container">
        <div className={`jarvis-circle ${isRecording ? 'active' : ''} ${isProcessing ? 'processing' : ''}`}>
          <div className="circle-ring ring-1"></div>
          <div className="circle-ring ring-2"></div>
          <div className="circle-ring ring-3"></div>
          <div className="circle-ring ring-4"></div>
          <div className="circle-ring ring-5"></div>
          
          <button 
            className="jarvis-core"
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
          >
            <div className="core-inner">
              <span className="riva-text">RIVA</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  )
}

export default App