"""
RenderEase Test Suite
Complete testing script with examples
"""

import cv2
import numpy as np
from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from renderease import RenderEase, process_room
from evaluation import RenderEaseEvaluator, compare_all_methods


def create_test_images():
    """Create synthetic test images for quick testing."""
    print("\n" + "=" * 60)
    print("CREATING TEST IMAGES")
    print("=" * 60 + "\n")

    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)

    # Create a simple room image (800x600)
    room_img = np.ones((600, 800, 3), dtype=np.uint8) * 200

    # Draw a simple wall (light gray rectangle)
    cv2.rectangle(room_img, (100, 50), (700, 500), (220, 220, 220), -1)

    # Add some "furniture" (dark rectangles)
    cv2.rectangle(room_img, (150, 400), (300, 550), (80, 80, 80), -1)
    cv2.rectangle(room_img, (600, 350), (680, 550), (80, 80, 80), -1)

    # Add texture to make it look more realistic
    noise = np.random.randint(-20, 20, room_img.shape, dtype=np.int16)
    room_img = np.clip(room_img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Save room image
    room_path = test_dir / "test_room.jpg"
    cv2.imwrite(str(room_path), room_img)
    print(f"✓ Created test room: {room_path}")

    # Create a brick texture (400x400)
    texture_img = np.ones((400, 400, 3), dtype=np.uint8)

    # Red brick color
    texture_img[:, :] = [50, 50, 180]  # BGR format

    # Draw brick pattern
    brick_h, brick_w = 40, 80
    mortar_color = [180, 180, 180]

    for y in range(0, 400, brick_h):
        for x in range(0, 400, brick_w):
            # Offset every other row
            x_offset = brick_w // 2 if (y // brick_h) % 2 == 1 else 0
            x_pos = (x + x_offset) % 400

            # Draw mortar lines
            cv2.rectangle(
                texture_img,
                (x_pos, y),
                (x_pos + brick_w - 2, y + brick_h - 2),
                mortar_color,
                2,
            )

    # Add slight texture variation
    noise = np.random.randint(-15, 15, texture_img.shape, dtype=np.int16)
    texture_img = np.clip(texture_img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    texture_path = test_dir / "brick_texture.jpg"
    cv2.imwrite(str(texture_path), texture_img)
    print(f"✓ Created brick texture: {texture_path}")

    # Create ground truth mask for evaluation
    gt_mask = np.zeros((600, 800), dtype=np.uint8)
    cv2.rectangle(gt_mask, (100, 50), (700, 500), 255, -1)

    gt_path = test_dir / "test_room_gt_mask.png"
    cv2.imwrite(str(gt_path), gt_mask)
    print(f"✓ Created ground truth mask: {gt_path}")

    print(f"\n✓ Test images created in: {test_dir}")

    return str(room_path), str(texture_path), str(gt_path)


def test_classical_method():
    """Test classical segmentation method."""
    print("\n" + "=" * 60)
    print("TEST 1: CLASSICAL METHOD (Hough + Edges)")
    print("=" * 60)

    room_path, texture_path, gt_path = create_test_images()

    # Process with classical method
    system = RenderEase(method="classical", save_intermediates=True)
    result = system.process_image(room_path, texture_path, surface_type="wall")

    print("\n✓ Classical method test complete")
    return result


def test_all_methods():
    """Test all three methods on the same image."""
    print("\n" + "=" * 60)
    print("TEST 2: COMPARE ALL METHODS")
    print("=" * 60)

    room_path, texture_path, gt_path = create_test_images()

    results = {}

    # Test each method
    for method in ["classical", "deeplab", "sam"]:
        try:
            print(f"\n--- Testing {method.upper()} ---")
            result = process_room(room_path, texture_path, method=method)
            results[method] = result
        except Exception as e:
            print(f"⚠ {method} test failed: {e}")
            results[method] = None

    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")

    for method, result in results.items():
        if result:
            print(f"\n{method.upper()}:")
            print(f"  - Time: {result['segmentation_time']:.3f}s")
            print(f"  - Coverage: {result['mask_area_ratio']*100:.1f}%")
            print(f"  - Output: {result['output_path']}")

    return results


def test_evaluation():
    """Test evaluation metrics."""
    print("\n" + "=" * 60)
    print("TEST 3: EVALUATION METRICS")
    print("=" * 60)

    # First, generate results
    room_path, texture_path, gt_path = create_test_images()

    # Process with classical method
    print("\nGenerating results for evaluation...")
    result = process_room(room_path, texture_path, method="classical")

    # Evaluate
    print("\nEvaluating results...")
    evaluator = RenderEaseEvaluator()

    # Find the generated mask
    mask_path = Path("outputs") / "test_room_classical_mask.png"

    if mask_path.exists():
        metrics = evaluator.evaluate_single(str(mask_path), gt_path)

        print(f"\n{'='*60}")
        print("EVALUATION RESULTS")
        print(f"{'='*60}")
        print(f"IoU:            {metrics['iou']:.3f}")
        print(f"Pixel Accuracy: {metrics['pixel_accuracy']:.3f}")
        print(f"Boundary F1:    {metrics['boundary_f1']:.3f}")
        print(f"Success:        {'✓' if metrics['success'] else '✗'}")
        print(f"{'='*60}")

        return metrics
    else:
        print("⚠ Mask file not found for evaluation")
        return None


def test_batch_processing():
    """Test batch processing of multiple images."""
    print("\n" + "=" * 60)
    print("TEST 4: BATCH PROCESSING")
    print("=" * 60)

    # Create multiple test images
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)

    print("\nCreating batch of test images...")

    for i in range(3):
        # Create slightly different room images
        room_img = np.ones((600, 800, 3), dtype=np.uint8) * (180 + i * 20)

        # Wall region (slightly different each time)
        wall_x1 = 100 + i * 10
        wall_x2 = 700 - i * 10
        cv2.rectangle(room_img, (wall_x1, 50), (wall_x2, 500), (220, 220, 220), -1)

        # Add noise
        noise = np.random.randint(-20, 20, room_img.shape, dtype=np.int16)
        room_img = np.clip(room_img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Save
        room_path = test_dir / f"room_{i+1}.jpg"
        cv2.imwrite(str(room_path), room_img)
        print(f"✓ Created {room_path}")

        # Create GT mask
        gt_mask = np.zeros((600, 800), dtype=np.uint8)
        cv2.rectangle(gt_mask, (wall_x1, 50), (wall_x2, 500), 255, -1)
        gt_path = test_dir / f"room_{i+1}_gt_mask.png"
        cv2.imwrite(str(gt_path), gt_mask)

    # Create texture
    texture_path = test_dir / "brick_texture.jpg"
    if not texture_path.exists():
        texture_img = np.ones((400, 400, 3), dtype=np.uint8) * 150
        cv2.imwrite(str(texture_path), texture_img)

    # Process all images
    print("\nProcessing batch...")
    system = RenderEase(method="classical")

    results = []
    for i in range(3):
        room_path = test_dir / f"room_{i+1}.jpg"
        result = system.process_image(str(room_path), str(texture_path))
        results.append(result)

    print(f"\n✓ Batch processing complete: {len(results)} images processed")

    return results


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "=" * 70)
    print(" " * 20 + "RENDEREASE TEST SUITE")
    print("=" * 70)

    tests_passed = 0
    tests_failed = 0

    # Test 1: Classical method
    try:
        test_classical_method()
        tests_passed += 1
        print("\n✓ Test 1 PASSED")
    except Exception as e:
        tests_failed += 1
        print(f"\n✗ Test 1 FAILED: {e}")

    # Test 2: All methods comparison
    try:
        test_all_methods()
        tests_passed += 1
        print("\n✓ Test 2 PASSED")
    except Exception as e:
        tests_failed += 1
        print(f"\n✗ Test 2 FAILED: {e}")

    # Test 3: Evaluation
    try:
        test_evaluation()
        tests_passed += 1
        print("\n✓ Test 3 PASSED")
    except Exception as e:
        tests_failed += 1
        print(f"\n✗ Test 3 FAILED: {e}")

    # Test 4: Batch processing
    try:
        test_batch_processing()
        tests_passed += 1
        print("\n✓ Test 4 PASSED")
    except Exception as e:
        tests_failed += 1
        print(f"\n✗ Test 4 FAILED: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
    print("=" * 70 + "\n")

    print("✓ Check the 'outputs' directory for results!")
    print("✓ Check the 'test_data' directory for test images!")


def demo_with_real_image():
    """
    Demo function for processing your own images.
    Replace paths with your actual image paths.
    """
    print("\n" + "=" * 60)
    print("DEMO: PROCESS YOUR OWN IMAGES")
    print("=" * 60)

    # TODO: Replace these with your actual image paths
    room_image = "path/to/your/room.jpg"
    texture_image = "path/to/your/texture.jpg"

    print(
        """
To use this demo with your own images:

1. Place your room image in the project directory
2. Place your texture image in the project directory
3. Update the paths in this function
4. Run: python test_suite.py --demo

Example:
    room_image = "my_room.jpg"
    texture_image = "wood_floor.jpg"
    
Then call:
    result = process_room(room_image, texture_image, 
                         method='classical', 
                         surface_type='floor')
    """
    )

    # Uncomment when you have real images:
    # result = process_room(room_image, texture_image,
    #                      method='classical',
    #                      surface_type='wall')
    #
    # print(f"\n✓ Result saved to: {result['output_path']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RenderEase Test Suite")
    parser.add_argument(
        "--test", type=int, choices=[1, 2, 3, 4], help="Run specific test (1-4)"
    )
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument(
        "--demo", action="store_true", help="Show demo for your own images"
    )

    args = parser.parse_args()

    if args.test == 1:
        test_classical_method()
    elif args.test == 2:
        test_all_methods()
    elif args.test == 3:
        test_evaluation()
    elif args.test == 4:
        test_batch_processing()
    elif args.all or len(sys.argv) == 1:
        run_all_tests()
    elif args.demo:
        demo_with_real_image()
    else:
        print("Usage: python test_suite.py [--test N] [--all] [--demo]")
        print("\nOptions:")
        print("  --test 1    Test classical method")
        print("  --test 2    Test all methods")
        print("  --test 3    Test evaluation")
        print("  --test 4    Test batch processing")
        print("  --all       Run all tests (default)")
        print("  --demo      Show demo instructions")
