import React, { useRef, useEffect, useState } from 'react';
import './Canvas.css';

function Canvas({ image, edgeImage, onRegionSelect, selectedRegion }) {
  const canvasRef = useRef(null);
  const [isSelecting, setIsSelecting] = useState(false);
  const [startPoint, setStartPoint] = useState(null);
  const [currentPoint, setCurrentPoint] = useState(null);

  // Draw image on canvas
  useEffect(() => {
    if (!image) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    const img = new Image();
    img.onload = () => {
      // Resize canvas to fit image
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

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);

      // Draw selected region if exists
      if (selectedRegion) {
        drawSelection(ctx, selectedRegion);
      }
    };
    img.src = image;
  }, [image, selectedRegion]);

  const drawSelection = (ctx, region) => {
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 3;
    ctx.setLineDash([5, 5]);
    ctx.strokeRect(region.x, region.y, region.width, region.height);
    ctx.setLineDash([]);
  };

  const handleMouseDown = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setIsSelecting(true);
    setStartPoint({ x, y });
    setCurrentPoint({ x, y });
  };

  const handleMouseMove = (e) => {
    if (!isSelecting) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setCurrentPoint({ x, y });

    // Redraw
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      // Draw selection
      ctx.strokeStyle = '#667eea';
      ctx.lineWidth = 3;
      ctx.setLineDash([5, 5]);
      ctx.strokeRect(
        startPoint.x,
        startPoint.y,
        x - startPoint.x,
        y - startPoint.y
      );
      ctx.setLineDash([]);
    };
    img.src = image;
  };

  const handleMouseUp = (e) => {
    if (!isSelecting) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setIsSelecting(false);

    const region = {
      x: Math.min(startPoint.x, x),
      y: Math.min(startPoint.y, y),
      width: Math.abs(x - startPoint.x),
      height: Math.abs(y - startPoint.y),
    };

    if (region.width > 10 && region.height > 10) {
      onRegionSelect(region);
    }

    setStartPoint(null);
    setCurrentPoint(null);
  };

  return (
    <div className="canvas-container">
      {image ? (
        <canvas
          ref={canvasRef}
          className="main-canvas"
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
        />
      ) : (
        <div className="canvas-placeholder">
          <p>Upload an image to get started</p>
        </div>
      )}
    </div>
  );
}

export default Canvas;
