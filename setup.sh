#!/bin/bash

# RenderEase Setup Script

echo "========================================="
echo "   RenderEase - Setup Script            "
echo "========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"
echo "✓ npm found: $(npm --version)"
echo ""

# Setup Backend
echo "Setting up Python backend..."
echo "----------------------------"

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "✓ Backend setup complete"
echo ""

cd ..

# Setup Frontend
echo "Setting up React frontend..."
echo "----------------------------"

cd frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✓ Frontend setup complete"
echo ""

cd ..

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "Creating backend .env file..."
    cat > backend/.env << EOF
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
EOF
    echo "✓ Created backend/.env"
fi

if [ ! -f "frontend/.env" ]; then
    echo "Creating frontend .env file..."
    cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:5000/api
EOF
    echo "✓ Created frontend/.env"
fi

echo ""
echo "========================================="
echo "   Setup Complete!                      "
echo "========================================="
echo ""
echo "To start the application:"
echo "1. Run backend:  ./run-backend.sh"
echo "2. Run frontend: ./run-frontend.sh"
echo ""
echo "Or use: ./run-all.sh (runs both)"
echo ""
