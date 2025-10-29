import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import ImageUploader from './components/ImageUploader';
import Canvas from './components/Canvas';
import TextureLibrary from './components/TextureLibrary';
import Controls from './components/Controls';
import { apiService, fileToBase64 } from './services/api';

function App() {
  // State management
  const [originalImage, setOriginalImage] = useState(null);
  const [currentImage, setCurrentImage] = useState(null);
  const [selectedTexture, setSelectedTexture] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [status, setStatus] = useState('Ready to start');
  const [edges, setEdges] = useState(null);
  const [detectedLines, setDetectedLines] = useState([]);

  // Settings
  const [blendMode, setBlendMode] = useState('normal');
  const [opacity, setOpacity] = useState(80);
  const [brightness, setBrightness] = useState(0);
  const [perspectiveCorrection, setPerspectiveCorrection] = useState(true);

  // Handle image upload
  const handleImageUpload = async (file) => {
    try {
      setProcessing(true);
      setStatus('Loading image...');

      const imageData = await fileToBase64(file);
      setOriginalImage(imageData);
      setCurrentImage(imageData);

      setStatus('Image loaded successfully');
    } catch (error) {
      console.error('Error loading image:', error);
      setStatus('Error loading image');
    } finally {
      setProcessing(false);
    }
  };

  // Handle texture selection
  const handleTextureSelect = (texture) => {
    setSelectedTexture(texture);
    setStatus('Texture selected');
  };

  // Handle region selection from canvas
  const handleRegionSelect = (region) => {
    setSelectedRegion(region);
    setStatus(`Region selected: ${Math.round(region.width)}x${Math.round(region.height)}px`);
  };

  // Detect edges
  const handleEdgeDetection = async () => {
    if (!originalImage) return;

    try {
      setProcessing(true);
      setStatus('Detecting edges...');

      const result = await apiService.detectEdges(originalImage, 'canny', {
        low_threshold: 50,
        high_threshold: 150,
      });

      setEdges(result.edges);
      setStatus('Edge detection complete');
    } catch (error) {
      console.error('Error detecting edges:', error);
      setStatus('Error detecting edges');
    } finally {
      setProcessing(false);
    }
  };

  // Detect surfaces
  const handleSurfaceDetection = async () => {
    if (!originalImage) return;

    try {
      setProcessing(true);
      setStatus('Detecting surfaces...');

      const result = await apiService.detectSurfaces(originalImage);

      setCurrentImage(result.result);
      setEdges(result.edges);
      setDetectedLines({
        horizontal: result.horizontal_lines,
        vertical: result.vertical_lines,
        intersections: result.intersections,
      });

      setStatus(`Detected ${result.horizontal_lines} horizontal and ${result.vertical_lines} vertical lines`);
    } catch (error) {
      console.error('Error detecting surfaces:', error);
      setStatus('Error detecting surfaces');
    } finally {
      setProcessing(false);
    }
  };

  // Apply texture
  const handleApplyTexture = async () => {
    if (!originalImage || !selectedTexture || !selectedRegion) {
      setStatus('Please select an image, texture, and region');
      return;
    }

    try {
      setProcessing(true);
      setStatus('Applying texture...');

      // Generate or get texture
      let textureData = selectedTexture.data;

      if (!textureData) {
        // Generate texture from backend
        const texResult = await apiService.generateTexture(
          selectedTexture.type,
          selectedRegion.width,
          selectedRegion.height,
          { base_color: selectedTexture.color || [139, 69, 19] }
        );
        textureData = texResult.texture;
      }

      // Calculate corners from selected region
      const corners = [
        [selectedRegion.x, selectedRegion.y],
        [selectedRegion.x + selectedRegion.width, selectedRegion.y],
        [selectedRegion.x + selectedRegion.width, selectedRegion.y + selectedRegion.height],
        [selectedRegion.x, selectedRegion.y + selectedRegion.height],
      ];

      // Apply texture
      const result = await apiService.applyTexture(
        currentImage,
        textureData,
        corners,
        opacity / 100,
        brightness / 100
      );

      setCurrentImage(result.result);
      setStatus('Texture applied successfully');
    } catch (error) {
      console.error('Error applying texture:', error);
      setStatus('Error applying texture');
    } finally {
      setProcessing(false);
    }
  };

  // Reset to original
  const handleReset = () => {
    setCurrentImage(originalImage);
    setSelectedRegion(null);
    setEdges(null);
    setDetectedLines([]);
    setStatus('Reset to original');
  };

  // Save result
  const handleSave = () => {
    if (!currentImage) return;

    const link = document.createElement('a');
    link.download = 'renderease-result.png';
    link.href = currentImage;
    link.click();

    setStatus('Image saved successfully');
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>RenderEase</h1>
        <p className="subtitle">Interior Design Visualization Tool</p>
      </header>

      <main className="app-main">
        <aside className="control-panel">
          <section className="panel-section">
            <h2>1. Upload Room Image</h2>
            <ImageUploader onImageUpload={handleImageUpload} />
          </section>

          <section className="panel-section">
            <h2>2. Detect Surfaces</h2>
            <div className="detection-controls">
              <button
                className="btn btn-secondary"
                onClick={handleEdgeDetection}
                disabled={!originalImage || processing}
              >
                Detect Edges
              </button>
              <button
                className="btn btn-secondary"
                onClick={handleSurfaceDetection}
                disabled={!originalImage || processing}
              >
                Detect Surfaces (Hough)
              </button>
            </div>
            <p className="instruction-text">
              Or manually select a region on the canvas
            </p>
          </section>

          <section className="panel-section">
            <h2>3. Choose Texture</h2>
            <TextureLibrary
              onTextureSelect={handleTextureSelect}
              selectedTexture={selectedTexture}
            />
          </section>

          <section className="panel-section">
            <h2>4. Adjust Settings</h2>
            <Controls
              opacity={opacity}
              setOpacity={setOpacity}
              brightness={brightness}
              setBrightness={setBrightness}
              blendMode={blendMode}
              setBlendMode={setBlendMode}
              perspectiveCorrection={perspectiveCorrection}
              setPerspectiveCorrection={setPerspectiveCorrection}
            />
          </section>

          <section className="panel-section">
            <h2>5. Actions</h2>
            <div className="action-buttons">
              <button
                className="btn btn-primary"
                onClick={handleApplyTexture}
                disabled={!selectedTexture || !selectedRegion || processing}
              >
                {processing ? 'Processing...' : 'Apply Texture'}
              </button>
              <button
                className="btn btn-secondary"
                onClick={handleReset}
                disabled={!currentImage || processing}
              >
                Reset
              </button>
              <button
                className="btn btn-success"
                onClick={handleSave}
                disabled={!currentImage || processing}
              >
                Save Result
              </button>
            </div>
          </section>
        </aside>

        <div className="canvas-area">
          <Canvas
            image={currentImage}
            edgeImage={edges}
            onRegionSelect={handleRegionSelect}
            selectedRegion={selectedRegion}
          />

          <div className="status-bar">
            <div className="status-item">
              <span className="status-label">Status:</span>
              <span className="status-value">{status}</span>
            </div>
            {selectedRegion && (
              <div className="status-item">
                <span className="status-label">Selection:</span>
                <span className="status-value">
                  {Math.round(selectedRegion.width)}x{Math.round(selectedRegion.height)}px
                </span>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>
          RenderEase - COMP SCI 566 Project | Team: Bhinu Puvva, Bala Shukla, Rain Jiayu Sun
        </p>
      </footer>
    </div>
  );
}

export default App;
