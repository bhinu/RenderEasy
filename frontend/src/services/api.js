/**
 * API Service for RenderEase Backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Edge detection
  detectEdges: async (imageData, method = 'canny', params = {}) => {
    const response = await api.post('/edge-detection', {
      image: imageData,
      method,
      params,
    });
    return response.data;
  },

  // Line detection (Hough Transform)
  detectLines: async (imageData, edgeData = null, params = {}) => {
    const response = await api.post('/detect-lines', {
      image: imageData,
      edges: edgeData,
      params,
    });
    return response.data;
  },

  // Image segmentation
  segmentImage: async (imageData, method = 'color', params = {}) => {
    const response = await api.post('/segment', {
      image: imageData,
      method,
      params,
    });
    return response.data;
  },

  // Generate texture
  generateTexture: async (type, width, height, params = {}) => {
    const response = await api.post('/generate-texture', {
      type,
      width,
      height,
      params,
    });
    return response.data;
  },

  // Apply texture to image
  applyTexture: async (imageData, textureData, corners, blendAlpha = 0.8, brightness = 0) => {
    const response = await api.post('/apply-texture', {
      image: imageData,
      texture: textureData,
      corners,
      blend_alpha: blendAlpha,
      brightness,
    });
    return response.data;
  },

  // Detect surfaces automatically
  detectSurfaces: async (imageData) => {
    const response = await api.post('/detect-surfaces', {
      image: imageData,
    });
    return response.data;
  },

  // Complete processing pipeline
  processComplete: async (imageData, textureType, options = {}) => {
    const response = await api.post('/process-complete', {
      image: imageData,
      texture_type: textureType,
      ...options,
    });
    return response.data;
  },
};

// Helper function to convert File to base64
export const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

export default apiService;
