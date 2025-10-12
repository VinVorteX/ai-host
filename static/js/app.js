let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const micBtn = document.getElementById('micBtn');
const sendBtn = document.getElementById('sendBtn');
const textInput = document.getElementById('textInput');
const messages = document.getElementById('messages');
const status = document.getElementById('status');
const visualizer = document.getElementById('visualizer');

document.addEventListener('DOMContentLoaded', () => {
    initGeminiEffect();
    addMessage('assistant', 'Namaste! I\'m Riva, your AI assistant. How can I help you today?');
});

function initGeminiEffect() {
    const svg = document.querySelector('.gemini-svg');
    if (!svg) return;
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        svg.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
    });
}

micBtn.addEventListener('click', () => {
    isRecording ? stopRecording() : startRecording();
});

sendBtn.addEventListener('click', () => {
    const text = textInput.value.trim();
    if (text) {
        handleStreamingTextRequest(text);
        textInput.value = '';
    }
});

textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendBtn.click();
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            handleAudioMessage(audioBlob);
            stream.getTracks().forEach(track => track.stop());
        };
        mediaRecorder.start();
        isRecording = true;
        micBtn.classList.add('recording');
        showVisualizer();
        setStatus('🎤 Listening...');
    } catch (error) {
        setStatus('❌ Microphone access denied');
        console.error(error);
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        micBtn.classList.remove('recording');
        hideVisualizer();
        setStatus('🔄 Transcribing...');
    }
}

async function handleAudioMessage(audioBlob) {
    try {
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = async () => {
            const base64Audio = reader.result;
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ audio: base64Audio })
            });

            const data = await response.json();

            if (response.ok) {
                handleStreamingTextRequest(data.transcript);
            } else {
                setStatus(`❌ Error: ${data.error}`);
            }
        };
    } catch (error) {
        setStatus('❌ Connection error');
        console.error(error);
    }
}

async function handleStreamingTextRequest(text) {
    addMessage('user', text);
    setStatus('🤔 Thinking...');
    const cacheKey = text.toLowerCase().trim();

    // Placeholder for assistant message
    const assistantMessageContent = addMessage('assistant', '');

    try {
        const response = await fetch('/api/text_stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        if (!response.ok) throw new Error(`Server error: ${response.statusText}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            assistantMessageContent.textContent += chunk;
            messages.scrollTop = messages.scrollHeight;
        }

        setStatus('');
        fetchAudio(cacheKey); // Fetch audio after text stream ends

    } catch (error) {
        assistantMessageContent.textContent = 'Sorry, I encountered a connection problem.';
        setStatus('❌ Connection error');
        console.error(error);
    }
}

async function fetchAudio(cacheKey, retries = 10) {
    if (retries <= 0) {
        console.error("Failed to fetch audio after multiple attempts.");
        return;
    }

    try {
        const response = await fetch(`/api/get_audio/${encodeURIComponent(cacheKey)}`);
        const data = await response.json();

        if (data.status === 'ready' && data.audio !== 'error') {
            // 🧠 FIXED: Convert Base64 to Blob to avoid "NotSupportedError"
            if (data.audio.startsWith('data:audio')) {
                const base64 = data.audio.split(',')[1];
                const binary = atob(base64);
                const array = new Uint8Array(binary.length);
                for (let i = 0; i < binary.length; i++) array[i] = binary.charCodeAt(i);
                const blob = new Blob([array], { type: 'audio/mp3' });
                const url = URL.createObjectURL(blob);
                const audio = new Audio(url);
                audio.play().catch(e => console.error('Audio playback failed:', e));
            } else {
                // if backend returns URL, play directly
                const audio = new Audio(data.audio);
                audio.play().catch(e => console.error('Audio playback failed:', e));
            }

        } else if (data.status === 'processing') {
            // Retry after 2s if audio still generating
            setTimeout(() => fetchAudio(cacheKey, retries - 1), 2000);
        } else {
            console.error("Failed to generate or fetch audio:", data.audio);
        }
    } catch (error) {
        console.error("Error in fetchAudio:", error);
    }
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🐴';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;

    return contentDiv;
}

function setStatus(text) {
    status.textContent = text;
}

function showVisualizer() {
    visualizer.classList.add('active');
    visualizer.innerHTML = '';
    for (let i = 0; i < 20; i++) {
        const bar = document.createElement('div');
        bar.className = 'voice-bar';
        bar.style.animationDelay = `${i * 0.05}s`;
        visualizer.appendChild(bar);
    }
}

function hideVisualizer() {
    visualizer.classList.remove('active');
}
