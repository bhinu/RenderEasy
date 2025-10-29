# RenderEase - Interior Design Visualization Tool
## Flask Backend + React Frontend Architecture

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-18.2-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)

A full-stack web application for interior design visualization with computer vision algorithms for automatic surface detection and texture application.

## Team
- **Bhinu Puvva** - puvvala@wisc.edu
- **Bala Shukla** - shukla35@wisc.edu
- **Rain Jiayu Sun** - jsun424@wisc.edu

**Course:** COMP SCI 566 - Intro to Computer Vision
**Institution:** University of Wisconsin-Madison

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                 React Frontend                   │
│         (localhost:3000)                         │
│  - Image Upload UI                               │
│  - Canvas for Selection                          │
│  - Texture Library                               │
│  - Real-time Preview                             │
└────────────────┬────────────────────────────────┘
                 │ HTTP/REST API
                 │ (JSON)
┌────────────────▼────────────────────────────────┐
│             Flask Backend API                    │
│         (localhost:5000)                         │
│  - Image Processing Endpoints                    │
│  - CV Algorithm Integration                      │
│  - Texture Generation                            │
└────────────────┬────────────────────────────────┘
                 │
      ┌──────────┼──────────┐
      │          │          │
┌─────▼────┐ ┌──▼────┐ ┌──▼────────┐
│   Edge   │ │ Hough │ │Segmenta- │
│ Detection│ │Transform│ │  tion    │
└──────────┘ └────────┘ └───────────┘
```

---

## Project Structure

```
566 Final Project/
│
├── backend/                    # Python Flask Backend
│   ├── cv_algorithms/          # Computer Vision Modules
│   │   ├── __init__.py
│   │   ├── edge_detector.py    # Canny, Sobel, Laplacian
│   │   ├── hough_transform.py  # Line/Circle Detection
│   │   ├── segmentation.py     # Color, GrabCut, Watershed
│   │   ├── homography.py       # Perspective Transform
│   │   └── texture_generator.py# Procedural Textures
│   │
│   ├── api/                    # API Utilities (future)
│   ├── utils/                  # Helper Functions (future)
│   ├── app.py                  # Main Flask Application
│   ├── requirements.txt        # Python Dependencies
│   └── .env                    # Environment Variables
│
├── frontend/                   # React Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUploader.js
│   │   │   ├── Canvas.js
│   │   │   ├── TextureLibrary.js
│   │   │   └── Controls.js
│   │   ├── services/
│   │   │   └── api.js          # API Service Layer
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env
│
├── uploads/                    # Uploaded Images Storage
│
├── setup.sh                    # One-time Setup Script
├── run-backend.sh              # Start Backend Server
├── run-frontend.sh             # Start Frontend Server
├── run-all.sh                  # Start Both Servers
│
└── NEW_README.md              # This File
```

---

## Quick Start

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)

### Installation

```bash
# 1. Clone or navigate to project directory
cd "566 Final Project"

# 2. Run setup script (installs all dependencies)
./setup.sh

# This will:
# - Create Python virtual environment
# - Install Python packages (Flask, OpenCV, etc.)
# - Install Node.js packages (React, Axios, etc.)
# - Create environment files
```

### Running the Application

**Option 1: Run Everything Together**
```bash
./run-all.sh
```
Then open [http://localhost:3000](http://localhost:3000) in your browser.

**Option 2: Run Separately**

Terminal 1 - Backend:
```bash
./run-backend.sh
```

Terminal 2 - Frontend:
```bash
./run-frontend.sh
```

---

## Features

### ✅ Implemented (v2.0)

#### Backend (Flask + Python)

1. **Edge Detection API**
   - Canny edge detection
   - Sobel edge detection
   - Laplacian edge detection
   - Adaptive thresholding
   - Morphological edge detection

2. **Hough Transform API**
   - Line detection (standard & probabilistic)
   - Circle detection
   - Horizontal/vertical line filtering
   - Line intersection finding
   - Visualization of detected features

3. **Segmentation API**
   - Color-based segmentation (HSV/LAB/RGB)
   - GrabCut segmentation
   - Watershed segmentation
   - K-means clustering
   - Mean shift segmentation
   - Flood fill segmentation

4. **Homography & Perspective**
   - Perspective transformation
   - Texture warping with homography
   - Rectification of regions
   - Distortion correction

5. **Texture Generation**
   - Procedural wood texture
   - Marble texture with veins
   - Carpet texture
   - Tile patterns with grout
   - Brick patterns
   - Concrete texture
   - Brightness adjustment
   - Texture tiling

#### Frontend (React)

1. **User Interface**
   - Modern, responsive design
   - Drag-and-drop image upload
   - Interactive canvas for region selection
   - Real-time preview

2. **Texture Library**
   - 12 built-in textures
   - Visual texture preview grid
   - Easy selection interface

3. **Controls**
   - Opacity slider (0-100%)
   - Brightness adjustment (-50 to +50)
   - Blend modes (Normal, Multiply, Overlay, Soft Light)
   - Perspective correction toggle

4. **Processing**
   - Automatic surface detection
   - Manual region selection
   - Real-time texture application
   - Image export (PNG)

### 🔄 Planned Features

- Deep learning segmentation (UNet, DeepLab, SAM)
- Advanced lighting simulation
- Multi-surface support
- Undo/redo functionality
- Project save/load
- Batch processing

---

## API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "RenderEase API is running"
}
```

#### 2. Edge Detection
```http
POST /edge-detection
```
**Request Body:**
```json
{
  "image": "data:image/png;base64,...",
  "method": "canny",
  "params": {
    "low_threshold": 50,
    "high_threshold": 150
  }
}
```
**Response:**
```json
{
  "success": true,
  "edges": "data:image/png;base64,...",
  "method": "canny"
}
```

#### 3. Line Detection (Hough Transform)
```http
POST /detect-lines
```
**Request Body:**
```json
{
  "image": "data:image/png;base64,...",
  "params": {
    "threshold": 100,
    "min_line_length": 50,
    "max_line_gap": 10
  }
}
```
**Response:**
```json
{
  "success": true,
  "image": "data:image/png;base64,...",
  "lines": [
    {"x1": 10, "y1": 20, "x2": 100, "y2": 120, "rho": 45.5, "theta": 1.57}
  ],
  "count": 15
}
```

#### 4. Image Segmentation
```http
POST /segment
```
**Request Body:**
```json
{
  "image": "data:image/png;base64,...",
  "method": "color",
  "params": {
    "lower_bound": [0, 0, 0],
    "upper_bound": [255, 255, 255],
    "color_space": "HSV"
  }
}
```

#### 5. Generate Texture
```http
POST /generate-texture
```
**Request Body:**
```json
{
  "type": "wood",
  "width": 512,
  "height": 512,
  "params": {
    "base_color": [139, 69, 19]
  }
}
```

#### 6. Apply Texture
```http
POST /apply-texture
```
**Request Body:**
```json
{
  "image": "data:image/png;base64,...",
  "texture": "data:image/png;base64,...",
  "corners": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],
  "blend_alpha": 0.8,
  "brightness": 0.0
}
```

#### 7. Detect Surfaces
```http
POST /detect-surfaces
```
Automatically detects edges, lines, and corner points.

#### 8. Complete Processing Pipeline
```http
POST /process-complete
```
End-to-end processing with auto-detection and texture application.

---

## Usage Guide

### Basic Workflow

1. **Upload Image**
   - Click "Choose Image" or drag & drop
   - Supported formats: JPG, PNG, BMP
   - Max size: 16MB

2. **Detect Surfaces** (Optional)
   - Click "Detect Edges" for Canny edge detection
   - Click "Detect Surfaces" for automatic Hough line detection
   - Or manually select a region with click & drag

3. **Select Texture**
   - Choose from 12 built-in textures
   - Textures include: wood, marble, carpet, tile, brick, concrete

4. **Adjust Settings**
   - **Opacity:** How transparent the texture is (80% recommended)
   - **Brightness:** Adjust to match room lighting
   - **Blend Mode:** How texture mixes with original
   - **Perspective Correction:** Enable for realistic depth

5. **Apply & Save**
   - Click "Apply Texture" to render
   - Use "Reset" to return to original
   - Click "Save Result" to download PNG

### Tips for Best Results

- **Image Quality:** Higher resolution = better results
- **Lighting:** Even lighting works best
- **Selection:** Select entire surface area
- **Blend Modes:**
  - Normal: Direct overlay
  - Multiply: Darkens (good for floors)
  - Overlay: Preserves detail (good for walls)
  - Soft Light: Subtle effect

---

## Computer Vision Algorithms

### 1. Edge Detection (`edge_detector.py`)

**Canny Edge Detection**
- Multi-stage algorithm for optimal edge detection
- Gaussian blur → Gradient calculation → Non-maximum suppression → Hysteresis thresholding

**Sobel Edge Detection**
- Gradient-based edge detection
- Calculates first derivative of image intensity

**Laplacian Edge Detection**
- Second derivative operator
- Finds rapid intensity changes

### 2. Hough Transform (`hough_transform.py`)

**Line Detection**
- Converts lines to parameter space (rho, theta)
- Votes for lines in accumulator
- Probabilistic variant for efficiency

**Circle Detection**
- Specialized for circular shapes
- Three-parameter space (x, y, radius)

**Applications:**
- Floor/ceiling boundary detection
- Wall edge detection
- Corner point identification

### 3. Segmentation (`segmentation.py`)

**Color-Based**
- Segments by color range in HSV/LAB space
- Good for uniform colored surfaces

**GrabCut**
- Graph-cut based interactive segmentation
- User provides rough bounding box

**Watershed**
- Topology-based segmentation
- Treats image as topographic surface

**K-means Clustering**
- Clusters pixels by color similarity
- K = number of desired segments

### 4. Homography (`homography.py`)

**Perspective Transformation**
- 3x3 matrix mapping between two planes
- Essential for realistic texture application

**Applications:**
- Warp texture to match perspective
- Rectify tilted surfaces
- Apply textures to quadrilaterals

---

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
python app.py

# Or with Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Frontend Development

```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Adding New CV Algorithms

1. Create new module in `backend/cv_algorithms/`
2. Implement algorithm class with methods
3. Add API endpoint in `backend/app.py`
4. Update frontend `services/api.js`
5. Add UI controls in React components

---

## Dependencies

### Backend (Python)

```
Flask==3.0.0              # Web framework
Flask-CORS==4.0.0         # Cross-origin support
opencv-python==4.8.1.78   # Computer vision
numpy==1.24.3             # Numerical computing
Pillow==10.1.0            # Image processing
```

### Frontend (JavaScript)

```
react==18.2.0             # UI framework
react-dom==18.2.0         # React DOM renderer
axios==1.6.0              # HTTP client
react-scripts==5.0.1      # Build tools
```

---

## Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>

# Or change port in app.py
app.run(port=5001)
```

**OpenCV import error:**
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python==4.8.1.78
```

**Virtual environment issues:**
```bash
rm -rf backend/venv
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Kill process on port 3000
lsof -i :3000
kill -9 <PID>

# Or use different port
PORT=3001 npm start
```

**Node modules issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Ensure backend is running on port 5000
- Check `frontend/.env` has correct API URL
- Verify Flask-CORS is installed

---

## Performance

### Optimization Tips

**Backend:**
- Use smaller images for testing
- Enable caching for textures
- Reduce line detection threshold for faster processing

**Frontend:**
- Compress images before upload
- Debounce slider inputs
- Use React.memo for expensive components

### Benchmarks

| Operation | Average Time |
|-----------|--------------|
| Image Upload | < 1s |
| Edge Detection | 200-500ms |
| Hough Transform | 500-1000ms |
| Texture Generation | 100-300ms |
| Texture Application | 500-1500ms |

*(Tested on 800x600px images)*

---

## Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Test individual modules
python -m cv_algorithms.edge_detector
python -m cv_algorithms.hough_transform

# Test API endpoints
curl http://localhost:5000/api/health
```

### Frontend Testing

```bash
cd frontend

# Run unit tests
npm test

# Generate coverage report
npm test -- --coverage
```

---

## Deployment

### Production Build

**Backend:**
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Frontend:**
```bash
cd frontend
npm run build
# Deploy 'build' folder to static hosting
```

### Docker (Future)

```dockerfile
# Example Dockerfile for backend
FROM python:3.9
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "app.py"]
```

---

## Contributing

This is an academic project for COMP SCI 566. For questions or contributions:

- Bhinu Puvva: puvvala@wisc.edu
- Bala Shukla: shukla35@wisc.edu
- Rain Jiayu Sun: jsun424@wisc.edu

---

## License

Academic project for University of Wisconsin-Madison COMP SCI 566.
All rights reserved by the team members.

---

## Acknowledgments

- **Course:** COMP SCI 566 - Intro to Computer Vision
- **Institution:** University of Wisconsin-Madison
- **Frameworks:** Flask, React, OpenCV
- **Inspiration:** Professional interior design tools

---

## Changelog

### v2.0 (Current) - Full Stack Architecture
- ✅ Flask backend with REST API
- ✅ React frontend with modern UI
- ✅ Separate CV algorithm modules
- ✅ Comprehensive API endpoints
- ✅ Real-time processing

### v1.0 - Initial Prototype
- Basic vanilla JavaScript implementation
- Client-side processing only
- Limited CV capabilities

---

**Last Updated:** October 28, 2025
