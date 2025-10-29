"""
Advanced Image Segmentation Module
Implements state-of-the-art segmentation for precise object isolation
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass


@dataclass
class SegmentationResult:
    """Container for segmentation results"""
    mask: np.ndarray
    refined_mask: np.ndarray
    confidence: float
    contours: List[np.ndarray]
    bounding_box: Tuple[int, int, int, int]


class AdvancedSegmentation:
    """
    Advanced segmentation techniques for precise object isolation
    """

    def __init__(self):
        self.last_trimap = None
        self.last_mask = None

    def interactive_grabcut(
        self,
        image: np.ndarray,
        rect: Tuple[int, int, int, int],
        iterations: int = 5,
        refine: bool = True
    ) -> SegmentationResult:
        """
        Interactive GrabCut segmentation with automatic refinement

        Args:
            image: Input image (BGR)
            rect: Initial rectangle (x, y, width, height)
            iterations: Number of GrabCut iterations
            refine: Apply morphological refinement

        Returns:
            SegmentationResult with mask and refined mask
        """
        # Initialize mask and models
        mask = np.zeros(image.shape[:2], np.uint8)
        bg_model = np.zeros((1, 65), np.float64)
        fg_model = np.zeros((1, 65), np.float64)

        # Apply GrabCut
        cv2.grabCut(
            image,
            mask,
            rect,
            bg_model,
            fg_model,
            iterations,
            cv2.GC_INIT_WITH_RECT
        )

        # Create binary mask (foreground and probable foreground)
        binary_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Refine mask if requested
        if refine:
            refined_mask = self._refine_mask(binary_mask)
        else:
            refined_mask = binary_mask.copy()

        # Get contours
        contours, _ = cv2.findContours(
            refined_mask * 255,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Get bounding box of largest contour
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            bbox = (x, y, w, h)
            confidence = cv2.contourArea(largest_contour) / (image.shape[0] * image.shape[1])
        else:
            bbox = rect
            confidence = 0.0

        return SegmentationResult(
            mask=binary_mask,
            refined_mask=refined_mask,
            confidence=confidence,
            contours=contours,
            bounding_box=bbox
        )

    def superpixel_segmentation(
        self,
        image: np.ndarray,
        n_segments: int = 100,
        compactness: float = 10.0
    ) -> Tuple[np.ndarray, int]:
        """
        SLIC superpixel segmentation for region grouping

        Args:
            image: Input image (BGR)
            n_segments: Number of superpixels
            compactness: Balance between color and space

        Returns:
            Tuple of (segment labels, number of segments)
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Apply SLIC
        seeds = cv2.ximgproc.createSuperpixelSLIC(
            lab,
            region_size=int(np.sqrt(image.shape[0] * image.shape[1] / n_segments))
        )
        seeds.iterate(10)

        # Get labels
        labels = seeds.getLabels()
        num_segments = seeds.getNumberOfSuperpixels()

        return labels, num_segments

    def watershed_with_markers(
        self,
        image: np.ndarray,
        foreground_rect: Tuple[int, int, int, int]
    ) -> np.ndarray:
        """
        Watershed segmentation with automatic marker generation

        Args:
            image: Input image (BGR)
            foreground_rect: Rectangle indicating foreground region

        Returns:
            Binary segmentation mask
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply threshold
        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        # Noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # Sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)

        # Unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Marker labelling
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        # Apply watershed
        markers = cv2.watershed(image, markers)

        # Create binary mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        mask[markers > 1] = 1

        return mask

    def region_growing(
        self,
        image: np.ndarray,
        seed_point: Tuple[int, int],
        threshold: int = 10
    ) -> np.ndarray:
        """
        Region growing segmentation from seed point

        Args:
            image: Input image
            seed_point: Starting point (x, y)
            threshold: Similarity threshold

        Returns:
            Binary mask
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        h, w = gray.shape
        mask = np.zeros((h, w), np.uint8)
        visited = np.zeros((h, w), dtype=bool)

        # Get seed value
        seed_x, seed_y = seed_point
        seed_value = gray[seed_y, seed_x]

        # Queue for BFS
        queue = [(seed_x, seed_y)]
        visited[seed_y, seed_x] = True

        while queue:
            x, y = queue.pop(0)

            # Check if pixel is similar to seed
            if abs(int(gray[y, x]) - int(seed_value)) <= threshold:
                mask[y, x] = 1

                # Add neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                        visited[ny, nx] = True
                        queue.append((nx, ny))

        return mask

    def smart_flood_fill(
        self,
        image: np.ndarray,
        seed_point: Tuple[int, int],
        tolerance: int = 10
    ) -> np.ndarray:
        """
        Smart flood fill with edge-aware stopping

        Args:
            image: Input image
            seed_point: Starting point (x, y)
            tolerance: Color tolerance

        Returns:
            Binary mask
        """
        h, w = image.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Flags for flood fill
        flags = 4  # 4-connectivity
        flags |= cv2.FLOODFILL_MASK_ONLY
        flags |= (255 << 8)  # New value

        # Flood fill
        _, _, mask, _ = cv2.floodFill(
            image.copy(),
            mask,
            seed_point,
            (255, 255, 255),
            (tolerance,) * 3,
            (tolerance,) * 3,
            flags
        )

        # Remove padding
        mask = mask[1:-1, 1:-1]

        return (mask > 0).astype(np.uint8)

    def edge_aware_segmentation(
        self,
        image: np.ndarray,
        mask: np.ndarray,
        edge_strength: float = 0.5
    ) -> np.ndarray:
        """
        Refine segmentation using edge information

        Args:
            image: Input image
            mask: Initial mask
            edge_strength: Weight for edge information (0-1)

        Returns:
            Refined mask
        """
        # Detect edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Dilate edges slightly
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        # Use edges to refine mask
        # Remove mask pixels that cross strong edges
        refined_mask = mask.copy()
        refined_mask[edges > 0] = 0

        # Clean up with morphology
        refined_mask = self._refine_mask(refined_mask)

        return refined_mask

    def multi_scale_segmentation(
        self,
        image: np.ndarray,
        rect: Tuple[int, int, int, int],
        scales: List[float] = [0.5, 1.0, 1.5]
    ) -> np.ndarray:
        """
        Multi-scale segmentation for robust results

        Args:
            image: Input image
            rect: Initial rectangle
            scales: List of scale factors

        Returns:
            Combined mask from multiple scales
        """
        h, w = image.shape[:2]
        masks = []

        for scale in scales:
            # Resize image
            scaled_h, scaled_w = int(h * scale), int(w * scale)
            scaled_img = cv2.resize(image, (scaled_w, scaled_h))

            # Scale rectangle
            x, y, rw, rh = rect
            scaled_rect = (
                int(x * scale),
                int(y * scale),
                int(rw * scale),
                int(rh * scale)
            )

            # Segment at this scale
            result = self.interactive_grabcut(scaled_img, scaled_rect, iterations=3)

            # Resize mask back
            mask_resized = cv2.resize(
                result.refined_mask.astype(np.uint8),
                (w, h),
                interpolation=cv2.INTER_NEAREST
            )
            masks.append(mask_resized)

        # Combine masks (majority voting)
        combined = np.sum(masks, axis=0)
        final_mask = (combined >= len(scales) / 2).astype(np.uint8)

        return final_mask

    def _refine_mask(self, mask: np.ndarray) -> np.ndarray:
        """
        Apply morphological operations to refine mask

        Args:
            mask: Binary mask

        Returns:
            Refined mask
        """
        # Remove small noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        refined = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Fill holes
        refined = cv2.morphologyEx(refined, cv2.MORPH_CLOSE, kernel)

        # Smooth boundaries
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        refined = cv2.morphologyEx(refined, cv2.MORPH_CLOSE, kernel)

        return refined

    def get_smooth_contour(
        self,
        mask: np.ndarray,
        epsilon_factor: float = 0.01
    ) -> np.ndarray:
        """
        Get smooth contour from mask

        Args:
            mask: Binary mask
            epsilon_factor: Contour approximation factor

        Returns:
            Smoothed contour points
        """
        contours, _ = cv2.findContours(
            (mask * 255).astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        # Get largest contour
        largest = max(contours, key=cv2.contourArea)

        # Approximate contour
        epsilon = epsilon_factor * cv2.arcLength(largest, True)
        smoothed = cv2.approxPolyDP(largest, epsilon, True)

        return smoothed

    def create_feathered_mask(
        self,
        mask: np.ndarray,
        feather_amount: int = 10
    ) -> np.ndarray:
        """
        Create soft-edged mask for natural blending

        Args:
            mask: Binary mask
            feather_amount: Feathering radius in pixels

        Returns:
            Feathered mask (0-1 float)
        """
        # Convert to float
        mask_float = mask.astype(np.float32)

        # Apply Gaussian blur for feathering
        feathered = cv2.GaussianBlur(
            mask_float,
            (feather_amount * 2 + 1, feather_amount * 2 + 1),
            0
        )

        return feathered

    def segment_by_color_histogram(
        self,
        image: np.ndarray,
        sample_rect: Tuple[int, int, int, int],
        similarity_threshold: float = 0.7
    ) -> np.ndarray:
        """
        Segment similar colors based on histogram matching

        Args:
            image: Input image (BGR)
            sample_rect: Rectangle with sample region
            similarity_threshold: Histogram similarity threshold

        Returns:
            Binary mask
        """
        x, y, w, h = sample_rect
        sample = image[y:y+h, x:x+w]

        # Calculate histogram of sample
        hsv_sample = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
        hist_sample = cv2.calcHist(
            [hsv_sample],
            [0, 1],
            None,
            [180, 256],
            [0, 180, 0, 256]
        )
        cv2.normalize(hist_sample, hist_sample, 0, 255, cv2.NORM_MINMAX)

        # Calculate back projection
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        back_proj = cv2.calcBackProject(
            [hsv_image],
            [0, 1],
            hist_sample,
            [0, 180, 0, 256],
            1
        )

        # Threshold
        _, mask = cv2.threshold(
            back_proj,
            int(255 * similarity_threshold),
            255,
            cv2.THRESH_BINARY
        )

        # Refine
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return (mask > 0).astype(np.uint8)
