"""
Hough Transform Module
Implements Hough Line Transform and Hough Circle Transform
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Line:
    """Represents a line detected by Hough Transform"""
    rho: float
    theta: float
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass
class Circle:
    """Represents a circle detected by Hough Transform"""
    x: int
    y: int
    radius: int


class HoughTransform:
    """
    Hough Transform for line and circle detection
    """

    def __init__(self):
        self.detected_lines = []
        self.detected_circles = []

    def detect_lines(
        self,
        edge_image: np.ndarray,
        rho: float = 1,
        theta: float = np.pi / 180,
        threshold: int = 100,
        min_line_length: int = 50,
        max_line_gap: int = 10,
        use_probabilistic: bool = True
    ) -> List[Line]:
        """
        Detect lines using Hough Transform

        Args:
            edge_image: Binary edge image
            rho: Distance resolution in pixels
            theta: Angle resolution in radians
            threshold: Minimum number of votes
            min_line_length: Minimum line length (probabilistic only)
            max_line_gap: Maximum gap between line segments (probabilistic only)
            use_probabilistic: Use probabilistic Hough transform

        Returns:
            List of detected lines
        """
        lines = []

        if use_probabilistic:
            # Probabilistic Hough Line Transform
            detected = cv2.HoughLinesP(
                edge_image,
                rho,
                theta,
                threshold,
                minLineLength=min_line_length,
                maxLineGap=max_line_gap
            )

            if detected is not None:
                for line in detected:
                    x1, y1, x2, y2 = line[0]

                    # Calculate rho and theta for the line
                    dx = x2 - x1
                    dy = y2 - y1
                    if dx == 0:
                        theta_calc = np.pi / 2
                    else:
                        theta_calc = np.arctan2(dy, dx)

                    rho_calc = x1 * np.cos(theta_calc) + y1 * np.sin(theta_calc)

                    lines.append(Line(
                        rho=rho_calc,
                        theta=theta_calc,
                        x1=int(x1),
                        y1=int(y1),
                        x2=int(x2),
                        y2=int(y2)
                    ))
        else:
            # Standard Hough Line Transform
            detected = cv2.HoughLines(edge_image, rho, theta, threshold)

            if detected is not None:
                height, width = edge_image.shape
                for line in detected:
                    rho_val, theta_val = line[0]

                    # Convert to Cartesian coordinates
                    a = np.cos(theta_val)
                    b = np.sin(theta_val)
                    x0 = a * rho_val
                    y0 = b * rho_val

                    # Extend line to image boundaries
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                    lines.append(Line(
                        rho=rho_val,
                        theta=theta_val,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2
                    ))

        self.detected_lines = lines
        return lines

    def detect_circles(
        self,
        image: np.ndarray,
        min_dist: int = 50,
        param1: int = 100,
        param2: int = 30,
        min_radius: int = 10,
        max_radius: int = 100
    ) -> List[Circle]:
        """
        Detect circles using Hough Circle Transform

        Args:
            image: Input image (grayscale)
            min_dist: Minimum distance between circle centers
            param1: Upper threshold for Canny edge detector
            param2: Accumulator threshold for circle detection
            min_radius: Minimum circle radius
            max_radius: Maximum circle radius

        Returns:
            List of detected circles
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply median blur to reduce noise
        gray = cv2.medianBlur(gray, 5)

        # Detect circles
        circles_detected = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=min_dist,
            param1=param1,
            param2=param2,
            minRadius=min_radius,
            maxRadius=max_radius
        )

        circles = []
        if circles_detected is not None:
            circles_detected = np.uint16(np.around(circles_detected))
            for circle in circles_detected[0, :]:
                circles.append(Circle(
                    x=int(circle[0]),
                    y=int(circle[1]),
                    radius=int(circle[2])
                ))

        self.detected_circles = circles
        return circles

    def filter_horizontal_lines(
        self,
        lines: List[Line],
        angle_threshold: float = 10
    ) -> List[Line]:
        """
        Filter lines to keep only horizontal ones

        Args:
            lines: List of lines
            angle_threshold: Angle threshold in degrees

        Returns:
            Filtered list of horizontal lines
        """
        horizontal_lines = []
        threshold_rad = np.deg2rad(angle_threshold)

        for line in lines:
            # Check if line is close to horizontal (0 or 180 degrees)
            if abs(line.theta) < threshold_rad or abs(line.theta - np.pi) < threshold_rad:
                horizontal_lines.append(line)

        return horizontal_lines

    def filter_vertical_lines(
        self,
        lines: List[Line],
        angle_threshold: float = 10
    ) -> List[Line]:
        """
        Filter lines to keep only vertical ones

        Args:
            lines: List of lines
            angle_threshold: Angle threshold in degrees

        Returns:
            Filtered list of vertical lines
        """
        vertical_lines = []
        threshold_rad = np.deg2rad(angle_threshold)

        for line in lines:
            # Check if line is close to vertical (90 degrees)
            if abs(line.theta - np.pi/2) < threshold_rad:
                vertical_lines.append(line)

        return vertical_lines

    def find_line_intersections(
        self,
        lines: List[Line]
    ) -> List[Tuple[int, int]]:
        """
        Find intersection points of detected lines

        Args:
            lines: List of lines

        Returns:
            List of intersection points
        """
        intersections = []

        for i, line1 in enumerate(lines):
            for line2 in lines[i+1:]:
                intersection = self._line_intersection(line1, line2)
                if intersection is not None:
                    intersections.append(intersection)

        return intersections

    def _line_intersection(
        self,
        line1: Line,
        line2: Line
    ) -> Optional[Tuple[int, int]]:
        """
        Calculate intersection point of two lines

        Args:
            line1: First line
            line2: Second line

        Returns:
            Intersection point or None
        """
        x1, y1, x2, y2 = line1.x1, line1.y1, line1.x2, line1.y2
        x3, y3, x4, y4 = line2.x1, line2.y1, line2.x2, line2.y2

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if abs(denom) < 1e-10:
            return None  # Lines are parallel

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom

        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))

        return (x, y)

    def draw_lines(
        self,
        image: np.ndarray,
        lines: List[Line],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw detected lines on image

        Args:
            image: Input image
            lines: List of lines to draw
            color: Line color (BGR)
            thickness: Line thickness

        Returns:
            Image with lines drawn
        """
        output = image.copy()

        for line in lines:
            cv2.line(
                output,
                (line.x1, line.y1),
                (line.x2, line.y2),
                color,
                thickness
            )

        return output

    def draw_circles(
        self,
        image: np.ndarray,
        circles: List[Circle],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw detected circles on image

        Args:
            image: Input image
            circles: List of circles to draw
            color: Circle color (BGR)
            thickness: Circle thickness

        Returns:
            Image with circles drawn
        """
        output = image.copy()

        for circle in circles:
            cv2.circle(output, (circle.x, circle.y), circle.radius, color, thickness)
            cv2.circle(output, (circle.x, circle.y), 2, (0, 0, 255), 3)

        return output
