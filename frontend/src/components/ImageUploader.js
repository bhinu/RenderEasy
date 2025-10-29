import React, { useCallback } from 'react';
import './ImageUploader.css';

function ImageUploader({ onImageUpload }) {
  const handleFileChange = useCallback(
    (event) => {
      const file = event.target.files[0];
      if (file && file.type.startsWith('image/')) {
        onImageUpload(file);
      }
    },
    [onImageUpload]
  );

  const handleDrop = useCallback(
    (event) => {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        onImageUpload(file);
      }
    },
    [onImageUpload]
  );

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div className="image-uploader">
      <div
        className="upload-area"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <input
          type="file"
          id="imageUpload"
          accept="image/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <button
          className="btn btn-primary"
          onClick={() => document.getElementById('imageUpload').click()}
        >
          Choose Image
        </button>
        <p className="upload-text">or drag and drop an image here</p>
      </div>
    </div>
  );
}

export default ImageUploader;
