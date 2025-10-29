"""
Texture Generation Module
Generates procedural textures for interior design visualization
"""

import cv2
import numpy as np
from typing import Tuple


class TextureGenerator:
    """
    Generate procedural textures for various materials
    """

    def __init__(self):
        self.texture_cache = {}

    def generate_wood_texture(
        self,
        width: int,
        height: int,
        base_color: Tuple[int, int, int] = (139, 69, 19),
        grain_intensity: float = 0.3
    ) -> np.ndarray:
        """
        Generate wood texture with grain patterns

        Args:
            width: Texture width
            height: Texture height
            base_color: Base wood color (BGR)
            grain_intensity: Intensity of wood grain (0-1)

        Returns:
            Wood texture image
        """
        # Create base color image
        texture = np.ones((height, width, 3), dtype=np.uint8)
        texture[:, :] = base_color

        # Add wood grain using sine waves
        for y in range(height):
            for x in range(width):
                # Create wavy grain pattern
                noise = np.sin(y / 10.0 + np.random.randn() * 0.1) * 30
                noise += np.sin(x / 50.0) * 10

                # Apply grain
                grain = int(noise * grain_intensity)
                texture[y, x] = np.clip(texture[y, x] + grain, 0, 255)

        # Add random grain lines
        for _ in range(width // 20):
            y_pos = np.random.randint(0, height)
            thickness = np.random.randint(1, 3)
            variation = np.random.randint(-20, -10)

            for x in range(width):
                y_noise = int(y_pos + np.sin(x / 30.0) * 5)
                if 0 <= y_noise < height - thickness:
                    texture[y_noise:y_noise + thickness, x] = np.clip(
                        texture[y_noise:y_noise + thickness, x] + variation,
                        0,
                        255
                    )

        return texture

    def generate_marble_texture(
        self,
        width: int,
        height: int,
        base_color: Tuple[int, int, int] = (245, 245, 220),
        vein_color: Tuple[int, int, int] = (180, 180, 180)
    ) -> np.ndarray:
        """
        Generate marble texture with veins

        Args:
            width: Texture width
            height: Texture height
            base_color: Base marble color (BGR)
            vein_color: Vein color (BGR)

        Returns:
            Marble texture image
        """
        # Create base
        texture = np.ones((height, width, 3), dtype=np.uint8)
        texture[:, :] = base_color

        # Add Perlin-like noise for base variation
        noise = np.random.randn(height, width) * 10
        for c in range(3):
            texture[:, :, c] = np.clip(texture[:, :, c] + noise, 0, 255)

        # Add veins
        num_veins = np.random.randint(5, 15)
        for _ in range(num_veins):
            # Random vein path
            start_x = np.random.randint(0, width)
            start_y = np.random.randint(0, height)

            points = [(start_x, start_y)]
            for i in range(20):
                last_x, last_y = points[-1]
                next_x = last_x + np.random.randint(-30, 30)
                next_y = last_y + np.random.randint(-30, 30)
                next_x = np.clip(next_x, 0, width - 1)
                next_y = np.clip(next_y, 0, height - 1)
                points.append((next_x, next_y))

            # Draw vein
            for i in range(len(points) - 1):
                cv2.line(
                    texture,
                    points[i],
                    points[i + 1],
                    vein_color,
                    np.random.randint(1, 3),
                    cv2.LINE_AA
                )

        # Blur for smooth appearance
        texture = cv2.GaussianBlur(texture, (3, 3), 0)

        return texture

    def generate_carpet_texture(
        self,
        width: int,
        height: int,
        base_color: Tuple[int, int, int] = (128, 128, 128)
    ) -> np.ndarray:
        """
        Generate carpet texture

        Args:
            width: Texture width
            height: Texture height
            base_color: Carpet color (BGR)

        Returns:
            Carpet texture image
        """
        # Create base
        texture = np.ones((height, width, 3), dtype=np.uint8)
        texture[:, :] = base_color

        # Add fiber noise
        noise = np.random.randint(-15, 15, (height, width, 3))
        texture = np.clip(texture.astype(int) + noise, 0, 255).astype(np.uint8)

        # Add texture by applying blur
        texture = cv2.GaussianBlur(texture, (3, 3), 0)

        return texture

    def generate_tile_texture(
        self,
        width: int,
        height: int,
        tile_size: int = 100,
        base_color: Tuple[int, int, int] = (255, 255, 255),
        grout_color: Tuple[int, int, int] = (180, 180, 180),
        grout_width: int = 3
    ) -> np.ndarray:
        """
        Generate tile texture with grout

        Args:
            width: Texture width
            height: Texture height
            tile_size: Size of each tile
            base_color: Tile color (BGR)
            grout_color: Grout color (BGR)
            grout_width: Width of grout lines

        Returns:
            Tile texture image
        """
        # Create base
        texture = np.ones((height, width, 3), dtype=np.uint8)
        texture[:, :] = base_color

        # Draw grout lines
        # Vertical lines
        for x in range(0, width, tile_size):
            cv2.line(texture, (x, 0), (x, height), grout_color, grout_width)

        # Horizontal lines
        for y in range(0, height, tile_size):
            cv2.line(texture, (0, y), (width, y), grout_color, grout_width)

        # Add slight variation to tiles
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tile_y_end = min(y + tile_size, height)
                tile_x_end = min(x + tile_size, width)

                variation = np.random.randint(-5, 5)
                texture[y:tile_y_end, x:tile_x_end] = np.clip(
                    texture[y:tile_y_end, x:tile_x_end] + variation,
                    0,
                    255
                )

        return texture

    def generate_brick_texture(
        self,
        width: int,
        height: int,
        brick_width: int = 150,
        brick_height: int = 60,
        base_color: Tuple[int, int, int] = (178, 34, 34),
        mortar_color: Tuple[int, int, int] = (200, 200, 200)
    ) -> np.ndarray:
        """
        Generate brick texture with mortar

        Args:
            width: Texture width
            height: Texture height
            brick_width: Width of each brick
            brick_height: Height of each brick
            base_color: Brick color (BGR)
            mortar_color: Mortar color (BGR)

        Returns:
            Brick texture image
        """
        # Create base (mortar)
        texture = np.ones((height, width, 3), dtype=np.uint8)
        texture[:, :] = mortar_color

        # Draw bricks
        row = 0
        y = 0
        while y < height:
            x_offset = (brick_width // 2) if (row % 2 == 1) else 0
            x = x_offset

            while x < width:
                # Draw brick
                brick_x_end = min(x + brick_width - 5, width)
                brick_y_end = min(y + brick_height - 5, height)

                if brick_x_end > x and brick_y_end > y:
                    # Add variation to brick color
                    variation = np.random.randint(-10, 10, 3)
                    brick_color = np.clip(
                        np.array(base_color) + variation,
                        0,
                        255
                    )

                    cv2.rectangle(
                        texture,
                        (x, y),
                        (brick_x_end, brick_y_end),
                        tuple(map(int, brick_color)),
                        -1
                    )

                x += brick_width

            y += brick_height
            row += 1

        return texture

    def generate_concrete_texture(
        self,
        width: int,
        height: int,
        base_color: Tuple[int, int, int] = (169, 169, 169)
    ) -> np.ndarray:
        """
        Generate concrete texture

        Args:
            width: Texture width
            height: Texture height
            base_color: Concrete color (BGR)

        Returns:
            Concrete texture image
        """
        # Create base
        texture = np.ones((height, width, 3), dtype=np.uint8)
        texture[:, :] = base_color

        # Add noise for concrete aggregate
        noise = np.random.randint(-20, 20, (height, width, 3))
        texture = np.clip(texture.astype(int) + noise, 0, 255).astype(np.uint8)

        # Add larger aggregate spots
        num_spots = (width * height) // 1000
        for _ in range(num_spots):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            radius = np.random.randint(1, 3)
            color = np.clip(
                np.array(base_color) + np.random.randint(-30, 30),
                0,
                255
            )
            cv2.circle(texture, (x, y), radius, tuple(map(int, color)), -1)

        # Apply blur for smooth appearance
        texture = cv2.GaussianBlur(texture, (3, 3), 0)

        return texture

    def adjust_brightness(
        self,
        texture: np.ndarray,
        factor: float
    ) -> np.ndarray:
        """
        Adjust texture brightness

        Args:
            texture: Input texture
            factor: Brightness factor (-1 to 1)

        Returns:
            Adjusted texture
        """
        hsv = cv2.cvtColor(texture, cv2.COLOR_BGR2HSV).astype(float)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * (1 + factor), 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    def tile_texture(
        self,
        texture: np.ndarray,
        target_width: int,
        target_height: int
    ) -> np.ndarray:
        """
        Tile texture to fill larger area

        Args:
            texture: Base texture
            target_width: Target width
            target_height: Target height

        Returns:
            Tiled texture
        """
        tex_h, tex_w = texture.shape[:2]

        # Calculate number of tiles needed
        tiles_x = (target_width // tex_w) + 2
        tiles_y = (target_height // tex_h) + 2

        # Create tiled texture
        tiled = np.tile(texture, (tiles_y, tiles_x, 1))

        # Crop to exact size
        return tiled[:target_height, :target_width]
