#!/usr/bin/env python3
"""Start FastAPI version of Riva AI Assistant"""

import os
import sys
import subprocess

def check_fastapi_deps():
    """Check FastAPI dependencies"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI dependencies available")
        return True
    except ImportError:
        print("❌ Installing FastAPI dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]", "jinja2", "python-multipart"])
        return True

def main():
    """Start FastAPI server"""
    print("🐴 Riva AI Assistant - FastAPI Version")
    print("=" * 50)
    
    if not check_fastapi_deps():
        sys.exit(1)
    
    print("🚀 Starting FastAPI server...")
    print("📱 Frontend: http://127.0.0.1:5000")
    print("📚 API Docs: http://127.0.0.1:5000/docs")
    print("🎨 Demo: http://127.0.0.1:5000/demo")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "app:app",
            host="127.0.0.1",
            port=5000,
            reload=False,
            workers=1,
            access_log=False
        )
    except KeyboardInterrupt:
        print("\n👋 FastAPI server stopped")

if __name__ == "__main__":
    main()