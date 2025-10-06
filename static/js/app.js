let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const micBtn = document.getElementById('micBtn');
const sendBtn = document.getElementById('sendBtn');
const textInput = document.getElementById('textInput');
const messages = document.getElementById('messages');
const status = document.getElementById('status');
const visualizer = document.getElementById('visualizer');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initGeminiEffect();
    addMessage('assistant', 'Namaste! I\'m Chetak, your AI assistant. How can I help you today?');
});

// Gemini Effect Animation
function initGeminiEffect() {
    const svg = document.querySelector('.gemini-svg');
    if (!svg) return;
    
    // Subtle parallax effect on mouse move
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        svg.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
    });
}

// Microphone button
micBtn.addEventListener('click', async () => {
    if (!isRecording) {
        await startRecording();
    } else {
        await stopRecording();
    }
});

// Send button
sendBtn.addEventListener('click', () => {
    const text = textInput.value.trim();
    if (text) {
        sendTextMessage(text);
        textInput.value = '';
    }
});

// Enter key
textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            await sendAudioMessage(audioBlob);
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

async function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        micBtn.classList.remove('recording');
        hideVisualizer();
        setStatus('🔄 Processing...');
    }
}

async function sendAudioMessage(audioBlob) {
    try {
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = async () => {
            const base64Audio = reader.result;

            const response = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ audio: base64Audio })
            });

            const data = await response.json();

            if (response.ok) {
                addMessage('user', data.transcript);
                addMessage('assistant', data.response, data.audio);
                setStatus('');
            } else {
                setStatus(`❌ Error: ${data.error}`);
            }
        };
    } catch (error) {
        setStatus('❌ Connection error');
        console.error(error);
    }
}

async function sendTextMessage(text) {
    addMessage('user', text);
    setStatus('🔄 Processing...');

    try {
        const response = await fetch('/api/text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (response.ok) {
            addMessage('assistant', data.response, data.audio);
            setStatus('');
        } else {
            setStatus(`❌ Error: ${data.error}`);
        }
    } catch (error) {
        setStatus('❌ Connection error');
        console.error(error);
    }
}

function addMessage(role, content, audioData = null) {
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

    // Play audio if provided
    if (audioData) {
        const audio = new Audio(audioData);
        audio.play().catch(e => console.error('Audio playback failed:', e));
    }

    // Scroll to bottom
    messages.scrollTop = messages.scrollHeight;
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
