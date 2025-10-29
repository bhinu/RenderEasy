# RenderEase - Interior Design Visualization Tool

A web-based application for visualizing interior design changes in real-time, allowing designers and clients to preview how different textures, materials, and finishes will look on surfaces like floors, walls, and ceilings.

## Team
- **Bhinu Puvva** - puvvala@wisc.edu
- **Bala Shukla** - shukla35@wisc.edu
- **Rain Jiayu Sun** - jsun424@wisc.edu

**Course:** COMP SCI 566 - Intro to Computer Vision
**Institution:** University of Wisconsin-Madison

## Problem Statement

Interior designers need to quickly visualize how surfaces will look with different materials and finishes. Current solutions are either:
- Expensive (Photoshop, CAD tools)
- Require specialized expertise
- Fragmented across multiple applications
- Not easily accessible to clients

RenderEase solves this by providing a streamlined, web-based visualization tool that's fast, intuitive, and requires no installation.

## Features

### Current Implementation

1. **Image Upload & Management**
   - Upload custom room images
   - Built-in sample rooms for testing
   - Automatic canvas resizing and aspect ratio preservation

2. **Surface Selection**
   - Interactive click-and-drag selection
   - Visual selection feedback
   - Selection dimension display

3. **Texture Library**
   - 12 built-in procedural textures:
     - Wood (Light, Dark, Standard)
     - Marble
     - Carpet (Gray, Beige, Green)
     - Tile (White, Black, Blue)
     - Brick
     - Concrete
   - Custom texture upload support
   - Real-time texture preview generation

4. **Texture Application**
   - Multiple blend modes (Normal, Multiply, Overlay, Soft Light)
   - Adjustable opacity (0-100%)
   - Brightness adjustment (-50 to +50)
   - Perspective correction toggle

5. **Export & Save**
   - Save final result as PNG
   - High-quality image export
   - Reset to original functionality

### Planned Enhancements

According to the project timeline, future phases will include:

- **Advanced Surface Detection**
  - Edge detection using Canny algorithm
  - Hough Transform for line and corner detection
  - Color-based segmentation
  - Binary mask creation

- **Deep Learning Integration**
  - UNet, DeepLab, or Segment Anything (SAM) models
  - Automatic surface segmentation
  - Comparison with traditional methods

- **Enhanced Rendering**
  - Homography-based perspective warping
  - Advanced lighting correction
  - Shadow preservation
  - Realistic material properties

## Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Graphics:** HTML5 Canvas API
- **Architecture:** Single Page Application (SPA)
- **No Dependencies:** Pure vanilla JavaScript - no frameworks required

## Installation & Usage

### Option 1: Direct Browser Opening
1. Clone or download this repository
2. Open `index.html` in a modern web browser
3. Start designing!

### Option 2: Local Server (Recommended)
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx http-server

# Using PHP
php -S localhost:8000
```

Then navigate to `http://localhost:8000` in your browser.

## How to Use

### Step-by-Step Guide

1. **Upload Room Image**
   - Click "Choose Image" to upload your room photo
   - Or click one of the sample room buttons to test with generated rooms

2. **Select Surface**
   - Click and drag on the canvas to select the area you want to modify
   - The selected region will be highlighted with a dashed border
   - Selection dimensions appear in the info panel

3. **Choose Texture**
   - Click on any texture in the library to select it
   - Or upload your own texture using "Upload Custom Texture"
   - Selected texture will have a blue border

4. **Adjust Settings**
   - **Blend Mode:** Changes how the texture mixes with the original image
   - **Opacity:** Controls transparency (80% recommended)
   - **Brightness:** Adjust to match room lighting
   - **Perspective Correction:** Enable for realistic depth

5. **Apply & Save**
   - Click "Apply Texture" to render the changes
   - Use "Reset" to return to the original image
   - Click "Save Result" to download the final image

## Project Structure

```
566 Final Project/
│
├── index.html          # Main HTML structure
├── styles.css          # Complete styling and layout
├── app.js             # Core application logic
└── README.md          # This file
```

## Technical Implementation Details

### Image Processing Pipeline

1. **Image Loading**
   - File input handling with FileReader API
   - Dynamic canvas sizing with aspect ratio preservation
   - ImageData capture for manipulation

2. **Selection System**
   - Mouse event handling for interactive selection
   - Rectangular selection with visual feedback
   - Region coordinate storage

3. **Texture Generation**
   - Procedural texture generation using canvas patterns
   - Custom algorithms for wood, marble, carpet, tile, brick, and concrete
   - Color manipulation and brightness adjustment

4. **Texture Application**
   - Canvas compositing operations
   - Multiple blend modes support
   - Alpha blending for opacity control
   - Pixel-level brightness manipulation

5. **Export**
   - Canvas to PNG conversion
   - Blob generation and download

### Key Algorithms

**Procedural Texture Generation:**
- Wood: Bezier curves for grain patterns
- Marble: Random stroke veining
- Carpet: Noise-based fiber simulation
- Tile: Grid-based grout lines
- Brick: Offset row patterns
- Concrete: Multi-scale noise

**Color Manipulation:**
```javascript
adjustBrightness(color, amount) {
    const num = parseInt(color.replace("#", ""), 16);
    const r = Math.max(0, Math.min(255, (num >> 16) + amount));
    const g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) + amount));
    const b = Math.max(0, Math.min(255, (num & 0x0000FF) + amount));
    return "#" + ((r << 16) | (g << 8) | b).toString(16);
}
```

## Development Timeline

### Phase 1: Foundation (Weeks 1-2) ✅ COMPLETED
- [x] Environment setup
- [x] Data gathering and sample creation
- [x] Basic GUI implementation
- [x] Image upload and display

### Phase 2: Core Features (Weeks 3-4) ✅ COMPLETED
- [x] Surface selection interface
- [x] Texture library implementation
- [x] Basic texture application
- [x] Perspective correction placeholder

### Phase 3: Enhancement (Weeks 5-6) 🔄 IN PROGRESS
- [ ] Edge detection implementation (Canny)
- [ ] Hough Transform for lines/corners
- [ ] Advanced lighting adjustments
- [ ] Realistic blending improvements

### Phase 4: Advanced (Week 7) 📅 PLANNED
- [ ] Deep learning model integration
- [ ] Automatic segmentation (UNet/DeepLab/SAM)
- [ ] Performance comparison tools
- [ ] Model evaluation metrics

### Phase 5: Finalization (Week 8) 📅 PLANNED
- [ ] Comprehensive testing
- [ ] Bug fixes and optimization
- [ ] Documentation completion
- [ ] Final presentation preparation

## Browser Compatibility

- ✅ Chrome 90+ (Recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Note:** Requires JavaScript and HTML5 Canvas support.

## Performance Considerations

- Images automatically resized to max 800x600px for performance
- Canvas operations optimized for real-time interaction
- Procedural textures generated on-demand
- Minimal memory footprint (~5-10MB typical usage)

## Future Enhancements

### Computer Vision Features
- [ ] Automatic floor/wall/ceiling detection
- [ ] Semantic segmentation using deep learning
- [ ] Lighting condition analysis
- [ ] Shadow and reflection preservation
- [ ] 3D perspective transformation with homography matrices

### User Experience
- [ ] Undo/Redo functionality
- [ ] Multiple selection support
- [ ] Layer management
- [ ] Before/After comparison slider
- [ ] Mobile responsive design
- [ ] Touch gesture support

### Texture Library
- [ ] Expanded texture database (50+ textures)
- [ ] Texture search and filtering
- [ ] User-contributed texture sharing
- [ ] Texture scaling and rotation
- [ ] Seamless pattern generation

### Professional Features
- [ ] Project save/load
- [ ] Multi-room project support
- [ ] Client collaboration tools
- [ ] Cost estimation integration
- [ ] Material supplier links

## Known Limitations

1. **Perspective Correction:** Current implementation is a placeholder; full homography transformation pending
2. **Surface Detection:** Automatic detection requires implementation of computer vision algorithms
3. **Lighting:** Basic brightness adjustment only; advanced lighting simulation planned
4. **Selection:** Currently limited to rectangular selections; polygon/freeform selection planned

## Methodology Comparison

### Traditional Approach
- Edge detection (Canny)
- Hough Transform
- Homography warping
- Mask-based blending

**Pros:** Interpretable, lightweight, fast
**Cons:** Requires manual tuning, less robust to complex scenes

### Deep Learning Approach
- Pre-trained segmentation models
- Automatic feature learning
- Robust to variations

**Pros:** More accurate, handles complex scenes
**Cons:** Requires computation resources, less interpretable

### Our Hybrid Approach
We aim to provide both methods, allowing users to:
- Start with fast traditional methods
- Fall back to deep learning for difficult cases
- Compare results side-by-side
- Choose based on speed/accuracy tradeoffs

## Contributing

This is an academic project for COMP SCI 566. For questions or contributions:

- **Bhinu Puvva:** puvvala@wisc.edu
- **Bala Shukla:** shukla35@wisc.edu
- **Rain Jiayu Sun:** jsun424@wisc.edu

## License

Academic project for University of Wisconsin-Madison COMP SCI 566.
All rights reserved by the team members.

## Acknowledgments

- Course: COMP SCI 566 - Intro to Computer Vision
- Institution: University of Wisconsin-Madison
- Inspiration: Professional interior design software and AR visualization tools

## References

1. Canvas API Documentation: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
2. Computer Vision: Algorithms and Applications (Szeliski, 2022)
3. Deep Learning for Semantic Segmentation: UNet, DeepLab, SAM
4. Perspective Transformation and Homography Estimation
5. Canny Edge Detection and Hough Transform

---

**Built with ❤️ for Interior Designers and Computer Vision Enthusiasts**

Last Updated: October 2025
