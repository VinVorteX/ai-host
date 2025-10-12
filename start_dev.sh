#!/bin/bash

echo "🚀 Starting Riva AI Assistant (Development Mode)"
echo "=================================================="

# Start backend
echo "📡 Starting FastAPI backend on port 5000..."
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting React frontend on port 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Development servers started!"
echo "📱 Frontend: http://localhost:3000"
echo "📡 Backend:  http://localhost:5000"
echo "📚 API Docs: http://localhost:5000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait