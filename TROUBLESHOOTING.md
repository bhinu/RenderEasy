# RenderEase - Troubleshooting Guide

## Common Setup Issues & Solutions

### Issue: "Cannot import 'setuptools.build_meta'"

This is a common Python build tools issue. Here are multiple solutions:

#### Solution 1: Use Manual Setup Script (Recommended)

```bash
./manual-setup.sh
```

This script installs packages in the correct order and handles the setuptools issue.

#### Solution 2: Manual Installation

```bash
# Navigate to backend
cd backend

# Remove old virtual environment
rm -rf venv

# Create fresh virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade build tools FIRST
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel

# Install packages one by one
pip install Flask Flask-CORS
pip install numpy
pip install opencv-python
pip install Pillow python-dotenv
```

#### Solution 3: Use System Python Packages

If virtual environment continues to have issues:

```bash
# Skip virtual environment (not recommended for production)
cd backend

# Install globally
pip3 install --user Flask Flask-CORS opencv-python numpy Pillow python-dotenv

# Run without activating venv
python3 app.py
```

---

### Issue: OpenCV Installation Fails

#### macOS Solution

```bash
# Install system dependencies
brew install cmake

# Then install OpenCV
cd backend
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install opencv-python
```

#### Linux (Ubuntu/Debian) Solution

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libopencv-dev

# Then install Python package
cd backend
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install opencv-python
```

#### Windows Solution

```bash
# Using WSL or Git Bash
pip install --upgrade pip setuptools wheel
pip install opencv-python
```

---

### Issue: NumPy Compatibility Error

#### Error: "numpy 2.0 is incompatible"

```bash
cd backend
source venv/bin/activate

# Install specific compatible version
pip install "numpy>=1.24.0,<2.0.0"
```

---

### Issue: Port Already in Use

#### Backend (Port 5000)

```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in backend/app.py
# Edit the last line to:
# app.run(debug=True, host='0.0.0.0', port=5001)

# Update frontend/.env accordingly:
# REACT_APP_API_URL=http://localhost:5001/api
```

#### Frontend (Port 3000)

```bash
# Find what's using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use different port
cd frontend
PORT=3001 npm start
```

---

### Issue: React Dependencies Conflict

```bash
cd frontend

# Clean install
rm -rf node_modules package-lock.json
npm cache clean --force

# Install with legacy peer deps flag
npm install --legacy-peer-deps
```

---

### Issue: CORS Errors in Browser

**Symptoms:** Browser console shows "CORS policy" errors

**Solutions:**

1. Verify backend is running:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. Check Flask-CORS is installed:
   ```bash
   cd backend
   source venv/bin/activate
   pip show Flask-CORS
   ```

3. Verify frontend .env file:
   ```bash
   cat frontend/.env
   # Should show: REACT_APP_API_URL=http://localhost:5000/api
   ```

4. Restart both servers:
   ```bash
   # Kill both servers (Ctrl+C)
   ./run-all.sh
   ```

---

### Issue: "Module not found" in Backend

**Error:** `ModuleNotFoundError: No module named 'cv2'` or similar

**Solution:**

```bash
cd backend

# Make sure you're in the virtual environment
source venv/bin/activate

# Verify activation (should show path to venv)
which python

# Reinstall missing package
pip install opencv-python

# Test import
python -c "import cv2; print(cv2.__version__)"
```

---

### Issue: React App Won't Start

**Error:** Various npm/React errors

**Solution:**

```bash
cd frontend

# Complete cleanup
rm -rf node_modules package-lock.json .cache

# Clear npm cache
npm cache clean --force

# Reinstall
npm install --legacy-peer-deps

# If still failing, check Node version
node --version  # Should be 16+

# Update Node if needed (macOS):
brew upgrade node

# Update Node (Linux):
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

### Issue: Virtual Environment Won't Activate

**Error:** `source venv/bin/activate` doesn't work

**Solutions:**

#### For different shells:

```bash
# Bash/Zsh (default on macOS/Linux):
source venv/bin/activate

# Fish shell:
source venv/bin/activate.fish

# Windows Git Bash:
source venv/Scripts/activate
```

#### If still not working:

```bash
# Delete and recreate
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Verify
which python  # Should show path inside venv
```

---

### Issue: Permission Denied

**Error:** `Permission denied` when running scripts

**Solution:**

```bash
# Make scripts executable
chmod +x setup.sh
chmod +x manual-setup.sh
chmod +x run-backend.sh
chmod +x run-frontend.sh
chmod +x run-all.sh
```

---

### Issue: Image Upload Not Working

**Symptoms:** Image upload button doesn't respond or images don't display

**Solutions:**

1. Check browser console for errors (F12)

2. Verify backend is running:
   ```bash
   curl http://localhost:5000/api/health
   ```

3. Check file size (must be < 16MB)

4. Try different image format (JPEG/PNG)

5. Check uploads directory exists:
   ```bash
   mkdir -p uploads
   ```

---

### Issue: Texture Application Not Working

**Symptoms:** "Apply Texture" button doesn't work or gives errors

**Solutions:**

1. Ensure you've selected:
   - ✓ An image
   - ✓ A region (click and drag on canvas)
   - ✓ A texture

2. Check backend logs for errors

3. Try with smaller image

4. Verify all CV modules loaded:
   ```bash
   cd backend
   source venv/bin/activate
   python -c "from cv_algorithms.homography import HomographyTransform; print('OK')"
   ```

---

## Verification Tests

### Test Backend

```bash
cd backend
source venv/bin/activate

# Test Python imports
python << 'EOF'
import flask
import cv2
import numpy as np
from PIL import Image
print("All imports successful!")
EOF

# Test Flask app
python app.py
# Should show: "Server running on http://localhost:5000"
```

### Test Frontend

```bash
cd frontend

# Test React
npm start
# Should open browser to http://localhost:3000
```

### Test Full Stack

```bash
# Terminal 1
./run-backend.sh

# Terminal 2
./run-frontend.sh

# In browser at http://localhost:3000
# 1. Upload an image
# 2. Select a region
# 3. Choose a texture
# 4. Click "Apply Texture"
```

---

## Quick Fixes

### Complete Reset

If everything is broken, start fresh:

```bash
# 1. Clean everything
rm -rf backend/venv
rm -rf frontend/node_modules
rm -rf frontend/package-lock.json

# 2. Run manual setup
./manual-setup.sh

# 3. Test
./run-all.sh
```

### Backend Only Reset

```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Frontend Only Reset

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

## Environment-Specific Issues

### macOS Apple Silicon (M1/M2)

Some packages need Rosetta 2:

```bash
# Install Rosetta if not already
softwareupdate --install-rosetta

# Use x86 Python
arch -x86_64 python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (WSL)

```bash
# Make sure you're in WSL, not Command Prompt
wsl

# Then follow Linux instructions
./manual-setup.sh
```

---

## Getting Additional Help

If issues persist:

1. **Check logs:**
   - Backend: Look at terminal running backend
   - Frontend: Browser console (F12)

2. **Verify versions:**
   ```bash
   python3 --version  # Should be 3.8+
   node --version     # Should be 16+
   pip --version      # Should be 20+
   npm --version      # Should be 8+
   ```

3. **Check system resources:**
   ```bash
   # Disk space
   df -h .

   # Memory
   free -h  # Linux
   vm_stat  # macOS
   ```

4. **Contact team:**
   - Bhinu Puvva: puvvala@wisc.edu
   - Bala Shukla: shukla35@wisc.edu
   - Rain Jiayu Sun: jsun424@wisc.edu

---

## Minimal Working Setup

If you just want to get something running quickly:

### Option 1: Backend Only (No React)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install Flask Flask-CORS opencv-python numpy Pillow
python app.py

# Test with curl
curl http://localhost:5000/api/health
```

### Option 2: Use Old Vanilla JS Version

```bash
# Use the original simple version
open index.html

# Or with server
python3 -m http.server 8000
open http://localhost:8000
```

---

**Last Updated:** October 28, 2025
