#!/bin/bash

# RenderEase Startup Script

echo "========================================="
echo "   RenderEase - Starting Application    "
echo "========================================="
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found"
    echo ""
    echo "Starting local server on http://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    echo "Opening browser in 2 seconds..."

    # Start server in background
    python3 -m http.server 8000 &
    SERVER_PID=$!

    # Wait a moment for server to start
    sleep 2

    # Open browser (works on macOS, Linux, Windows Git Bash)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open http://localhost:8000
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open http://localhost:8000 2>/dev/null || echo "Please open http://localhost:8000 in your browser"
    else
        # Windows or other
        start http://localhost:8000 2>/dev/null || echo "Please open http://localhost:8000 in your browser"
    fi

    # Wait for user to stop
    wait $SERVER_PID

elif command -v python &> /dev/null; then
    echo "✓ Python found"
    echo ""
    echo "Starting local server on http://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""

    python -m SimpleHTTPServer 8000

else
    echo "❌ Python not found!"
    echo ""
    echo "Alternative options:"
    echo "1. Install Python: https://www.python.org/downloads/"
    echo "2. Open index.html directly in your browser"
    echo "3. Use another web server (Node.js, PHP, etc.)"
    echo ""
fi
