"""
RenderEase Flask Backend
Main application file with API endpoints
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from io import BytesIO
from PIL import Image

# Import CV algorithms
from cv_algorithms.edge_detector import EdgeDetector
from cv_algorithms.hough_transform import HoughTransform
from cv_algorithms.segmentation import Segmentation
from cv_algorithms.homography import HomographyTransform
from cv_algorithms.texture_generator import TextureGenerator
from cv_algorithms.advanced_segmentation import AdvancedSegmentation

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = '../uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize CV processors
edge_detector = EdgeDetector()
hough_transform = HoughTransform()
segmentation = Segmentation()
homography_transform = HomographyTransform()
texture_generator = TextureGenerator()
advanced_segmentation = AdvancedSegmentation()


# Helper Functions
def decode_image(image_data: str) -> np.ndarray:
    """
    Decode base64 image to numpy array
    """
    if ',' in image_data:
        image_data = image_data.split(',')[1]

    img_bytes = base64.b64decode(image_data)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return img


def encode_image(image: np.ndarray) -> str:
    """
    Encode numpy array to base64 string
    """
    _, buffer = cv2.imencode('.png', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'RenderEase API is running'})


@app.route('/api/edge-detection', methods=['POST'])
def detect_edges():
    """
    Detect edges in uploaded image using various algorithms
    """
    try:
        data = request.json
        image_data = data.get('image')
        method = data.get('method', 'canny')
        params = data.get('params', {})

        # Decode image
        img = decode_image(image_data)

        # Apply edge detection
        if method == 'canny':
            edges = edge_detector.canny_edge_detection(
                img,
                low_threshold=params.get('low_threshold', 50),
                high_threshold=params.get('high_threshold', 150)
            )
        elif method == 'sobel':
            edges, _, _ = edge_detector.sobel_edge_detection(img)
        elif method == 'laplacian':
            edges = edge_detector.laplacian_edge_detection(img)
        else:
            return jsonify({'error': 'Unknown method'}), 400

        # Encode result
        result_data = encode_image(edges)

        return jsonify({
            'success': True,
            'edges': result_data,
            'method': method
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect-lines', methods=['POST'])
def detect_lines():
    """
    Detect lines using Hough Transform
    """
    try:
        data = request.json
        image_data = data.get('image')
        edge_data = data.get('edges', None)
        params = data.get('params', {})

        # Decode image
        img = decode_image(image_data)

        # Get or compute edges
        if edge_data:
            edges = decode_image(edge_data)
            if len(edges.shape) == 3:
                edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
        else:
            edges = edge_detector.canny_edge_detection(img)

        # Detect lines
        lines = hough_transform.detect_lines(
            edges,
            threshold=params.get('threshold', 100),
            min_line_length=params.get('min_line_length', 50),
            max_line_gap=params.get('max_line_gap', 10)
        )

        # Draw lines on image
        result_img = hough_transform.draw_lines(img, lines)

        # Convert lines to serializable format
        lines_data = [
            {
                'x1': line.x1,
                'y1': line.y1,
                'x2': line.x2,
                'y2': line.y2,
                'rho': float(line.rho),
                'theta': float(line.theta)
            }
            for line in lines
        ]

        # Encode result
        result_data = encode_image(result_img)

        return jsonify({
            'success': True,
            'image': result_data,
            'lines': lines_data,
            'count': len(lines)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/segment', methods=['POST'])
def segment_image():
    """
    Segment image using various algorithms
    """
    try:
        data = request.json
        image_data = data.get('image')
        method = data.get('method', 'color')
        params = data.get('params', {})

        # Decode image
        img = decode_image(image_data)

        # Apply segmentation
        if method == 'color':
            lower = tuple(params.get('lower_bound', [0, 0, 0]))
            upper = tuple(params.get('upper_bound', [255, 255, 255]))
            mask = segmentation.color_based_segmentation(
                img,
                lower,
                upper,
                color_space=params.get('color_space', 'HSV')
            )
        elif method == 'grabcut':
            rect = tuple(params.get('rect', [10, 10, img.shape[1]-20, img.shape[0]-20]))
            mask = segmentation.grabcut_segmentation(img, rect)
            mask = mask * 255
        elif method == 'kmeans':
            segmented, labels = segmentation.kmeans_segmentation(
                img,
                k=params.get('k', 3)
            )
            # Return segmented image instead of mask
            result_data = encode_image(segmented)
            return jsonify({
                'success': True,
                'segmented': result_data,
                'method': method
            })
        else:
            return jsonify({'error': 'Unknown method'}), 400

        # Apply mask to image
        result = cv2.bitwise_and(img, img, mask=mask)

        # Encode results
        result_data = encode_image(result)
        mask_data = encode_image(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))

        return jsonify({
            'success': True,
            'result': result_data,
            'mask': mask_data,
            'method': method
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-texture', methods=['POST'])
def generate_texture():
    """
    Generate procedural texture
    """
    try:
        data = request.json
        texture_type = data.get('type', 'wood')
        width = data.get('width', 512)
        height = data.get('height', 512)
        params = data.get('params', {})

        # Generate texture
        if texture_type == 'wood':
            base_color = tuple(params.get('base_color', [139, 69, 19]))
            texture = texture_generator.generate_wood_texture(
                width,
                height,
                base_color=base_color
            )
        elif texture_type == 'marble':
            base_color = tuple(params.get('base_color', [245, 245, 220]))
            texture = texture_generator.generate_marble_texture(
                width,
                height,
                base_color=base_color
            )
        elif texture_type == 'carpet':
            base_color = tuple(params.get('base_color', [128, 128, 128]))
            texture = texture_generator.generate_carpet_texture(
                width,
                height,
                base_color=base_color
            )
        elif texture_type == 'tile':
            base_color = tuple(params.get('base_color', [255, 255, 255]))
            texture = texture_generator.generate_tile_texture(
                width,
                height,
                base_color=base_color
            )
        elif texture_type == 'brick':
            base_color = tuple(params.get('base_color', [178, 34, 34]))
            texture = texture_generator.generate_brick_texture(
                width,
                height,
                base_color=base_color
            )
        elif texture_type == 'concrete':
            base_color = tuple(params.get('base_color', [169, 169, 169]))
            texture = texture_generator.generate_concrete_texture(
                width,
                height,
                base_color=base_color
            )
        else:
            return jsonify({'error': 'Unknown texture type'}), 400

        # Encode texture
        texture_data = encode_image(texture)

        return jsonify({
            'success': True,
            'texture': texture_data,
            'type': texture_type,
            'width': width,
            'height': height
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/apply-texture', methods=['POST'])
def apply_texture():
    """
    Apply texture to image region with perspective correction
    """
    try:
        data = request.json
        image_data = data.get('image')
        texture_data = data.get('texture')
        corners = data.get('corners')  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        blend_alpha = data.get('blend_alpha', 0.8)
        brightness = data.get('brightness', 0.0)

        # Decode images
        img = decode_image(image_data)
        texture = decode_image(texture_data)

        # Adjust brightness if needed
        if brightness != 0.0:
            texture = texture_generator.adjust_brightness(texture, brightness)

        # Apply texture with perspective
        result = homography_transform.apply_texture_with_perspective(
            img,
            texture,
            corners,
            blend_alpha=blend_alpha
        )

        # Encode result
        result_data = encode_image(result)

        return jsonify({
            'success': True,
            'result': result_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect-surfaces', methods=['POST'])
def detect_surfaces():
    """
    Automatically detect floor/wall/ceiling surfaces
    """
    try:
        data = request.json
        image_data = data.get('image')

        # Decode image
        img = decode_image(image_data)

        # Detect edges
        edges = edge_detector.canny_edge_detection(img)

        # Detect lines
        lines = hough_transform.detect_lines(edges, threshold=100)

        # Filter horizontal and vertical lines
        horizontal_lines = hough_transform.filter_horizontal_lines(lines)
        vertical_lines = hough_transform.filter_vertical_lines(lines)

        # Find intersections (potential corners)
        all_lines = horizontal_lines + vertical_lines
        intersections = hough_transform.find_line_intersections(all_lines)

        # Draw results
        result_img = img.copy()
        result_img = hough_transform.draw_lines(
            result_img,
            horizontal_lines,
            color=(0, 255, 0)
        )
        result_img = hough_transform.draw_lines(
            result_img,
            vertical_lines,
            color=(255, 0, 0)
        )

        # Draw intersections
        for point in intersections:
            if 0 <= point[0] < img.shape[1] and 0 <= point[1] < img.shape[0]:
                cv2.circle(result_img, point, 5, (0, 0, 255), -1)

        # Encode result
        result_data = encode_image(result_img)
        edges_data = encode_image(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))

        return jsonify({
            'success': True,
            'result': result_data,
            'edges': edges_data,
            'horizontal_lines': len(horizontal_lines),
            'vertical_lines': len(vertical_lines),
            'intersections': intersections[:20]  # Limit to first 20
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/advanced-segment', methods=['POST'])
def advanced_segment():
    """
    Advanced segmentation with GrabCut, region growing, etc.
    """
    try:
        data = request.json
        image_data = data.get('image')
        method = data.get('method', 'grabcut')
        params = data.get('params', {})

        # Decode image
        img = decode_image(image_data)

        if method == 'grabcut':
            # Interactive GrabCut
            rect = tuple(params.get('rect', [10, 10, img.shape[1]-20, img.shape[0]-20]))
            iterations = params.get('iterations', 5)

            result = advanced_segmentation.interactive_grabcut(
                img,
                rect,
                iterations=iterations,
                refine=True
            )

            # Apply mask to image
            masked_img = cv2.bitwise_and(img, img, mask=result.refined_mask)

            # Encode results
            result_data = encode_image(masked_img)
            mask_data = encode_image(cv2.cvtColor(result.refined_mask * 255, cv2.COLOR_GRAY2BGR))

            return jsonify({
                'success': True,
                'result': result_data,
                'mask': mask_data,
                'confidence': float(result.confidence),
                'bbox': result.bounding_box,
                'method': 'grabcut'
            })

        elif method == 'region_growing':
            # Region growing from seed point
            seed = tuple(params.get('seed_point', [img.shape[1]//2, img.shape[0]//2]))
            threshold = params.get('threshold', 10)

            mask = advanced_segmentation.region_growing(img, seed, threshold)
            masked_img = cv2.bitwise_and(img, img, mask=mask)

            result_data = encode_image(masked_img)
            mask_data = encode_image(cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR))

            return jsonify({
                'success': True,
                'result': result_data,
                'mask': mask_data,
                'method': 'region_growing'
            })

        elif method == 'flood_fill':
            # Smart flood fill
            seed = tuple(params.get('seed_point', [img.shape[1]//2, img.shape[0]//2]))
            tolerance = params.get('tolerance', 10)

            mask = advanced_segmentation.smart_flood_fill(img, seed, tolerance)
            masked_img = cv2.bitwise_and(img, img, mask=mask)

            result_data = encode_image(masked_img)
            mask_data = encode_image(cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR))

            return jsonify({
                'success': True,
                'result': result_data,
                'mask': mask_data,
                'method': 'flood_fill'
            })

        elif method == 'multi_scale':
            # Multi-scale segmentation
            rect = tuple(params.get('rect', [10, 10, img.shape[1]-20, img.shape[0]-20]))

            mask = advanced_segmentation.multi_scale_segmentation(img, rect)
            masked_img = cv2.bitwise_and(img, img, mask=mask)

            result_data = encode_image(masked_img)
            mask_data = encode_image(cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR))

            return jsonify({
                'success': True,
                'result': result_data,
                'mask': mask_data,
                'method': 'multi_scale'
            })

        else:
            return jsonify({'error': 'Unknown method'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/apply-texture-with-mask', methods=['POST'])
def apply_texture_with_mask():
    """
    Apply texture using precise mask-based blending
    """
    try:
        data = request.json
        image_data = data.get('image')
        texture_data = data.get('texture')
        mask_data = data.get('mask')  # Binary mask
        blend_alpha = data.get('blend_alpha', 0.8)
        brightness = data.get('brightness', 0.0)
        feather = data.get('feather', 5)  # Feathering amount

        # Decode images
        img = decode_image(image_data)
        texture = decode_image(texture_data)
        mask = decode_image(mask_data)

        # Convert mask to single channel if needed
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        # Normalize mask to 0-1
        mask = (mask > 127).astype(np.uint8)

        # Create feathered mask for smooth blending
        feathered_mask = advanced_segmentation.create_feathered_mask(mask, feather)

        # Resize texture to match image
        texture_resized = cv2.resize(texture, (img.shape[1], img.shape[0]))

        # Adjust brightness if needed
        if brightness != 0.0:
            texture_resized = texture_generator.adjust_brightness(texture_resized, brightness)

        # Blend using feathered mask
        feathered_mask_3ch = cv2.cvtColor((feathered_mask * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR) / 255.0

        result = img.astype(float) * (1 - feathered_mask_3ch * blend_alpha) + \
                 texture_resized.astype(float) * feathered_mask_3ch * blend_alpha

        result = np.clip(result, 0, 255).astype(np.uint8)

        # Encode result
        result_data = encode_image(result)

        return jsonify({
            'success': True,
            'result': result_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-complete', methods=['POST'])
def process_complete():
    """
    Complete processing pipeline: detect surfaces, apply texture
    """
    try:
        data = request.json
        image_data = data.get('image')
        texture_type = data.get('texture_type', 'wood')
        auto_detect = data.get('auto_detect', False)
        region = data.get('region', None)  # {x, y, width, height}

        # Decode image
        img = decode_image(image_data)

        # Generate texture
        tex_params = data.get('texture_params', {})
        if texture_type == 'wood':
            texture = texture_generator.generate_wood_texture(512, 512)
        elif texture_type == 'carpet':
            texture = texture_generator.generate_carpet_texture(512, 512)
        else:
            texture = texture_generator.generate_tile_texture(512, 512)

        # Determine corners
        if auto_detect:
            # Auto-detect (simplified - use provided region or default)
            if region:
                x, y, w, h = region['x'], region['y'], region['width'], region['height']
            else:
                h, w = img.shape[:2]
                x, y = 0, int(h * 0.6)
                w, h = w, int(h * 0.4)

            corners = [
                [x, y],
                [x + w, y],
                [x + w, y + h],
                [x, y + h]
            ]
        else:
            corners = data.get('corners', [[0, 0], [100, 0], [100, 100], [0, 100]])

        # Apply texture
        result = homography_transform.apply_texture_with_perspective(
            img,
            texture,
            corners,
            blend_alpha=data.get('blend_alpha', 0.8)
        )

        # Encode result
        result_data = encode_image(result)

        return jsonify({
            'success': True,
            'result': result_data,
            'corners': corners
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("RenderEase Backend Server")
    print("=" * 50)
    print("Server running on http://localhost:5001")
    print("API endpoints available:")
    print("  - POST /api/edge-detection")
    print("  - POST /api/detect-lines")
    print("  - POST /api/segment")
    print("  - POST /api/generate-texture")
    print("  - POST /api/apply-texture")
    print("  - POST /api/detect-surfaces")
    print("  - POST /api/advanced-segment      [NEW]")
    print("  - POST /api/apply-texture-with-mask [NEW]")
    print("  - POST /api/process-complete")
    print("=" * 50)
    print("Note: Using port 5001 (port 5000 often used by macOS AirPlay)")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5001)
