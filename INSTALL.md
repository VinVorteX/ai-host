# Installation Guide

## Cross-Platform Setup

### Windows

```powershell
# Install Python 3.8+ from python.org

# Clone and setup
git clone <repo-url>
cd nextgen
python -m venv env
env\Scripts\activate
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env with your API keys

# Run
python app.py  # Web UI
# OR
python main.py  # CLI
```

### macOS

```bash
# Install Python 3.8+ (if not installed)
brew install python3

# Clone and setup
git clone <repo-url>
cd nextgen
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python app.py  # Web UI
# OR
python main.py  # CLI
```

### Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install mpg123 ffmpeg alsa-utils portaudio19-dev

# Clone and setup
git clone <repo-url>
cd nextgen
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python app.py  # Web UI
# OR
python main.py  # CLI
```

### Linux (Fedora/RHEL)

```bash
# Install dependencies
sudo dnf install python3 python3-pip
sudo dnf install mpg123 ffmpeg alsa-utils portaudio-devel

# Clone and setup
git clone <repo-url>
cd nextgen
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python app.py  # Web UI
# OR
python main.py  # CLI
```

## Troubleshooting

### Audio Issues (Linux)
```bash
# Test audio output
speaker-test -t wav -c 2

# Check available players
python -c "from utils.audio_player import check_audio_dependencies; print(check_audio_dependencies())"
```

### Microphone Issues
```bash
# Test microphone
arecord -d 3 test.wav && aplay test.wav

# Check permissions (Linux)
sudo usermod -a -G audio $USER
```

### Port Already in Use
```bash
# Change port in app.py
# app.run(port=5001)  # Use different port
```

## Verification

```bash
# Test installation
python -c "import openai, flask, sounddevice; print('✅ All dependencies installed')"

# Test API connection
python -c "from ai.chat import ask_chatgpt; print(ask_chatgpt('test'))"
```
