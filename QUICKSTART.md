# RenderEase - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Open the Application

**Easiest Method:**
- Simply double-click `index.html` to open it in your default browser

**Alternative (Recommended for best performance):**
```bash
# In the project directory, run:
python3 -m http.server 8000

# Then open in browser:
# http://localhost:8000
```

### 2. Try the Demo

1. Click on one of the "Sample Room" buttons (Room 1, 2, or 3)
2. Click and drag on the floor area to select it
3. Click on any texture from the library (try "Wood Floor" or "Carpet Gray")
4. Click "Apply Texture" button
5. See the magic happen! ✨

### 3. Use Your Own Images

1. Click "Choose Image" and upload a photo of your room
2. Select the surface you want to change (floor, wall, etc.)
3. Choose a texture or upload your own
4. Adjust opacity and brightness to match your room's lighting
5. Click "Apply Texture"
6. Click "Save Result" to download your visualization

## 🎨 Tips for Best Results

### Taking Room Photos
- Use good lighting
- Take photos straight-on for walls and floors
- Avoid extreme angles
- Higher resolution = better results

### Selecting Surfaces
- Click and drag to create a selection box
- Try to select the entire surface area
- Avoid including furniture or objects
- Larger selections work better

### Applying Textures
- Start with 80% opacity
- Use "Multiply" blend mode for floors
- Use "Overlay" for walls
- Adjust brightness to match room lighting
- Enable "Perspective Correction" for realism

### Blend Modes Explained
- **Normal:** Direct overlay (best for first try)
- **Multiply:** Darkens (great for floors)
- **Overlay:** Preserves highlights and shadows (best for walls)
- **Soft Light:** Subtle effect (good for subtle changes)

## 🛠️ Troubleshooting

### Image Won't Load
- Ensure image is in JPG or PNG format
- Check file size (< 10MB recommended)
- Try refreshing the page

### Selection Not Working
- Make sure an image is loaded first
- Click and hold, then drag
- Selection must be at least 10x10 pixels

### Texture Looks Wrong
- Try different blend modes
- Adjust opacity (lower = more subtle)
- Adjust brightness to match room
- Try a different texture

### Can't See Changes
- Make sure you selected a surface area
- Make sure you selected a texture
- Check if opacity is too low
- Try clicking "Reset" and starting over

## 📱 Browser Requirements

Works best in:
- Chrome (recommended)
- Firefox
- Safari
- Edge

Requires JavaScript enabled.

## 💡 Example Workflows

### Workflow 1: Floor Change
1. Upload room image
2. Select floor area (usually bottom 40% of image)
3. Choose wood or carpet texture
4. Set blend mode to "Multiply"
5. Set opacity to 75-85%
6. Apply and save

### Workflow 2: Wall Paint
1. Upload room image
2. Select wall area
3. Upload custom paint color or choose texture
4. Set blend mode to "Overlay" or "Soft Light"
5. Set opacity to 60-70%
6. Adjust brightness if needed
7. Apply and save

### Workflow 3: Multiple Surfaces
1. Upload room image
2. Select floor → apply texture → note the result
3. Click "Apply Texture" again
4. Select wall → choose different texture
5. Apply again
6. Save final result

## 🎯 What to Expect

### Current Features (Phase 1-2)
✅ Manual surface selection
✅ 12 procedural textures
✅ Custom texture upload
✅ Real-time preview
✅ Multiple blend modes
✅ Export to PNG

### Coming Soon (Phase 3-4)
🔄 Automatic surface detection
🔄 AI-powered segmentation
🔄 Advanced lighting correction
🔄 3D perspective transformation

## 📚 Learn More

- Full documentation: See `README.md`
- Technical details: See comments in `app.js`
- Project proposal: Contact team members

## 🤝 Need Help?

Contact the development team:
- Bhinu Puvva: puvvala@wisc.edu
- Bala Shukla: shukla35@wisc.edu
- Rain Jiayu Sun: jsun424@wisc.edu

---

**Happy Designing! 🏠✨**
