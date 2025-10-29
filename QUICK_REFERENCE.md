# RenderEase - Quick Reference Card

## 🚀 Getting Started (2 Commands)

```bash
./manual-setup.sh    # First time only
./run-all.sh         # Every time
```

Open browser to: **http://localhost:3000**

---

## 📁 Project Layout

```
backend/
├── cv_algorithms/   # CV modules
└── app.py          # Flask server

frontend/
├── src/
│   ├── components/ # React components
│   └── services/   # API calls
```

---

## 🛠️ Common Commands

### Setup & Installation

```bash
./manual-setup.sh        # Initial setup (if setup.sh fails)
./setup.sh              # Automated setup
```

### Running

```bash
./run-all.sh            # Start everything
./run-backend.sh        # Backend only (port 5000)
./run-frontend.sh       # Frontend only (port 3000)
```

### Testing

```bash
# Test backend
curl http://localhost:5000/api/health

# Test imports
cd backend && source venv/bin/activate
python -c "import cv2, numpy, flask; print('OK')"
```

### Cleanup

```bash
# Full reset
rm -rf backend/venv frontend/node_modules
./manual-setup.sh

# Backend only
cd backend && rm -rf venv && python3 -m venv venv
source venv/bin/activate && pip install -r requirements.txt

# Frontend only
cd frontend && rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

## 🔧 Troubleshooting

### "Cannot import setuptools"
```bash
./manual-setup.sh
```

### Port already in use
```bash
lsof -i :5000  # or :3000
kill -9 <PID>
```

### CORS errors
```bash
# Restart both servers
# Verify backend/.env and frontend/.env
```

### Module not found
```bash
cd backend && source venv/bin/activate
pip install <missing-package>
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/edge-detection` | POST | Detect edges |
| `/api/detect-lines` | POST | Hough transform |
| `/api/segment` | POST | Segmentation |
| `/api/generate-texture` | POST | Create texture |
| `/api/apply-texture` | POST | Apply to image |
| `/api/detect-surfaces` | POST | Auto-detect |

---

## 🎨 CV Algorithms

### Edge Detection
- Canny (best overall)
- Sobel (gradient-based)
- Laplacian (second derivative)

### Hough Transform
- Line detection (floors/walls/ceilings)
- Circle detection
- Corner finding

### Segmentation
- Color-based (HSV/LAB)
- GrabCut (interactive)
- Watershed (topology-based)
- K-means (clustering)

### Homography
- Perspective transformation
- Texture warping
- Rectification

---

## 📦 Dependencies

### Backend
```
Flask ≥2.3
opencv-python ≥4.8
numpy ≥1.24,<2.0
Pillow ≥10.0
```

### Frontend
```
react 18.2
axios 1.6
react-scripts 5.0
```

---

## 💡 Usage Tips

1. **Upload image** → Drag & drop or click button
2. **Detect surfaces** → Auto-detect or manual select
3. **Choose texture** → Click from 12 textures
4. **Adjust settings** → Opacity, brightness, blend
5. **Apply & save** → Click apply, then save

### Best Blend Modes
- **Normal** - Direct overlay
- **Multiply** - For floors (darkens)
- **Overlay** - For walls (preserves detail)
- **Soft Light** - Subtle changes

---

## 🔍 File Locations

### Backend
- **Main API**: `backend/app.py`
- **Edge Detection**: `backend/cv_algorithms/edge_detector.py`
- **Hough Transform**: `backend/cv_algorithms/hough_transform.py`
- **Segmentation**: `backend/cv_algorithms/segmentation.py`
- **Homography**: `backend/cv_algorithms/homography.py`
- **Textures**: `backend/cv_algorithms/texture_generator.py`

### Frontend
- **Main App**: `frontend/src/App.js`
- **Canvas**: `frontend/src/components/Canvas.js`
- **Upload**: `frontend/src/components/ImageUploader.js`
- **Textures**: `frontend/src/components/TextureLibrary.js`
- **API**: `frontend/src/services/api.js`

---

## ⚡ Performance

| Operation | Time |
|-----------|------|
| Image upload | < 1s |
| Edge detection | 200-500ms |
| Hough transform | 500-1000ms |
| Texture gen | 100-300ms |
| Apply texture | 500-1500ms |

---

## 📚 Documentation

- **NEW_README.md** - Complete docs
- **SETUP_GUIDE.md** - Detailed setup
- **TROUBLESHOOTING.md** - Fix issues
- **PROJECT_STRUCTURE.txt** - File layout

---

## 🆘 Emergency Commands

### Everything is broken
```bash
rm -rf backend/venv frontend/node_modules
./manual-setup.sh
```

### Backend broken
```bash
cd backend && rm -rf venv
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install Flask Flask-CORS opencv-python numpy Pillow python-dotenv
```

### Frontend broken
```bash
cd frontend && rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Can't fix it
```bash
# Use original vanilla JS version
open index.html
```

---

## 👥 Team

- Bhinu Puvva: puvvala@wisc.edu
- Bala Shukla: shukla35@wisc.edu
- Rain Jiayu Sun: jsun424@wisc.edu

COMP SCI 566 - UW-Madison

---

**Print this for quick reference!**
