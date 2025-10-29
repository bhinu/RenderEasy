# 🏠 RenderEase - START HERE

Welcome to **RenderEase** - Interior Design Visualization Tool!

---

## ⚡ Quick Start (If You're in a Hurry)

```bash
# 1. Install everything (one time)
./manual-setup.sh

# 2. Run the app
./run-all.sh

# 3. Open browser to http://localhost:3000
```

**That's it!** 🎉

---

## 📖 What is RenderEase?

A web application that lets interior designers visualize how different textures (wood, carpet, tile, etc.) will look on surfaces like floors, walls, and ceilings.

**Key Features:**
- 🖼️ Upload room photos
- 🎨 Choose from 12+ textures
- 🤖 Automatic surface detection (Hough Transform)
- 🔍 Edge detection (Canny algorithm)
- ✨ Real-time preview
- 💾 Export results

---

## 🏗️ Architecture

```
React Frontend (Port 3000)
    ↕ REST API
Flask Backend (Port 5000)
    ↕
Computer Vision Algorithms
├── Edge Detection
├── Hough Transform
├── Segmentation
├── Homography
└── Texture Generation
```

---

## 📋 Prerequisites

Make sure you have these installed:

- [x] **Python 3.8+** - [Download](https://www.python.org/downloads/)
- [x] **Node.js 16+** - [Download](https://nodejs.org/)

Check your versions:
```bash
python3 --version
node --version
```

---

## 🚀 Installation Options

### Option 1: Automated Setup (Try this first)

```bash
./setup.sh
```

### Option 2: Manual Setup (If automated fails)

```bash
./manual-setup.sh
```

This installs packages in the correct order and handles setuptools issues.

### Option 3: Step-by-step Manual (If both fail)

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed manual instructions.

---

## 🎮 Running the Application

### All-in-One Command
```bash
./run-all.sh
```
This starts both backend and frontend.

### Separate Terminals
**Terminal 1:**
```bash
./run-backend.sh
```

**Terminal 2:**
```bash
./run-frontend.sh
```

---

## ✅ Verify It's Working

### 1. Check Backend
```bash
curl http://localhost:5000/api/health
```
Should return: `{"status":"healthy",...}`

### 2. Check Frontend
Open browser: [http://localhost:3000](http://localhost:3000)

You should see the RenderEase interface!

### 3. Test It
1. Click "Choose Image"
2. Upload a room photo
3. Select a texture
4. Click and drag on the canvas to select a region
5. Click "Apply Texture"
6. See the magic! ✨

---

## 🆘 Having Issues?

### Quick Fixes

**"Cannot import setuptools"**
```bash
./manual-setup.sh
```

**"Port already in use"**
```bash
lsof -i :5000
kill -9 <PID>
```

**Something else broke**
```bash
# Nuclear option - reset everything
rm -rf backend/venv frontend/node_modules
./manual-setup.sh
```

For more solutions: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **START_HERE.md** | You are here! 👋 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Command cheat sheet |
| [NEW_README.md](NEW_README.md) | Complete documentation |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed setup guide |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Fix common issues |
| [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt) | Project layout |

---

## 🎓 For Students/Developers

### Project Structure
```
backend/
├── cv_algorithms/          # Computer vision modules
│   ├── edge_detector.py    # Canny, Sobel, Laplacian
│   ├── hough_transform.py  # Line/circle detection
│   ├── segmentation.py     # Various segmentation
│   ├── homography.py       # Perspective transform
│   └── texture_generator.py# Procedural textures
└── app.py                  # Flask API server

frontend/
└── src/
    ├── components/         # React components
    │   ├── ImageUploader.js
    │   ├── Canvas.js
    │   ├── TextureLibrary.js
    │   └── Controls.js
    └── services/
        └── api.js          # API service layer
```

### Key Technologies
- **Backend:** Flask, OpenCV, NumPy
- **Frontend:** React, Axios
- **CV Algorithms:** Canny, Hough, GrabCut, K-means, Homography

### API Endpoints
- `POST /api/edge-detection` - Detect edges
- `POST /api/detect-lines` - Hough transform
- `POST /api/segment` - Image segmentation
- `POST /api/apply-texture` - Apply texture with perspective
- More in [NEW_README.md](NEW_README.md)

---

## 🎨 How to Use

### Basic Workflow

1. **Upload Image**
   - Drag & drop or click "Choose Image"
   - Supports JPG, PNG, BMP (< 16MB)

2. **Detect Surfaces (Optional)**
   - Click "Detect Edges" for Canny edge detection
   - Click "Detect Surfaces" for automatic Hough line detection
   - OR manually select by clicking and dragging

3. **Choose Texture**
   - 12 built-in textures available
   - Wood, Marble, Carpet, Tile, Brick, Concrete

4. **Adjust Settings**
   - **Opacity:** 0-100% (80% recommended)
   - **Brightness:** -50 to +50
   - **Blend Mode:** Normal, Multiply, Overlay, Soft Light

5. **Apply & Save**
   - Click "Apply Texture"
   - Click "Save Result" to download

### Pro Tips 💡

- Use **Multiply** blend mode for floors
- Use **Overlay** blend mode for walls
- Adjust brightness to match room lighting
- Select entire surface for best results
- Higher resolution images = better quality

---

## 🔬 Computer Vision Features

### Implemented Algorithms

**Edge Detection:**
- ✅ Canny (multi-stage optimal)
- ✅ Sobel (gradient-based)
- ✅ Laplacian (second derivative)
- ✅ Adaptive thresholding
- ✅ Morphological gradients

**Hough Transform:**
- ✅ Line detection (standard & probabilistic)
- ✅ Circle detection
- ✅ Horizontal/vertical filtering
- ✅ Intersection finding

**Segmentation:**
- ✅ Color-based (HSV/LAB/RGB)
- ✅ GrabCut (interactive)
- ✅ Watershed (topology)
- ✅ K-means clustering
- ✅ Mean shift
- ✅ Flood fill

**Homography:**
- ✅ Perspective transformation
- ✅ Texture warping
- ✅ Region rectification
- ✅ Distortion correction

**Texture Generation:**
- ✅ Procedural wood with grain
- ✅ Marble with veins
- ✅ Carpet fibers
- ✅ Tiles with grout
- ✅ Brick patterns
- ✅ Concrete aggregate

---

## 🎯 Project Goals

This is an academic project for **COMP SCI 566 - Intro to Computer Vision** at UW-Madison.

**Objectives:**
1. Apply CV algorithms to real-world problem
2. Compare traditional vs. deep learning approaches
3. Create accessible tool for designers
4. Demonstrate image processing pipeline

**Timeline:**
- ✅ Phase 1-2: Foundation & core features (Complete)
- 🔄 Phase 3: Advanced CV (In progress)
- 📅 Phase 4: Deep learning integration (Planned)

---

## 👥 Team

**Team Members:**
- Bhinu Puvva - puvvala@wisc.edu
- Bala Shukla - shukla35@wisc.edu
- Rain Jiayu Sun - jsun424@wisc.edu

**Course:** COMP SCI 566
**Institution:** University of Wisconsin-Madison

---

## 🚦 Next Steps

### For First-Time Users
1. ✅ Install with `./manual-setup.sh`
2. ✅ Run with `./run-all.sh`
3. ✅ Try uploading an image
4. ✅ Experiment with textures
5. 📖 Read [NEW_README.md](NEW_README.md) for details

### For Developers
1. 📖 Review [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)
2. 🔍 Explore `backend/cv_algorithms/`
3. ⚛️ Check out React components in `frontend/src/`
4. 🧪 Test API endpoints
5. 🎨 Add new features!

### For Researchers
1. 📖 Study CV algorithms in `cv_algorithms/`
2. 🔬 Compare with deep learning approaches
3. 📊 Benchmark performance
4. 📝 Document findings

---

## 💬 Getting Help

### Self-Help Resources
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command cheatsheet
2. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
3. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup

### Contact Team
- Bhinu Puvva: puvvala@wisc.edu
- Bala Shukla: shukla35@wisc.edu
- Rain Jiayu Sun: jsun424@wisc.edu

---

## 📊 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend API | ✅ Complete | Flask + OpenCV |
| Frontend UI | ✅ Complete | React + Axios |
| Edge Detection | ✅ Complete | Canny, Sobel, Laplacian |
| Hough Transform | ✅ Complete | Line & circle detection |
| Segmentation | ✅ Complete | 6 algorithms |
| Homography | ✅ Complete | Perspective transform |
| Textures | ✅ Complete | 12+ procedural |
| Deep Learning | 📅 Planned | UNet, SAM |

---

## 🎉 Success!

If you see the RenderEase interface in your browser, congratulations! You're ready to visualize interior designs!

**Try it now:**
1. Upload a room photo
2. Select the floor
3. Apply a wood texture
4. See the transformation!

---

## 📜 License

Academic project for University of Wisconsin-Madison COMP SCI 566.
All rights reserved by the team members.

---

**Happy Designing! 🎨🏠✨**

*Last updated: October 28, 2025*
