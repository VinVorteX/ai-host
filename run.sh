#!/bin/bash
# Quick start script for NextGen AI Assistant

echo "🚀 Starting NextGen AI Assistant..."

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
source env/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating from template..."
    cp .env.example .env
    echo "Please edit .env with your API keys"
    exit 1
fi

# Start the application
echo "✅ Starting web server on http://localhost:5000"
python app.py
