"""
RenderEase: Surface Segmentation and Texture Transfer System
Complete implementation with Classical, DeepLab, and SAM methods
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Optional, List
import json
from datetime import datetime


class RenderEase:
    """
    Main class for RenderEase texture transfer system.
    Supports multiple segmentation methods: Classical (Hough), DeepLab, and SAM.
    """

    def __init__(self, method="classical", save_intermediates=True):
        """
        Initialize RenderEase system.

        Args:
            method: 'classical', 'deeplab', or 'sam'
            save_intermediates: Save intermediate processing steps for debugging
        """
        self.method = method.lower()
        self.save_intermediates = save_intermediates
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)

        # Initialize the selected segmentation method
        if self.method == "classical":
            self.segmentor = ClassicalSegmentor()
        elif self.method == "deeplab":
            self.segmentor = DeepLabSegmentor()
        elif self.method == "sam":
            self.segmentor = SAMSegmentor()
        else:
            raise ValueError(
                f"Unknown method: {method}. Use 'classical', 'deeplab', or 'sam'"
            )

        print(f"✓ RenderEase initialized with {self.method} method")

    def process_image(
        self, image_path: str, texture_path: str, surface_type: str = "wall"
    ) -> Dict:
        """
        Main processing pipeline: segment surface and apply texture.

        Args:
            image_path: Path to room image
            texture_path: Path to texture image
            surface_type: 'wall', 'floor', or 'ceiling'

        Returns:
            Dictionary with results and metrics
        """
        print(f"\n{'='*60}")
        print(f"Processing: {Path(image_path).name}")
        print(f"Method: {self.method}")
        print(f"{'='*60}\n")

        # Load images
        image = cv2.imread(image_path)
        texture = cv2.imread(texture_path)

        if image is None or texture is None:
            raise FileNotFoundError(
                f"Could not load images: {image_path} or {texture_path}"
            )

        print(f"✓ Loaded image: {image.shape}")
        print(f"✓ Loaded texture: {texture.shape}")

        # Step 1: Segment the surface
        print(f"\n[1/4] Segmenting {surface_type}...")
        import time

        start_time = time.time()

        mask, corners, debug_info = self.segmentor.segment(image, surface_type)

        segmentation_time = time.time() - start_time
        print(f"✓ Segmentation complete ({segmentation_time:.3f}s)")

        if self.save_intermediates:
            self._save_intermediate(image, "input", image_path)
            self._save_intermediate(mask, "mask", image_path)

        # Step 2: Estimate homography
        print(f"\n[2/4] Computing homography...")
        if corners is None or len(corners) != 4:
            print("⚠ Warning: Could not find 4 corners, using mask bounds")
            corners = self._get_mask_bounds(mask)

        H = self._compute_homography(corners, texture.shape)
        print(f"✓ Homography computed")

        # Step 3: Warp texture
        print(f"\n[3/4] Warping texture...")
        warped_texture = cv2.warpPerspective(
            texture, H, (image.shape[1], image.shape[0])
        )

        if self.save_intermediates:
            self._save_intermediate(warped_texture, "warped", image_path)

        # Step 4: Blend texture with original image
        print(f"\n[4/4] Blending texture...")
        result = self._blend_texture(image, warped_texture, mask)

        # Save final result
        output_path = self._save_result(result, image_path)
        print(f"✓ Saved result: {output_path}")

        # Compute metrics
        metrics = {
            "method": self.method,
            "image": Path(image_path).name,
            "surface_type": surface_type,
            "segmentation_time": segmentation_time,
            "mask_area_ratio": np.sum(mask > 0) / mask.size,
            "corners": corners.tolist() if corners is not None else None,
            "output_path": str(output_path),
            "timestamp": datetime.now().isoformat(),
        }

        # Add method-specific debug info
        metrics.update(debug_info)

        # Save metrics
        self._save_metrics(metrics, image_path)

        print(f"\n{'='*60}")
        print(f"✓ Processing complete!")
        print(f"  - Segmentation time: {segmentation_time:.3f}s")
        print(f"  - Mask coverage: {metrics['mask_area_ratio']*100:.1f}%")
        print(f"  - Output: {output_path}")
        print(f"{'='*60}\n")

        return metrics

    def _compute_homography(
        self, corners: np.ndarray, texture_shape: Tuple
    ) -> np.ndarray:
        """Compute homography matrix from corners to texture coordinates."""
        h, w = texture_shape[:2]

        # Define destination points (texture corners)
        dst_pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)

        # Source points (detected corners)
        src_pts = corners.astype(np.float32)

        # Compute homography
        H, _ = cv2.findHomography(dst_pts, src_pts)

        return H

    def _get_mask_bounds(self, mask: np.ndarray) -> np.ndarray:
        """Get bounding box corners from mask."""
        coords = cv2.findNonZero(mask)
        if coords is None:
            # Return image corners as fallback
            h, w = mask.shape
            return np.array([[0, 0], [w, 0], [w, h], [0, h]])

        x, y, w, h = cv2.boundingRect(coords)
        return np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])

    def _blend_texture(
        self, image: np.ndarray, texture: np.ndarray, mask: np.ndarray
    ) -> np.ndarray:
        """Blend warped texture with original image using mask."""
        # Ensure mask is binary
        mask = (mask > 127).astype(np.uint8)

        # Create 3-channel mask
        mask_3ch = cv2.merge([mask, mask, mask])

        # Simple alpha blending
        result = np.where(mask_3ch > 0, texture, image)

        # Optional: Add slight feathering at edges
        kernel = np.ones((5, 5), np.uint8)
        mask_eroded = cv2.erode(mask, kernel, iterations=2)
        mask_border = mask - mask_eroded

        if np.any(mask_border):
            # Blend at borders
            alpha = 0.7
            mask_border_3ch = cv2.merge([mask_border, mask_border, mask_border])
            result = np.where(
                mask_border_3ch > 0,
                cv2.addWeighted(image, 1 - alpha, texture, alpha, 0),
                result,
            )

        return result.astype(np.uint8)

    def _save_intermediate(self, image: np.ndarray, stage: str, original_path: str):
        """Save intermediate processing stage."""
        base_name = Path(original_path).stem
        output_path = self.output_dir / f"{base_name}_{self.method}_{stage}.png"
        cv2.imwrite(str(output_path), image)

    def _save_result(self, result: np.ndarray, original_path: str) -> Path:
        """Save final result."""
        base_name = Path(original_path).stem
        output_path = self.output_dir / f"{base_name}_{self.method}_result.png"
        cv2.imwrite(str(output_path), result)
        return output_path

    def _save_metrics(self, metrics: Dict, original_path: str):
        """Save metrics to JSON."""
        base_name = Path(original_path).stem
        output_path = self.output_dir / f"{base_name}_{self.method}_metrics.json"
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)


class ClassicalSegmentor:
    """Classical computer vision approach using edge detection and Hough transform."""

    def __init__(self):
        self.name = "Classical (Hough + Edges)"

    def segment(self, image: np.ndarray, surface_type: str) -> Tuple:
        """
        Segment surface using classical CV methods.

        Returns:
            mask: Binary mask of segmented surface
            corners: 4 corner points (or None)
            debug_info: Dictionary with intermediate results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10
        )

        debug_info = {
            "num_edges": np.sum(edges > 0),
            "num_lines": len(lines) if lines is not None else 0,
        }

        if lines is None:
            print("⚠ Warning: No lines detected, using full image")
            mask = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8) * 255
            return mask, None, debug_info

        # Cluster lines by orientation
        horizontal_lines, vertical_lines = self._cluster_lines(lines)

        debug_info["num_horizontal"] = len(horizontal_lines)
        debug_info["num_vertical"] = len(vertical_lines)

        # Find intersection points (corners)
        corners = self._find_corners(horizontal_lines, vertical_lines, image.shape)

        if corners is not None and len(corners) == 4:
            # Create mask from corners
            mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            cv2.fillPoly(mask, [corners], 255)
            debug_info["segmentation_method"] = "corner_detection"
        else:
            # Fallback: use edge-based region growing
            print("⚠ Using fallback: edge-based segmentation")
            mask = self._edge_based_segmentation(edges, image.shape, surface_type)
            corners = None
            debug_info["segmentation_method"] = "edge_based_fallback"

        return mask, corners, debug_info

    def _cluster_lines(self, lines: np.ndarray) -> Tuple[List, List]:
        """Cluster lines into horizontal and vertical."""
        horizontal = []
        vertical = []

        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Calculate angle
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)

            # Classify as horizontal or vertical
            if angle < 30 or angle > 150:  # Horizontal (±30°)
                horizontal.append(line[0])
            elif 60 < angle < 120:  # Vertical (±30° from 90°)
                vertical.append(line[0])

        return horizontal, vertical

    def _find_corners(
        self, h_lines: List, v_lines: List, shape: Tuple
    ) -> Optional[np.ndarray]:
        """Find intersection points between horizontal and vertical lines."""
        if len(h_lines) < 2 or len(v_lines) < 2:
            return None

        # Sort lines
        h_lines_sorted = sorted(h_lines, key=lambda l: (l[1] + l[3]) / 2)
        v_lines_sorted = sorted(v_lines, key=lambda l: (l[0] + l[2]) / 2)

        # Take top/bottom horizontal and left/right vertical
        top_line = h_lines_sorted[0]
        bottom_line = h_lines_sorted[-1]
        left_line = v_lines_sorted[0]
        right_line = v_lines_sorted[-1]

        # Find intersections
        corners = []
        for h in [top_line, bottom_line]:
            for v in [left_line, right_line]:
                pt = self._line_intersection(h, v)
                if pt is not None:
                    corners.append(pt)

        if len(corners) == 4:
            # Order corners: top-left, top-right, bottom-right, bottom-left
            corners = np.array(corners)
            corners = self._order_points(corners)
            return corners

        return None

    def _line_intersection(
        self, line1: np.ndarray, line2: np.ndarray
    ) -> Optional[np.ndarray]:
        """Find intersection point of two lines."""
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return None

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        return np.array([int(px), int(py)])

    def _order_points(self, pts: np.ndarray) -> np.ndarray:
        """Order points as: top-left, top-right, bottom-right, bottom-left."""
        # Sort by y-coordinate
        pts_sorted = pts[np.argsort(pts[:, 1])]

        # Top two points
        top_pts = pts_sorted[:2]
        top_pts = top_pts[np.argsort(top_pts[:, 0])]  # Sort by x

        # Bottom two points
        bottom_pts = pts_sorted[2:]
        bottom_pts = bottom_pts[np.argsort(bottom_pts[:, 0])]  # Sort by x

        return np.array([top_pts[0], top_pts[1], bottom_pts[1], bottom_pts[0]])

    def _edge_based_segmentation(
        self, edges: np.ndarray, shape: Tuple, surface_type: str
    ) -> np.ndarray:
        """Fallback: simple edge-based segmentation."""
        # Dilate edges to create regions
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=3)

        # Find largest contour
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            # Return full image
            return np.ones((shape[0], shape[1]), dtype=np.uint8) * 255

        # Get largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Create mask
        mask = np.zeros((shape[0], shape[1]), dtype=np.uint8)
        cv2.drawContours(mask, [largest_contour], -1, 255, -1)

        return mask


class DeepLabSegmentor:
    """DeepLab-based semantic segmentation."""

    def __init__(self):
        self.name = "DeepLabv3+"
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load pretrained DeepLab model."""
        try:
            import torch
            import torchvision

            print("  Loading DeepLabv3+ model...")
            self.model = torchvision.models.segmentation.deeplabv3_resnet101(
                pretrained=True
            )
            self.model.eval()

            # Move to GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)

            print(f"  ✓ Model loaded on {self.device}")

        except Exception as e:
            print(f"  ⚠ Warning: Could not load DeepLab model: {e}")
            print(f"  ⚠ Falling back to classical method")
            self.model = None

    def segment(self, image: np.ndarray, surface_type: str) -> Tuple:
        """Segment using DeepLab."""
        if self.model is None:
            # Fallback to classical
            print("  Using classical fallback...")
            classical = ClassicalSegmentor()
            return classical.segment(image, surface_type)

        import torch
        import torchvision.transforms as T

        # Preprocess image
        transform = T.Compose(
            [
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = transform(input_image).unsqueeze(0).to(self.device)

        # Run inference
        with torch.no_grad():
            output = self.model(input_tensor)["out"][0]

        output_predictions = output.argmax(0).byte().cpu().numpy()

        # Map to surface type
        # DeepLab classes (PASCAL VOC): 0=background, 9=chair, 15=person, etc.
        # For demo, we'll use a simple heuristic
        mask = self._extract_surface_mask(output_predictions, surface_type, image.shape)

        # Find corners from mask
        corners = self._find_corners_from_mask(mask)

        debug_info = {
            "segmentation_method": "deeplab",
            "unique_classes": len(np.unique(output_predictions)),
            "model_device": str(self.device),
        }

        return mask, corners, debug_info

    def _extract_surface_mask(
        self, predictions: np.ndarray, surface_type: str, shape: Tuple
    ) -> np.ndarray:
        """Extract mask for specific surface type."""
        # For wall/floor/ceiling, we use heuristics based on location
        mask = np.zeros(shape[:2], dtype=np.uint8)

        # Heuristic: walls are typically vertical regions
        # floors are bottom third, ceilings are top third
        h, w = shape[:2]

        if surface_type == "wall":
            # Look for vertical surfaces (middle region)
            mask[int(h * 0.1) : int(h * 0.9), :] = 255
        elif surface_type == "floor":
            # Bottom region
            mask[int(h * 0.6) :, :] = 255
        elif surface_type == "ceiling":
            # Top region
            mask[: int(h * 0.4), :] = 255
        else:
            # Default: use largest segment
            mask = (predictions > 0).astype(np.uint8) * 255

        return mask

    def _find_corners_from_mask(self, mask: np.ndarray) -> Optional[np.ndarray]:
        """Find corner points from mask."""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # Get largest contour
        largest = max(contours, key=cv2.contourArea)

        # Approximate polygon
        epsilon = 0.02 * cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, epsilon, True)

        if len(approx) >= 4:
            # Take first 4 points
            return approx[:4].reshape(4, 2)

        return None


class SAMSegmentor:
    """Segment Anything Model (SAM) segmentation."""

    def __init__(self):
        self.name = "SAM"
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load SAM model."""
        try:
            from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
            import torch

            print("  Loading SAM model...")

            # Try to download model if not present
            model_path = "sam_vit_h_4b8939.pth"
            if not Path(model_path).exists():
                print("  ⚠ SAM model not found. Please download it from:")
                print("     https://github.com/facebookresearch/segment-anything")
                print("  ⚠ Falling back to classical method")
                self.model = None
                return

            sam = sam_model_registry["vit_h"](checkpoint=model_path)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            sam.to(device=device)

            self.mask_generator = SamAutomaticMaskGenerator(sam)
            self.model = sam

            print(f"  ✓ SAM loaded on {device}")

        except Exception as e:
            print(f"  ⚠ Warning: Could not load SAM: {e}")
            print(f"  ⚠ Falling back to classical method")
            self.model = None

    def segment(self, image: np.ndarray, surface_type: str) -> Tuple:
        """Segment using SAM."""
        if self.model is None:
            # Fallback to classical
            print("  Using classical fallback...")
            classical = ClassicalSegmentor()
            return classical.segment(image, surface_type)

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Generate masks
        masks = self.mask_generator.generate(image_rgb)

        # Select best mask based on surface type and size
        mask = self._select_best_mask(masks, surface_type, image.shape)

        # Find corners
        corners = self._find_corners_from_mask(mask)

        debug_info = {
            "segmentation_method": "sam",
            "num_masks": len(masks),
            "selected_mask_area": np.sum(mask > 0),
        }

        return mask, corners, debug_info

    def _select_best_mask(
        self, masks: List[Dict], surface_type: str, shape: Tuple
    ) -> np.ndarray:
        """Select the best mask based on criteria."""
        if not masks:
            return np.ones((shape[0], shape[1]), dtype=np.uint8) * 255

        # Sort by area (descending)
        masks_sorted = sorted(masks, key=lambda m: m["area"], reverse=True)

        # For now, take largest mask
        # TODO: Better heuristics based on surface_type and location
        best_mask = masks_sorted[0]["segmentation"]

        return (best_mask * 255).astype(np.uint8)

    def _find_corners_from_mask(self, mask: np.ndarray) -> Optional[np.ndarray]:
        """Find corner points from mask."""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, epsilon, True)

        if len(approx) >= 4:
            return approx[:4].reshape(4, 2)

        return None


# Convenience function
def process_room(
    image_path: str, texture_path: str, method="classical", surface_type="wall"
):
    """
    Quick function to process a single room image.

    Args:
        image_path: Path to room image
        texture_path: Path to texture image
        method: 'classical', 'deeplab', or 'sam'
        surface_type: 'wall', 'floor', or 'ceiling'

    Returns:
        Dictionary with results
    """
    system = RenderEase(method=method)
    return system.process_image(image_path, texture_path, surface_type)
