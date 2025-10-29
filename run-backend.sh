#!/bin/bash

# Run RenderEase Backend

echo "========================================="
echo "   Starting RenderEase Backend          "
echo "========================================="

cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Run Flask app
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python app.py
