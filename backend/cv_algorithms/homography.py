"""
Homography and Perspective Transformation Module
Implements perspective transformation and warping
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional


class HomographyTransform:
    """
    Homography matrix computation and perspective transformation
    """

    def __init__(self):
        self.homography_matrix = None
        self.last_warped = None

    def compute_homography(
        self,
        src_points: np.ndarray,
        dst_points: np.ndarray,
        method: str = 'RANSAC'
    ) -> Optional[np.ndarray]:
        """
        Compute homography matrix from point correspondences

        Args:
            src_points: Source points (Nx2 array)
            dst_points: Destination points (Nx2 array)
            method: Method for computing homography ('RANSAC', 'LMEDS', '0')

        Returns:
            3x3 homography matrix or None
        """
        if len(src_points) < 4 or len(dst_points) < 4:
            return None

        # Ensure points are float32
        src_pts = np.float32(src_points)
        dst_pts = np.float32(dst_points)

        # Select method
        if method == 'RANSAC':
            method_flag = cv2.RANSAC
        elif method == 'LMEDS':
            method_flag = cv2.LMEDS
        else:
            method_flag = 0

        # Compute homography
        H, mask = cv2.findHomography(src_pts, dst_pts, method_flag, 5.0)

        self.homography_matrix = H
        return H

    def warp_perspective(
        self,
        image: np.ndarray,
        homography: np.ndarray,
        output_size: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """
        Apply perspective transformation to image

        Args:
            image: Input image
            homography: 3x3 homography matrix
            output_size: Output image size (width, height), defaults to input size

        Returns:
            Warped image
        """
        if output_size is None:
            output_size = (image.shape[1], image.shape[0])

        warped = cv2.warpPerspective(
            image,
            homography,
            output_size,
            flags=cv2.INTER_LINEAR
        )

        self.last_warped = warped
        return warped

    def compute_homography_from_corners(
        self,
        src_corners: List[Tuple[int, int]],
        dst_corners: List[Tuple[int, int]]
    ) -> np.ndarray:
        """
        Compute homography from four corner points

        Args:
            src_corners: Source corner points [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
            dst_corners: Destination corner points

        Returns:
            3x3 homography matrix
        """
        src_pts = np.float32(src_corners)
        dst_pts = np.float32(dst_corners)

        H = cv2.getPerspectiveTransform(src_pts, dst_pts)

        self.homography_matrix = H
        return H

    def apply_texture_with_perspective(
        self,
        base_image: np.ndarray,
        texture_image: np.ndarray,
        corners: List[Tuple[int, int]],
        blend_alpha: float = 0.8
    ) -> np.ndarray:
        """
        Apply texture to image region with perspective correction

        Args:
            base_image: Base image to apply texture to
            texture_image: Texture to apply
            corners: Four corner points of the target region
            blend_alpha: Blending factor (0-1)

        Returns:
            Image with texture applied
        """
        # Get texture dimensions
        tex_h, tex_w = texture_image.shape[:2]

        # Define source points (texture corners)
        src_pts = np.float32([
            [0, 0],
            [tex_w, 0],
            [tex_w, tex_h],
            [0, tex_h]
        ])

        # Define destination points (target region corners)
        dst_pts = np.float32(corners)

        # Compute homography
        H = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # Warp texture
        warped_texture = cv2.warpPerspective(
            texture_image,
            H,
            (base_image.shape[1], base_image.shape[0])
        )

        # Create mask for the warped region
        mask = np.zeros(base_image.shape[:2], dtype=np.uint8)
        cv2.fillConvexPoly(mask, np.int32(corners), 255)

        # Blend images
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        result = base_image.copy().astype(float)

        # Apply blending only in masked region
        result = (
            result * (1 - mask_3ch * blend_alpha) +
            warped_texture.astype(float) * mask_3ch * blend_alpha
        )

        return result.astype(np.uint8)

    def rectify_region(
        self,
        image: np.ndarray,
        corners: List[Tuple[int, int]],
        output_size: Tuple[int, int] = (512, 512)
    ) -> np.ndarray:
        """
        Rectify (flatten) a quadrilateral region to a rectangle

        Args:
            image: Input image
            corners: Four corner points of the region
            output_size: Desired output size (width, height)

        Returns:
            Rectified region
        """
        # Define source points
        src_pts = np.float32(corners)

        # Define destination points (rectangle)
        dst_pts = np.float32([
            [0, 0],
            [output_size[0], 0],
            [output_size[0], output_size[1]],
            [0, output_size[1]]
        ])

        # Compute homography
        H = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # Warp region
        rectified = cv2.warpPerspective(image, H, output_size)

        return rectified

    def inverse_warp(
        self,
        warped_image: np.ndarray,
        original_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Apply inverse perspective transformation

        Args:
            warped_image: Warped image
            original_size: Original image size (width, height)

        Returns:
            Image warped back to original perspective
        """
        if self.homography_matrix is None:
            return warped_image

        # Compute inverse homography
        H_inv = np.linalg.inv(self.homography_matrix)

        # Apply inverse warp
        unwarped = cv2.warpPerspective(
            warped_image,
            H_inv,
            original_size
        )

        return unwarped

    def auto_detect_plane_homography(
        self,
        image: np.ndarray,
        edges: np.ndarray
    ) -> Optional[np.ndarray]:
        """
        Automatically detect plane homography from edges (simplified)

        Args:
            image: Input image
            edges: Edge image

        Returns:
            Homography matrix or None
        """
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=100,
            minLineLength=100,
            maxLineGap=10
        )

        if lines is None or len(lines) < 4:
            return None

        # Find intersections to get corner points (simplified approach)
        # This is a placeholder - full implementation would be more complex
        corners = self._find_quadrilateral_corners(lines, image.shape)

        if corners is None:
            return None

        # Define target rectangle
        width = image.shape[1]
        height = image.shape[0]
        dst_corners = [
            [0, 0],
            [width, 0],
            [width, height],
            [0, height]
        ]

        # Compute homography
        H = self.compute_homography_from_corners(corners, dst_corners)

        return H

    def _find_quadrilateral_corners(
        self,
        lines: np.ndarray,
        image_shape: Tuple
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find quadrilateral corners from lines (simplified)

        Args:
            lines: Detected lines
            image_shape: Image shape

        Returns:
            Four corner points or None
        """
        # This is a simplified placeholder
        # A full implementation would involve:
        # 1. Grouping parallel lines
        # 2. Finding intersections
        # 3. Selecting the four corners of the dominant quadrilateral

        # For now, return None (would need more sophisticated logic)
        return None

    def apply_barrel_distortion_correction(
        self,
        image: np.ndarray,
        k1: float = 0.0,
        k2: float = 0.0
    ) -> np.ndarray:
        """
        Correct barrel/pincushion distortion

        Args:
            image: Input image
            k1: Radial distortion coefficient
            k2: Radial distortion coefficient

        Returns:
            Corrected image
        """
        h, w = image.shape[:2]

        # Camera matrix (assuming image center is principal point)
        camera_matrix = np.array([
            [w, 0, w/2],
            [0, w, h/2],
            [0, 0, 1]
        ], dtype=np.float32)

        # Distortion coefficients
        dist_coeffs = np.array([k1, k2, 0, 0, 0], dtype=np.float32)

        # Undistort
        corrected = cv2.undistort(
            image,
            camera_matrix,
            dist_coeffs
        )

        return corrected
