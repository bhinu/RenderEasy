import React from 'react';
import './TextureLibrary.css';

const TEXTURES = [
  { id: 1, type: 'wood', name: 'Wood Floor', color: [139, 69, 19] },
  { id: 2, type: 'wood', name: 'Light Wood', color: [222, 184, 135] },
  { id: 3, type: 'wood', name: 'Dark Wood', color: [101, 67, 33] },
  { id: 4, type: 'marble', name: 'Marble', color: [245, 245, 220] },
  { id: 5, type: 'carpet', name: 'Gray Carpet', color: [128, 128, 128] },
  { id: 6, type: 'carpet', name: 'Beige Carpet', color: [210, 180, 140] },
  { id: 7, type: 'carpet', name: 'Green Carpet', color: [34, 139, 34] },
  { id: 8, type: 'tile', name: 'White Tile', color: [255, 255, 255] },
  { id: 9, type: 'tile', name: 'Black Tile', color: [51, 51, 51] },
  { id: 10, type: 'tile', name: 'Blue Tile', color: [65, 105, 225] },
  { id: 11, type: 'brick', name: 'Red Brick', color: [178, 34, 34] },
  { id: 12, type: 'concrete', name: 'Concrete', color: [169, 169, 169] },
];

function TextureLibrary({ onTextureSelect, selectedTexture }) {
  return (
    <div className="texture-library">
      <div className="texture-grid">
        {TEXTURES.map((texture) => (
          <div
            key={texture.id}
            className={`texture-item ${
              selectedTexture?.id === texture.id ? 'selected' : ''
            }`}
            style={{
              backgroundColor: `rgb(${texture.color.join(',')})`,
            }}
            onClick={() => onTextureSelect(texture)}
            title={texture.name}
          >
            <span className="texture-name">{texture.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TextureLibrary;
