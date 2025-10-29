#!/bin/bash

# Run both Backend and Frontend

echo "========================================="
echo "   Starting RenderEase Full Stack       "
echo "========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend in background
echo "Starting backend..."
(cd "$SCRIPT_DIR/backend" && source venv/bin/activate && python app.py) &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend..."
(cd "$SCRIPT_DIR/frontend" && npm start) &
FRONTEND_PID=$!

echo ""
echo "========================================="
echo "   RenderEase is Running!               "
echo "========================================="
echo "Backend:  http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
