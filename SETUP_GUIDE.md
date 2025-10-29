# RenderEase - Complete Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Verification](#verification)
5. [Common Issues](#common-issues)
6. [Manual Setup](#manual-setup)

---

## System Requirements

### Required Software

| Software | Minimum Version | Download Link |
|----------|----------------|---------------|
| Python | 3.8 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| Node.js | 16.0 or higher | [nodejs.org](https://nodejs.org/) |
| npm | 8.0 or higher | (comes with Node.js) |
| pip | 20.0 or higher | (comes with Python) |

### Recommended System Specs
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 2GB free space
- **OS:** macOS, Linux, or Windows (with WSL)
- **Browser:** Chrome, Firefox, Safari, or Edge (latest versions)

---

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd "/Users/chief/Projects and Codes/566 Final Project"
```

### Step 2: Run Setup Script

This script will install all dependencies for both backend and frontend:

```bash
./setup.sh
```

**What the setup script does:**
- ✅ Checks for Python 3 and Node.js
- ✅ Creates Python virtual environment (`backend/venv/`)
- ✅ Installs Python packages (Flask, OpenCV, NumPy, etc.)
- ✅ Installs Node.js packages (React, Axios, etc.)
- ✅ Creates `.env` configuration files

**Expected output:**
```
=========================================
   RenderEase - Setup Script
=========================================

✓ Python 3 found: Python 3.x.x
✓ Node.js found: v16.x.x
✓ npm found: 8.x.x

Setting up Python backend...
----------------------------
Creating Python virtual environment...
Activating virtual environment...
Installing Python dependencies...
✓ Backend setup complete

Setting up React frontend...
----------------------------
Installing Node.js dependencies...
✓ Frontend setup complete

✓ Created backend/.env
✓ Created frontend/.env

=========================================
   Setup Complete!
=========================================

To start the application:
1. Run backend:  ./run-backend.sh
2. Run frontend: ./run-frontend.sh

Or use: ./run-all.sh (runs both)
```

### Step 3: Verify Installation

Check that all files were created:

```bash
# Check backend virtual environment
ls backend/venv/

# Check frontend node_modules
ls frontend/node_modules/

# Check environment files
ls backend/.env frontend/.env
```

---

## Running the Application

### Method 1: Run Everything Together (Recommended)

```bash
./run-all.sh
```

This will:
1. Start Flask backend on `http://localhost:5000`
2. Start React frontend on `http://localhost:3000`
3. Automatically open your browser to the frontend

**To stop:** Press `Ctrl+C` in the terminal

---

### Method 2: Run Backend and Frontend Separately

**Terminal 1 - Backend:**
```bash
./run-backend.sh
```

Wait for message: `Server running on http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
./run-frontend.sh
```

Wait for message: `Compiled successfully!` and browser opens automatically.

---

## Verification

### 1. Check Backend is Running

Open a new terminal and test the API:

```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{"status":"healthy","message":"RenderEase API is running"}
```

### 2. Check Frontend is Running

Open browser to: [http://localhost:3000](http://localhost:3000)

You should see the RenderEase interface with:
- Header: "RenderEase - Interior Design Visualization Tool"
- Left panel with controls
- Right panel with canvas area

### 3. Test Basic Functionality

1. Click "Choose Image" button
2. Select any image file from your computer
3. Image should appear on the canvas
4. Try selecting a region by click and drag
5. Select a texture from the texture library
6. Click "Apply Texture"

If all steps work, setup is successful! 🎉

---

## Common Issues

### Issue 1: Python not found

**Error:** `python3: command not found`

**Solution:**
```bash
# Install Python 3
# macOS:
brew install python3

# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install python3 python3-pip

# Then retry setup
./setup.sh
```

---

### Issue 2: Node.js not found

**Error:** `node: command not found`

**Solution:**
```bash
# macOS:
brew install node

# Ubuntu/Debian:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

---

### Issue 3: Port Already in Use

**Error:** `Address already in use: port 5000`

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in backend/app.py
# Change: app.run(port=5000)
# To: app.run(port=5001)

# And update frontend/.env
# Change: REACT_APP_API_URL=http://localhost:5000/api
# To: REACT_APP_API_URL=http://localhost:5001/api
```

**For Frontend (Port 3000):**
```bash
# Set different port before starting
PORT=3001 npm start
```

---

### Issue 4: Permission Denied on Scripts

**Error:** `Permission denied: ./setup.sh`

**Solution:**
```bash
chmod +x setup.sh run-backend.sh run-frontend.sh run-all.sh
```

---

### Issue 5: OpenCV Installation Failed

**Error:** `Failed building wheel for opencv-python`

**Solution:**
```bash
# Install system dependencies first
# macOS:
brew install cmake

# Ubuntu/Debian:
sudo apt-get install build-essential cmake

# Then install OpenCV
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install opencv-python==4.8.1.78
```

---

### Issue 6: React Build Errors

**Error:** `Module not found` or dependency errors

**Solution:**
```bash
cd frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# If still issues, try:
npm install --legacy-peer-deps
```

---

### Issue 7: CORS Errors in Browser

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solutions:**
1. Ensure backend is running on port 5000
2. Check `frontend/.env` has correct URL:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```
3. Verify Flask-CORS is installed:
   ```bash
   cd backend
   source venv/bin/activate
   pip install Flask-CORS
   ```
4. Restart both backend and frontend

---

### Issue 8: Virtual Environment Not Activating

**Error:** `source venv/bin/activate` doesn't work

**Solution:**
```bash
# Recreate virtual environment
cd backend
rm -rf venv
python3 -m venv venv

# Activate based on your shell
# Bash/Zsh:
source venv/bin/activate

# Fish:
source venv/bin/activate.fish

# Windows (if using WSL):
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Manual Setup

If the automated setup script doesn't work, follow these manual steps:

### Backend Setup (Manual)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install opencv-python==4.8.1.78
pip install opencv-contrib-python==4.8.1.78
pip install numpy==1.24.3
pip install Pillow==10.1.0
pip install python-dotenv==1.0.0

# Create .env file
cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
EOF

# Test backend
python app.py
```

### Frontend Setup (Manual)

```bash
cd frontend

# Install dependencies
npm install react@18.2.0
npm install react-dom@18.2.0
npm install react-scripts@5.0.1
npm install axios@1.6.0

# Create .env file
cat > .env << EOF
REACT_APP_API_URL=http://localhost:5000/api
EOF

# Test frontend
npm start
```

---

## Environment Variables

### Backend `.env`

```bash
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
# Optional:
# MAX_CONTENT_LENGTH=16777216  # 16MB
# UPLOAD_FOLDER=../uploads
```

### Frontend `.env`

```bash
REACT_APP_API_URL=http://localhost:5000/api
# Optional:
# PORT=3000
# BROWSER=chrome
```

---

## Testing Installation

### Quick Test Script

Create a test file `test_setup.py` in the backend directory:

```python
# backend/test_setup.py
import sys
print(f"Python version: {sys.version}")

try:
    import flask
    print(f"✓ Flask: {flask.__version__}")
except ImportError:
    print("✗ Flask not installed")

try:
    import cv2
    print(f"✓ OpenCV: {cv2.__version__}")
except ImportError:
    print("✗ OpenCV not installed")

try:
    import numpy as np
    print(f"✓ NumPy: {np.__version__}")
except ImportError:
    print("✗ NumPy not installed")

print("\nAll checks passed!" if all else "Some packages missing!")
```

Run it:
```bash
cd backend
source venv/bin/activate
python test_setup.py
```

---

## Performance Tips

### Backend Optimization

```python
# In backend/app.py, add these for production:

# Disable debug mode
app.run(debug=False)

# Use production server
# pip install gunicorn
# gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Optimization

```bash
# Build optimized production version
cd frontend
npm run build

# Serve with static server
npx serve -s build -l 3000
```

---

## Next Steps

Once setup is complete:

1. **Read the Documentation**
   - [NEW_README.md](NEW_README.md) - Full documentation
   - [API Documentation](#api-endpoints) - API reference

2. **Try the Examples**
   - Upload a room photo
   - Try different textures
   - Experiment with edge detection

3. **Explore the Code**
   - Backend: `backend/cv_algorithms/`
   - Frontend: `frontend/src/components/`

4. **Extend the Project**
   - Add new CV algorithms
   - Create custom textures
   - Implement new features

---

## Getting Help

If you encounter issues not covered here:

1. **Check the logs**
   - Backend: Look at terminal running `run-backend.sh`
   - Frontend: Check browser console (F12)

2. **Contact the team**
   - Bhinu Puvva: puvvala@wisc.edu
   - Bala Shukla: shukla35@wisc.edu
   - Rain Jiayu Sun: jsun424@wisc.edu

3. **Common resources**
   - Flask docs: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
   - React docs: [react.dev](https://react.dev/)
   - OpenCV docs: [docs.opencv.org](https://docs.opencv.org/)

---

## System Check Commands

Run these to verify your system is ready:

```bash
# Check Python
python3 --version
python3 -m pip --version

# Check Node.js
node --version
npm --version

# Check available disk space
df -h .

# Check memory
free -h  # Linux
vm_stat  # macOS

# Check ports are available
lsof -i :5000  # Should be empty
lsof -i :3000  # Should be empty
```

---

**Setup complete! Ready to visualize interior designs! 🎨🏠**

*Last updated: October 28, 2025*
