"""
Edge Detection Module
Implements Canny edge detection and related algorithms
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class EdgeDetector:
    """
    Edge detection using various algorithms including Canny
    """

    def __init__(self):
        self.last_edges = None

    def canny_edge_detection(
        self,
        image: np.ndarray,
        low_threshold: int = 50,
        high_threshold: int = 150,
        aperture_size: int = 3,
        l2_gradient: bool = False
    ) -> np.ndarray:
        """
        Perform Canny edge detection on an image

        Args:
            image: Input image (BGR or grayscale)
            low_threshold: Lower threshold for edge detection
            high_threshold: Upper threshold for edge detection
            aperture_size: Aperture size for Sobel operator
            l2_gradient: Use L2 norm for gradient magnitude

        Returns:
            Binary edge map
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)

        # Apply Canny edge detection
        edges = cv2.Canny(
            blurred,
            low_threshold,
            high_threshold,
            apertureSize=aperture_size,
            L2gradient=l2_gradient
        )

        self.last_edges = edges
        return edges

    def sobel_edge_detection(
        self,
        image: np.ndarray,
        ksize: int = 3
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform Sobel edge detection

        Args:
            image: Input image
            ksize: Kernel size for Sobel operator

        Returns:
            Tuple of (magnitude, gradient_x, gradient_y)
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Calculate gradients
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

        # Calculate magnitude
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        magnitude = np.uint8(magnitude / magnitude.max() * 255)

        return magnitude, grad_x, grad_y

    def laplacian_edge_detection(
        self,
        image: np.ndarray,
        ksize: int = 3
    ) -> np.ndarray:
        """
        Perform Laplacian edge detection

        Args:
            image: Input image
            ksize: Kernel size

        Returns:
            Edge map
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Apply Laplacian
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F, ksize=ksize)
        laplacian = np.uint8(np.absolute(laplacian))

        return laplacian

    def adaptive_threshold_edges(
        self,
        image: np.ndarray,
        max_value: int = 255,
        block_size: int = 11,
        c: int = 2
    ) -> np.ndarray:
        """
        Adaptive thresholding for edge-like features

        Args:
            image: Input image
            max_value: Maximum value for thresholding
            block_size: Size of neighborhood area
            c: Constant subtracted from mean

        Returns:
            Binary edge map
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply adaptive thresholding
        edges = cv2.adaptiveThreshold(
            gray,
            max_value,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
            c
        )

        return edges

    def morphological_edge_detection(
        self,
        image: np.ndarray,
        kernel_size: int = 5
    ) -> np.ndarray:
        """
        Edge detection using morphological operations

        Args:
            image: Input image
            kernel_size: Size of morphological kernel

        Returns:
            Edge map
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Create kernel
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (kernel_size, kernel_size)
        )

        # Apply morphological gradient
        gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

        return gradient
