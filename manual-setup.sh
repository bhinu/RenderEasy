#!/bin/bash

# Manual Setup Script for RenderEase
# Use this if setup.sh has issues

echo "========================================="
echo "   RenderEase - Manual Setup            "
echo "========================================="
echo ""

# Step 1: Backend Setup
echo "Step 1: Setting up Backend..."
echo "----------------------------"
cd backend

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create fresh virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade base tools first
echo "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel

# Install packages one by one to catch errors
echo ""
echo "Installing Flask framework..."
pip install Flask>=2.3.0
pip install Flask-CORS>=4.0.0
pip install Werkzeug>=2.3.0

echo ""
echo "Installing NumPy (this may take a while)..."
pip install "numpy>=1.24.0,<2.0.0"

echo ""
echo "Installing OpenCV (this may take a while)..."
pip install opencv-python>=4.8.0

echo ""
echo "Installing Pillow..."
pip install Pillow>=10.0.0

echo ""
echo "Installing python-dotenv..."
pip install python-dotenv>=1.0.0

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat > .env << 'EOF'
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
EOF
fi

echo ""
echo "✓ Backend setup complete!"
echo ""

# Verify installation
echo "Verifying installation..."
python << 'PYEOF'
import sys
print(f"Python: {sys.version}")

try:
    import flask
    print(f"✓ Flask: {flask.__version__}")
except ImportError as e:
    print(f"✗ Flask: {e}")

try:
    import numpy as np
    print(f"✓ NumPy: {np.__version__}")
except ImportError as e:
    print(f"✗ NumPy: {e}")

try:
    import cv2
    print(f"✓ OpenCV: {cv2.__version__}")
except ImportError as e:
    print(f"✗ OpenCV: {e}")

try:
    import PIL
    print(f"✓ Pillow: {PIL.__version__}")
except ImportError as e:
    print(f"✗ Pillow: {e}")
PYEOF

cd ..

# Step 2: Frontend Setup
echo ""
echo "Step 2: Setting up Frontend..."
echo "----------------------------"
cd frontend

# Clean install
if [ -d "node_modules" ]; then
    echo "Removing old node_modules..."
    rm -rf node_modules package-lock.json
fi

echo "Installing Node.js dependencies..."
npm install --legacy-peer-deps

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << 'EOF'
REACT_APP_API_URL=http://localhost:5000/api
EOF
fi

echo ""
echo "✓ Frontend setup complete!"
echo ""

cd ..

echo "========================================="
echo "   Manual Setup Complete!               "
echo "========================================="
echo ""
echo "To start the application:"
echo "1. Backend:  ./run-backend.sh"
echo "2. Frontend: ./run-frontend.sh"
echo "Or use: ./run-all.sh"
echo ""
