#!/usr/bin/env python3
"""
RenderEase Quick Start Script
Run this to test everything immediately!
"""

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")

    required = {
        "cv2": "opencv-python",
        "numpy": "numpy",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "seaborn": "seaborn",
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package}")
            missing.append(package)

    if missing:
        print(f"\n⚠  Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")

        response = input("\nInstall now? (y/n): ")
        if response.lower() == "y":
            for package in missing:
                print(f"\nInstalling {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package])
            print("\n✓ Installation complete!")
        else:
            print("\nPlease install dependencies before continuing.")
            return False
    else:
        print("\n✓ All dependencies installed!")

    return True


def quick_demo():
    """Run a quick demonstration."""
    print("\n" + "=" * 60)
    print("RENDEREASE QUICK DEMO")
    print("=" * 60)

    # Import after checking dependencies
    try:
        from test_suite import create_test_images, test_classical_method
        from renderease import process_room
        from evaluation import RenderEaseEvaluator
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("Please ensure all files are in the current directory.")
        return

    print("\n[1/3] Creating test images...")
    room_path, texture_path, gt_path = create_test_images()

    print("\n[2/3] Processing with classical method...")
    result = process_room(room_path, texture_path, method="classical")

    print("\n[3/3] Evaluating result...")
    evaluator = RenderEaseEvaluator()
    mask_path = Path("outputs") / "test_room_classical_mask.png"

    if mask_path.exists():
        metrics = evaluator.evaluate_single(str(mask_path), gt_path)

        print(f"\n{'='*60}")
        print("RESULTS")
        print(f"{'='*60}")
        print(f"Processing Time:    {result['segmentation_time']:.3f}s")
        print(f"IoU Score:          {metrics['iou']:.3f}")
        print(f"Pixel Accuracy:     {metrics['pixel_accuracy']:.3f}")
        print(f"Success (IoU>0.7):  {'✓' if metrics['success'] else '✗'}")
        print(f"\nOutput saved to:    {result['output_path']}")
        print(f"{'='*60}")

        print("\n✓ Demo complete!")
        print(f"\nCheck these directories:")
        print(f"  - outputs/     (for results)")
        print(f"  - test_data/   (for test images)")
    else:
        print("⚠ Mask file not found")


def show_next_steps():
    """Show user what to do next."""
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)

    print(
        """
1. Run the full test suite:
   python test_suite.py --all

2. Process your own images:
   python -c "from renderease import process_room; \\
              process_room('room.jpg', 'texture.jpg', 'classical')"

3. Evaluate results:
   python -c "from evaluation import compare_all_methods; \\
              compare_all_methods('outputs/', 'outputs/', 'outputs/', 'test_data/')"

4. Read the README:
   cat README.md   # or open README.md in your editor

5. For your report, get comparison data:
   python test_suite.py --all
   # Then check outputs/method_comparison.csv

Need help? Read README.md for complete documentation!
    """
    )


def main():
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║                    RENDEREASE QUICK START                    ║
║          Surface Segmentation & Texture Transfer             ║
╚══════════════════════════════════════════════════════════════╝
    """
    )

    # Check dependencies
    if not check_dependencies():
        return

    # Ask user what to do
    print("\nWhat would you like to do?")
    print("  1. Run quick demo (recommended)")
    print("  2. Run full test suite")
    print("  3. Show next steps")
    print("  4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        quick_demo()
        show_next_steps()
    elif choice == "2":
        print("\nRunning full test suite...")
        subprocess.run([sys.executable, "test_suite.py", "--all"])
        show_next_steps()
    elif choice == "3":
        show_next_steps()
    else:
        print("\nExiting. Run this script again anytime!")
        print("Or run: python test_suite.py --all")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTry running: python test_suite.py --all")
        import traceback

        traceback.print_exc()
