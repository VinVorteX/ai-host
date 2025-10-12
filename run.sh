#!/bin/bash

# Riva AI Assistant - FastAPI Startup Script
echo "🐴 Starting Riva AI Assistant (FastAPI)"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check environment variables
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create it with your API keys."
    exit 1
fi

# Start FastAPI server
echo "🚀 Starting FastAPI server..."
echo "📱 Frontend: http://127.0.0.1:5000"
echo "📚 API Docs: http://127.0.0.1:5000/docs"
echo ""
python start.py