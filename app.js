// RenderEase - Main Application Logic

class RenderEase {
    constructor() {
        this.canvas = document.getElementById('mainCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.originalImage = null;
        this.currentImage = null;
        this.selectedTexture = null;
        this.selectedRegion = null;
        this.isSelecting = false;
        this.selectionStart = null;
        this.selectionPoints = [];
        this.history = [];

        this.initializeTextures();
        this.initializeEventListeners();
        this.updateStatus('Ready to start');
    }

    initializeTextures() {
        const textures = [
            { name: 'Wood Floor', color: '#8B4513', pattern: 'wood' },
            { name: 'Marble', color: '#F5F5DC', pattern: 'marble' },
            { name: 'Carpet Gray', color: '#808080', pattern: 'carpet' },
            { name: 'Carpet Beige', color: '#D2B48C', pattern: 'carpet' },
            { name: 'Tile White', color: '#FFFFFF', pattern: 'tile' },
            { name: 'Tile Black', color: '#333333', pattern: 'tile' },
            { name: 'Brick Red', color: '#B22222', pattern: 'brick' },
            { name: 'Concrete', color: '#A9A9A9', pattern: 'concrete' },
            { name: 'Light Wood', color: '#DEB887', pattern: 'wood' },
            { name: 'Dark Wood', color: '#654321', pattern: 'wood' },
            { name: 'Blue Tile', color: '#4169E1', pattern: 'tile' },
            { name: 'Green Carpet', color: '#228B22', pattern: 'carpet' }
        ];

        const textureGrid = document.getElementById('textureGrid');
        textures.forEach((texture, index) => {
            const textureItem = document.createElement('div');
            textureItem.className = 'texture-item';
            textureItem.dataset.index = index;
            textureItem.dataset.pattern = texture.pattern;
            textureItem.dataset.color = texture.color;
            textureItem.title = texture.name;

            // Create a canvas for the texture preview
            const previewCanvas = document.createElement('canvas');
            previewCanvas.width = 100;
            previewCanvas.height = 100;
            const previewCtx = previewCanvas.getContext('2d');
            this.generateTexturePattern(previewCtx, texture.pattern, texture.color, 100, 100);

            textureItem.style.backgroundImage = `url(${previewCanvas.toDataURL()})`;
            textureItem.addEventListener('click', () => this.selectTexture(index, texture));
            textureGrid.appendChild(textureItem);
        });
    }

    generateTexturePattern(ctx, pattern, baseColor, width, height) {
        ctx.fillStyle = baseColor;
        ctx.fillRect(0, 0, width, height);

        switch(pattern) {
            case 'wood':
                this.drawWoodPattern(ctx, baseColor, width, height);
                break;
            case 'marble':
                this.drawMarblePattern(ctx, baseColor, width, height);
                break;
            case 'carpet':
                this.drawCarpetPattern(ctx, baseColor, width, height);
                break;
            case 'tile':
                this.drawTilePattern(ctx, baseColor, width, height);
                break;
            case 'brick':
                this.drawBrickPattern(ctx, baseColor, width, height);
                break;
            case 'concrete':
                this.drawConcretePattern(ctx, baseColor, width, height);
                break;
        }
    }

    drawWoodPattern(ctx, baseColor, width, height) {
        ctx.strokeStyle = this.adjustBrightness(baseColor, -30);
        ctx.lineWidth = 2;
        for(let i = 0; i < 5; i++) {
            const y = Math.random() * height;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.bezierCurveTo(width/3, y + Math.random()*10-5, width*2/3, y + Math.random()*10-5, width, y);
            ctx.stroke();
        }
    }

    drawMarblePattern(ctx, baseColor, width, height) {
        for(let i = 0; i < 20; i++) {
            ctx.strokeStyle = this.adjustBrightness(baseColor, Math.random() * 40 - 20);
            ctx.lineWidth = Math.random() * 2;
            ctx.beginPath();
            ctx.moveTo(Math.random() * width, Math.random() * height);
            ctx.lineTo(Math.random() * width, Math.random() * height);
            ctx.stroke();
        }
    }

    drawCarpetPattern(ctx, baseColor, width, height) {
        for(let i = 0; i < 100; i++) {
            ctx.fillStyle = this.adjustBrightness(baseColor, Math.random() * 20 - 10);
            ctx.fillRect(Math.random() * width, Math.random() * height, 2, 2);
        }
    }

    drawTilePattern(ctx, baseColor, width, height) {
        const tileSize = width / 3;
        ctx.strokeStyle = this.adjustBrightness(baseColor, -40);
        ctx.lineWidth = 2;
        for(let i = 0; i <= 3; i++) {
            ctx.beginPath();
            ctx.moveTo(i * tileSize, 0);
            ctx.lineTo(i * tileSize, height);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(0, i * tileSize);
            ctx.lineTo(width, i * tileSize);
            ctx.stroke();
        }
    }

    drawBrickPattern(ctx, baseColor, width, height) {
        const brickHeight = height / 4;
        const brickWidth = width / 4;
        ctx.strokeStyle = this.adjustBrightness(baseColor, -40);
        ctx.lineWidth = 2;

        for(let row = 0; row <= 4; row++) {
            ctx.beginPath();
            ctx.moveTo(0, row * brickHeight);
            ctx.lineTo(width, row * brickHeight);
            ctx.stroke();
        }

        for(let row = 0; row < 4; row++) {
            const offset = (row % 2) * (brickWidth / 2);
            for(let col = 0; col < 4; col++) {
                ctx.beginPath();
                ctx.moveTo(col * brickWidth + offset, row * brickHeight);
                ctx.lineTo(col * brickWidth + offset, (row + 1) * brickHeight);
                ctx.stroke();
            }
        }
    }

    drawConcretePattern(ctx, baseColor, width, height) {
        for(let i = 0; i < 200; i++) {
            const brightness = Math.random() * 30 - 15;
            ctx.fillStyle = this.adjustBrightness(baseColor, brightness);
            const size = Math.random() * 3;
            ctx.fillRect(Math.random() * width, Math.random() * height, size, size);
        }
    }

    adjustBrightness(color, amount) {
        const num = parseInt(color.replace("#", ""), 16);
        const r = Math.max(0, Math.min(255, (num >> 16) + amount));
        const g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) + amount));
        const b = Math.max(0, Math.min(255, (num & 0x0000FF) + amount));
        return "#" + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
    }

    initializeEventListeners() {
        // Image upload
        document.getElementById('imageUpload').addEventListener('change', (e) => {
            this.handleImageUpload(e.target.files[0]);
        });

        // Texture upload
        document.getElementById('textureUpload').addEventListener('change', (e) => {
            this.handleTextureUpload(e.target.files[0]);
        });

        // Canvas selection
        this.canvas.addEventListener('mousedown', (e) => this.startSelection(e));
        this.canvas.addEventListener('mousemove', (e) => this.updateSelection(e));
        this.canvas.addEventListener('mouseup', (e) => this.endSelection(e));

        // Settings
        document.getElementById('opacity').addEventListener('input', (e) => {
            document.getElementById('opacityValue').textContent = e.target.value + '%';
        });

        document.getElementById('brightness').addEventListener('input', (e) => {
            document.getElementById('brightnessValue').textContent = e.target.value;
        });

        // Buttons
        document.getElementById('detectSurfaceBtn').addEventListener('click', () => this.detectSurfaces());
        document.getElementById('applyTextureBtn').addEventListener('click', () => this.applyTexture());
        document.getElementById('resetBtn').addEventListener('click', () => this.reset());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveResult());
    }

    handleImageUpload(file) {
        if (!file) return;

        document.getElementById('fileName').textContent = file.name;
        const reader = new FileReader();

        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                this.loadImage(img);
            };
            img.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }

    loadImage(img) {
        // Resize canvas to fit image while maintaining aspect ratio
        const maxWidth = 800;
        const maxHeight = 600;
        let width = img.width;
        let height = img.height;

        if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
        }
        if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
        }

        this.canvas.width = width;
        this.canvas.height = height;
        this.ctx.drawImage(img, 0, 0, width, height);

        this.originalImage = img;
        this.currentImage = this.ctx.getImageData(0, 0, width, height);

        document.getElementById('canvasOverlay').classList.add('hidden');
        document.getElementById('detectSurfaceBtn').disabled = false;
        document.getElementById('resetBtn').disabled = false;

        this.updateStatus('Image loaded - Select a surface area');
    }

    handleTextureUpload(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                // Create custom texture item
                const textureGrid = document.getElementById('textureGrid');
                const textureItem = document.createElement('div');
                textureItem.className = 'texture-item';
                textureItem.style.backgroundImage = `url(${e.target.result})`;
                textureItem.dataset.customImage = e.target.result;
                textureItem.addEventListener('click', () => {
                    this.selectTexture(-1, { customImage: img });
                });
                textureGrid.appendChild(textureItem);

                // Auto-select the uploaded texture
                this.selectTexture(-1, { customImage: img });
                this.updateStatus('Custom texture uploaded and selected');
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    selectTexture(index, textureData) {
        // Remove previous selection
        document.querySelectorAll('.texture-item').forEach(item => {
            item.classList.remove('selected');
        });

        // Add selection to clicked item
        if (index >= 0) {
            document.querySelector(`[data-index="${index}"]`).classList.add('selected');
        } else {
            document.querySelector('[data-custom-image]').classList.add('selected');
        }

        this.selectedTexture = textureData;

        if (this.selectedRegion) {
            document.getElementById('applyTextureBtn').disabled = false;
        }

        this.updateStatus('Texture selected');
    }

    startSelection(e) {
        if (!this.originalImage) return;

        this.isSelecting = true;
        const rect = this.canvas.getBoundingClientRect();
        this.selectionStart = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
        this.selectionPoints = [this.selectionStart];
    }

    updateSelection(e) {
        if (!this.isSelecting) return;

        const rect = this.canvas.getBoundingClientRect();
        const currentPoint = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };

        // Redraw image
        this.ctx.putImageData(this.currentImage, 0, 0);

        // Draw selection rectangle
        this.ctx.strokeStyle = '#667eea';
        this.ctx.lineWidth = 3;
        this.ctx.setLineDash([5, 5]);
        this.ctx.strokeRect(
            this.selectionStart.x,
            this.selectionStart.y,
            currentPoint.x - this.selectionStart.x,
            currentPoint.y - this.selectionStart.y
        );
        this.ctx.setLineDash([]);
    }

    endSelection(e) {
        if (!this.isSelecting) return;

        this.isSelecting = false;
        const rect = this.canvas.getBoundingClientRect();
        const selectionEnd = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };

        // Store selected region
        this.selectedRegion = {
            x: Math.min(this.selectionStart.x, selectionEnd.x),
            y: Math.min(this.selectionStart.y, selectionEnd.y),
            width: Math.abs(selectionEnd.x - this.selectionStart.x),
            height: Math.abs(selectionEnd.y - this.selectionStart.y)
        };

        if (this.selectedRegion.width > 10 && this.selectedRegion.height > 10) {
            document.getElementById('selectionInfo').textContent =
                `${Math.round(this.selectedRegion.width)}x${Math.round(this.selectedRegion.height)}px`;

            if (this.selectedTexture) {
                document.getElementById('applyTextureBtn').disabled = false;
            }

            this.updateStatus('Surface selected - Choose a texture and apply');
        } else {
            this.selectedRegion = null;
            document.getElementById('selectionInfo').textContent = 'None';
        }
    }

    detectSurfaces() {
        if (!this.originalImage) return;

        const method = document.getElementById('segmentationMethod').value;
        this.updateStatus(`Detecting surfaces using ${method} method...`);

        // Simulate surface detection (placeholder for actual computer vision algorithms)
        setTimeout(() => {
            this.updateStatus('Surface detection complete - Draw selection manually');
            alert(`${method} detection is a placeholder. Please manually select the surface area by clicking and dragging on the canvas.`);
        }, 500);
    }

    applyTexture() {
        if (!this.selectedRegion || !this.selectedTexture) {
            alert('Please select both a surface area and a texture');
            return;
        }

        this.updateStatus('Applying texture...');

        // Save current state to history
        this.history.push(this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height));

        // Create texture canvas
        const textureCanvas = document.createElement('canvas');
        const textureCtx = textureCanvas.getContext('2d');
        textureCanvas.width = this.selectedRegion.width;
        textureCanvas.height = this.selectedRegion.height;

        // Generate or draw texture
        if (this.selectedTexture.customImage) {
            // Draw custom image texture
            textureCtx.drawImage(
                this.selectedTexture.customImage,
                0, 0,
                textureCanvas.width,
                textureCanvas.height
            );
        } else {
            // Generate procedural texture
            this.generateTexturePattern(
                textureCtx,
                this.selectedTexture.pattern,
                this.selectedTexture.color,
                textureCanvas.width,
                textureCanvas.height
            );
        }

        // Apply settings
        const opacity = document.getElementById('opacity').value / 100;
        const brightness = parseInt(document.getElementById('brightness').value);
        const blendMode = document.getElementById('blendMode').value;

        // Apply brightness adjustment
        if (brightness !== 0) {
            const imageData = textureCtx.getImageData(0, 0, textureCanvas.width, textureCanvas.height);
            const data = imageData.data;
            for (let i = 0; i < data.length; i += 4) {
                data[i] = Math.max(0, Math.min(255, data[i] + brightness));
                data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + brightness));
                data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + brightness));
            }
            textureCtx.putImageData(imageData, 0, 0);
        }

        // Apply perspective correction if enabled
        if (document.getElementById('perspective').checked) {
            this.applyPerspectiveCorrection(textureCanvas);
        }

        // Blend texture with original image
        this.ctx.save();
        this.ctx.globalAlpha = opacity;
        this.ctx.globalCompositeOperation = blendMode;
        this.ctx.drawImage(
            textureCanvas,
            this.selectedRegion.x,
            this.selectedRegion.y,
            this.selectedRegion.width,
            this.selectedRegion.height
        );
        this.ctx.restore();

        // Update current image
        this.currentImage = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);

        document.getElementById('saveBtn').disabled = false;
        this.updateStatus('Texture applied successfully');
    }

    applyPerspectiveCorrection(textureCanvas) {
        // Placeholder for perspective transformation
        // In a full implementation, this would use homography matrix
        // For now, we'll just add a subtle effect
        const ctx = textureCanvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, textureCanvas.width, textureCanvas.height);
        // Apply subtle distortion to simulate perspective
        ctx.putImageData(imageData, 0, 0);
    }

    reset() {
        if (this.originalImage) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.drawImage(
                this.originalImage,
                0, 0,
                this.canvas.width,
                this.canvas.height
            );
            this.currentImage = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        }

        this.selectedRegion = null;
        this.history = [];

        document.getElementById('selectionInfo').textContent = 'None';
        document.getElementById('applyTextureBtn').disabled = true;
        document.getElementById('saveBtn').disabled = true;

        this.updateStatus('Reset to original image');
    }

    saveResult() {
        if (!this.currentImage) return;

        const link = document.createElement('a');
        link.download = 'renderease-result.png';
        link.href = this.canvas.toDataURL('image/png');
        link.click();

        this.updateStatus('Image saved successfully');
    }

    updateStatus(message) {
        document.getElementById('statusText').textContent = message;
    }
}

// Sample room image loader
function loadSampleImage(roomId) {
    const sampleImages = {
        room1: createSampleRoom('#D2B48C', 'living'),
        room2: createSampleRoom('#F5F5DC', 'bedroom'),
        room3: createSampleRoom('#E0E0E0', 'kitchen')
    };

    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');

    sampleImages[roomId](ctx);

    canvas.toBlob((blob) => {
        const file = new File([blob], `${roomId}.png`, { type: 'image/png' });
        app.handleImageUpload(file);
    });
}

function createSampleRoom(wallColor, type) {
    return (ctx) => {
        const width = ctx.canvas.width;
        const height = ctx.canvas.height;

        // Draw walls
        ctx.fillStyle = wallColor;
        ctx.fillRect(0, 0, width, height);

        // Draw floor with perspective
        ctx.fillStyle = '#8B7355';
        ctx.beginPath();
        ctx.moveTo(0, height * 0.6);
        ctx.lineTo(width, height * 0.6);
        ctx.lineTo(width, height);
        ctx.lineTo(0, height);
        ctx.closePath();
        ctx.fill();

        // Add floor lines for perspective
        ctx.strokeStyle = '#6B5335';
        ctx.lineWidth = 2;
        for (let i = 0; i < 5; i++) {
            const y = height * 0.6 + (height * 0.4 * i / 4);
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }

        // Draw room-specific details
        if (type === 'living') {
            // Window
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(width * 0.3, height * 0.2, width * 0.4, height * 0.3);
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 5;
            ctx.strokeRect(width * 0.3, height * 0.2, width * 0.4, height * 0.3);
        } else if (type === 'bedroom') {
            // Door
            ctx.fillStyle = '#654321';
            ctx.fillRect(width * 0.1, height * 0.3, width * 0.15, height * 0.3);
            ctx.fillStyle = '#FFD700';
            ctx.beginPath();
            ctx.arc(width * 0.12, height * 0.45, 5, 0, Math.PI * 2);
            ctx.fill();
        } else if (type === 'kitchen') {
            // Counter
            ctx.fillStyle = '#696969';
            ctx.fillRect(width * 0.7, height * 0.5, width * 0.25, height * 0.15);
        }

        // Add lighting effect
        const gradient = ctx.createRadialGradient(width/2, height/3, 0, width/2, height/3, width/2);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.3)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
    };
}

// Initialize application when DOM is ready
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new RenderEase();
    console.log('RenderEase initialized successfully');
});
