"""
Image Segmentation Module
Implements various segmentation algorithms including color-based and region-based
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class SegmentMask:
    """Represents a segmentation mask"""
    mask: np.ndarray
    area: int
    center: Tuple[int, int]
    bounding_box: Tuple[int, int, int, int]  # x, y, width, height


class Segmentation:
    """
    Image segmentation using various algorithms
    """

    def __init__(self):
        self.last_mask = None
        self.segments = []

    def color_based_segmentation(
        self,
        image: np.ndarray,
        lower_bound: Tuple[int, int, int],
        upper_bound: Tuple[int, int, int],
        color_space: str = 'HSV'
    ) -> np.ndarray:
        """
        Segment image based on color range

        Args:
            image: Input image (BGR)
            lower_bound: Lower color bound
            upper_bound: Upper color bound
            color_space: Color space ('HSV', 'LAB', 'RGB')

        Returns:
            Binary mask
        """
        # Convert color space
        if color_space == 'HSV':
            converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif color_space == 'LAB':
            converted = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        elif color_space == 'RGB':
            converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            converted = image.copy()

        # Create mask
        mask = cv2.inRange(converted, lower_bound, upper_bound)

        # Apply morphological operations to clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        self.last_mask = mask
        return mask

    def grabcut_segmentation(
        self,
        image: np.ndarray,
        rect: Tuple[int, int, int, int],
        iterations: int = 5
    ) -> np.ndarray:
        """
        Segment using GrabCut algorithm

        Args:
            image: Input image (BGR)
            rect: Rectangle containing foreground (x, y, width, height)
            iterations: Number of iterations

        Returns:
            Binary mask
        """
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

        # Create binary mask
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        self.last_mask = mask2
        return mask2

    def watershed_segmentation(
        self,
        image: np.ndarray,
        markers: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Segment using watershed algorithm

        Args:
            image: Input image (BGR)
            markers: Optional marker image

        Returns:
            Segmentation mask
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if markers is None:
            # Generate markers automatically
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

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

            # Finding unknown region
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
        mask[markers > 1] = 255

        self.last_mask = mask
        return mask

    def kmeans_segmentation(
        self,
        image: np.ndarray,
        k: int = 3,
        attempts: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Segment using K-means clustering

        Args:
            image: Input image (BGR)
            k: Number of clusters
            attempts: Number of attempts

        Returns:
            Tuple of (segmented image, labels)
        """
        # Reshape image
        pixel_values = image.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        # Define criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

        # Apply K-means
        _, labels, centers = cv2.kmeans(
            pixel_values,
            k,
            None,
            criteria,
            attempts,
            cv2.KMEANS_PP_CENTERS
        )

        # Convert back to 8-bit values
        centers = np.uint8(centers)

        # Flatten labels
        labels = labels.flatten()

        # Convert to image
        segmented = centers[labels].reshape(image.shape)

        return segmented, labels.reshape(image.shape[:2])

    def mean_shift_segmentation(
        self,
        image: np.ndarray,
        spatial_radius: int = 20,
        color_radius: int = 40
    ) -> np.ndarray:
        """
        Segment using Mean Shift algorithm

        Args:
            image: Input image (BGR)
            spatial_radius: Spatial window radius
            color_radius: Color window radius

        Returns:
            Segmented image
        """
        segmented = cv2.pyrMeanShiftFiltering(
            image,
            spatial_radius,
            color_radius
        )

        return segmented

    def find_largest_segment(
        self,
        mask: np.ndarray
    ) -> SegmentMask:
        """
        Find the largest connected component in a binary mask

        Args:
            mask: Binary mask

        Returns:
            SegmentMask object for the largest segment
        """
        # Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            mask,
            connectivity=8
        )

        # Find largest component (excluding background)
        if num_labels <= 1:
            return None

        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

        # Create mask for largest component
        segment_mask = (labels == largest_label).astype(np.uint8) * 255

        # Get properties
        x, y, w, h = stats[largest_label, cv2.CC_STAT_LEFT:cv2.CC_STAT_LEFT + 4]
        area = stats[largest_label, cv2.CC_STAT_AREA]
        center = tuple(map(int, centroids[largest_label]))

        return SegmentMask(
            mask=segment_mask,
            area=area,
            center=center,
            bounding_box=(x, y, w, h)
        )

    def flood_fill_segment(
        self,
        image: np.ndarray,
        seed_point: Tuple[int, int],
        tolerance: int = 10
    ) -> np.ndarray:
        """
        Segment region using flood fill

        Args:
            image: Input image
            seed_point: Starting point (x, y)
            tolerance: Color tolerance

        Returns:
            Binary mask
        """
        # Create mask
        h, w = image.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Flood fill
        _, _, mask, _ = cv2.floodFill(
            image.copy(),
            mask,
            seed_point,
            (255, 255, 255),
            (tolerance,) * 3,
            (tolerance,) * 3,
            cv2.FLOODFILL_MASK_ONLY
        )

        # Remove padding
        mask = mask[1:-1, 1:-1]

        self.last_mask = mask
        return mask

    def adaptive_segmentation(
        self,
        image: np.ndarray,
        block_size: int = 11,
        c: int = 2
    ) -> np.ndarray:
        """
        Adaptive threshold-based segmentation

        Args:
            image: Input image
            block_size: Size of neighborhood
            c: Constant subtracted from mean

        Returns:
            Binary mask
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply adaptive threshold
        mask = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
            c
        )

        self.last_mask = mask
        return mask

    def contour_based_segmentation(
        self,
        image: np.ndarray,
        min_area: int = 100
    ) -> List[np.ndarray]:
        """
        Segment objects using contour detection

        Args:
            image: Input image (should be binary or edge image)
            min_area: Minimum contour area to keep

        Returns:
            List of contour masks
        """
        # Find contours
        contours, _ = cv2.findContours(
            image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter and create masks
        masks = []
        h, w = image.shape[:2]

        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                mask = np.zeros((h, w), dtype=np.uint8)
                cv2.drawContours(mask, [contour], -1, 255, -1)
                masks.append(mask)

        return masks
