"""Security configuration for the AI assistant"""
import os

# File validation settings
ALLOWED_AUDIO_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.ogg'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_TEXT_LENGTH = 1000

# Path validation
def validate_file_path(path: str) -> bool:
    """Validate file path to prevent directory traversal"""
    if not path or '..' in path or path.startswith('/'):
        return False
    return os.path.isfile(path)

def validate_audio_extension(path: str) -> bool:
    """Validate audio file extension"""
    return any(path.lower().endswith(ext) for ext in ALLOWED_AUDIO_EXTENSIONS)

def sanitize_text_input(text: str) -> str:
    """Sanitize text input"""
    if not isinstance(text, str):
        return ""
    return text.strip()[:MAX_TEXT_LENGTH]