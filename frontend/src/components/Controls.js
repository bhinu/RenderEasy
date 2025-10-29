import React from 'react';
import './Controls.css';

function Controls({
  opacity,
  setOpacity,
  brightness,
  setBrightness,
  blendMode,
  setBlendMode,
  perspectiveCorrection,
  setPerspectiveCorrection,
}) {
  return (
    <div className="controls">
      <div className="control-item">
        <label htmlFor="blendMode">Blend Mode:</label>
        <select
          id="blendMode"
          value={blendMode}
          onChange={(e) => setBlendMode(e.target.value)}
        >
          <option value="normal">Normal</option>
          <option value="multiply">Multiply</option>
          <option value="overlay">Overlay</option>
          <option value="soft-light">Soft Light</option>
        </select>
      </div>

      <div className="control-item">
        <label htmlFor="opacity">
          Opacity: <span className="value">{opacity}%</span>
        </label>
        <input
          type="range"
          id="opacity"
          min="0"
          max="100"
          value={opacity}
          onChange={(e) => setOpacity(parseInt(e.target.value))}
        />
      </div>

      <div className="control-item">
        <label htmlFor="brightness">
          Brightness: <span className="value">{brightness}</span>
        </label>
        <input
          type="range"
          id="brightness"
          min="-50"
          max="50"
          value={brightness}
          onChange={(e) => setBrightness(parseInt(e.target.value))}
        />
      </div>

      <div className="control-item checkbox-item">
        <label htmlFor="perspective">
          <input
            type="checkbox"
            id="perspective"
            checked={perspectiveCorrection}
            onChange={(e) => setPerspectiveCorrection(e.target.checked)}
          />
          Perspective Correction
        </label>
      </div>
    </div>
  );
}

export default Controls;
