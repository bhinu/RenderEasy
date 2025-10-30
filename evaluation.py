"""
RenderEase Evaluation Module
Computes metrics and compares different segmentation methods
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class RenderEaseEvaluator:
    """Evaluate segmentation quality and compare methods."""

    def __init__(self, results_dir="outputs"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)

    def compute_iou(self, pred_mask: np.ndarray, gt_mask: np.ndarray) -> float:
        """
        Compute Intersection over Union.

        Args:
            pred_mask: Predicted binary mask
            gt_mask: Ground truth binary mask

        Returns:
            IoU score (0-1)
        """
        # Ensure binary
        pred = (pred_mask > 127).astype(np.uint8)
        gt = (gt_mask > 127).astype(np.uint8)

        # Resize if needed
        if pred.shape != gt.shape:
            pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]))

        intersection = np.logical_and(pred, gt).sum()
        union = np.logical_or(pred, gt).sum()

        if union == 0:
            return 0.0

        return float(intersection) / float(union)

    def compute_pixel_accuracy(
        self, pred_mask: np.ndarray, gt_mask: np.ndarray
    ) -> float:
        """Compute pixel-wise accuracy."""
        pred = (pred_mask > 127).astype(np.uint8)
        gt = (gt_mask > 127).astype(np.uint8)

        if pred.shape != gt.shape:
            pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]))

        correct = (pred == gt).sum()
        total = pred.size

        return correct / total

    def compute_boundary_f1(
        self, pred_mask: np.ndarray, gt_mask: np.ndarray, threshold=2
    ) -> float:
        """
        Compute F1 score for boundary pixels.

        Args:
            pred_mask: Predicted mask
            gt_mask: Ground truth mask
            threshold: Distance threshold for boundary matching (pixels)
        """
        pred = (pred_mask > 127).astype(np.uint8)
        gt = (gt_mask > 127).astype(np.uint8)

        if pred.shape != gt.shape:
            pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]))

        # Extract boundaries
        pred_boundary = cv2.Canny(pred * 255, 100, 200)
        gt_boundary = cv2.Canny(gt * 255, 100, 200)

        # Dilate GT boundary for matching
        kernel = np.ones((threshold * 2 + 1, threshold * 2 + 1), np.uint8)
        gt_boundary_dilated = cv2.dilate(gt_boundary, kernel, iterations=1)

        # Compute precision and recall
        pred_boundary_pts = np.sum(pred_boundary > 0)
        gt_boundary_pts = np.sum(gt_boundary > 0)

        if pred_boundary_pts == 0 or gt_boundary_pts == 0:
            return 0.0

        true_positives = np.sum(np.logical_and(pred_boundary, gt_boundary_dilated))

        precision = true_positives / pred_boundary_pts if pred_boundary_pts > 0 else 0
        recall = true_positives / gt_boundary_pts if gt_boundary_pts > 0 else 0

        if precision + recall == 0:
            return 0.0

        f1 = 2 * (precision * recall) / (precision + recall)
        return f1

    def evaluate_single(self, pred_mask_path: str, gt_mask_path: str) -> Dict:
        """
        Evaluate a single prediction against ground truth.

        Returns:
            Dictionary with all metrics
        """
        pred_mask = cv2.imread(pred_mask_path, cv2.IMREAD_GRAYSCALE)
        gt_mask = cv2.imread(gt_mask_path, cv2.IMREAD_GRAYSCALE)

        if pred_mask is None or gt_mask is None:
            raise FileNotFoundError(f"Could not load masks")

        iou = self.compute_iou(pred_mask, gt_mask)
        pixel_acc = self.compute_pixel_accuracy(pred_mask, gt_mask)
        boundary_f1 = self.compute_boundary_f1(pred_mask, gt_mask)

        return {
            "iou": iou,
            "pixel_accuracy": pixel_acc,
            "boundary_f1": boundary_f1,
            "success": iou > 0.7,
        }

    def evaluate_batch(
        self, pred_dir: str, gt_dir: str, method_name: str = "method"
    ) -> pd.DataFrame:
        """
        Evaluate all predictions in a directory.

        Args:
            pred_dir: Directory with predicted masks
            gt_dir: Directory with ground truth masks
            method_name: Name of the method being evaluated

        Returns:
            DataFrame with results for each image
        """
        pred_dir = Path(pred_dir)
        gt_dir = Path(gt_dir)

        results = []

        # Find all mask files
        mask_files = list(pred_dir.glob("*_mask.png"))

        print(f"\nEvaluating {method_name}...")
        print(f"Found {len(mask_files)} prediction masks\n")

        for pred_path in mask_files:
            # Find corresponding GT
            base_name = pred_path.name.replace(f"_{method_name}_mask.png", "")
            gt_path = gt_dir / f"{base_name}_gt_mask.png"

            if not gt_path.exists():
                print(f"⚠ No GT for {pred_path.name}, skipping...")
                continue

            try:
                metrics = self.evaluate_single(str(pred_path), str(gt_path))
                metrics["image"] = base_name
                metrics["method"] = method_name
                results.append(metrics)

                print(
                    f"✓ {base_name}: IoU={metrics['iou']:.3f}, "
                    f"Acc={metrics['pixel_accuracy']:.3f}, "
                    f"BF1={metrics['boundary_f1']:.3f}"
                )

            except Exception as e:
                print(f"✗ Error processing {pred_path.name}: {e}")

        if not results:
            print("⚠ No results to evaluate!")
            return pd.DataFrame()

        df = pd.DataFrame(results)

        # Print summary
        print(f"\n{'='*60}")
        print(f"SUMMARY: {method_name}")
        print(f"{'='*60}")
        print(f"Images evaluated:     {len(df)}")
        print(f"Average IoU:          {df['iou'].mean():.3f}")
        print(f"Average Pixel Acc:    {df['pixel_accuracy'].mean():.3f}")
        print(f"Average Boundary F1:  {df['boundary_f1'].mean():.3f}")
        print(f"Success Rate (>0.7):  {df['success'].mean()*100:.1f}%")
        print(f"Best IoU:             {df['iou'].max():.3f}")
        print(f"Worst IoU:            {df['iou'].min():.3f}")
        print(f"{'='*60}\n")

        return df

    def compare_methods(self, results_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Compare multiple methods.

        Args:
            results_dfs: Dictionary mapping method name to results DataFrame

        Returns:
            Comparison DataFrame
        """
        comparison = []

        for method, df in results_dfs.items():
            if df.empty:
                continue

            comparison.append(
                {
                    "Method": method,
                    "Avg IoU": df["iou"].mean(),
                    "Std IoU": df["iou"].std(),
                    "Avg Pixel Acc": df["pixel_accuracy"].mean(),
                    "Avg Boundary F1": df["boundary_f1"].mean(),
                    "Success Rate": df["success"].mean(),
                    "Num Images": len(df),
                }
            )

        comparison_df = pd.DataFrame(comparison)

        print(f"\n{'='*70}")
        print("METHOD COMPARISON")
        print(f"{'='*70}")
        print(comparison_df.to_string(index=False))
        print(f"{'='*70}\n")

        return comparison_df

    def plot_comparison(
        self, results_dfs: Dict[str, pd.DataFrame], save_path: str = None
    ):
        """Create comparison plots."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Prepare data
        methods = list(results_dfs.keys())
        iou_scores = [df["iou"].mean() for df in results_dfs.values()]
        pixel_accs = [df["pixel_accuracy"].mean() for df in results_dfs.values()]
        boundary_f1s = [df["boundary_f1"].mean() for df in results_dfs.values()]
        success_rates = [df["success"].mean() for df in results_dfs.values()]

        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]

        # Plot 1: IoU Comparison
        axes[0, 0].bar(methods, iou_scores, color=colors[: len(methods)], alpha=0.7)
        axes[0, 0].set_ylabel("IoU Score", fontsize=12)
        axes[0, 0].set_title(
            "Segmentation Accuracy (IoU)", fontsize=13, fontweight="bold"
        )
        axes[0, 0].set_ylim([0, 1])
        axes[0, 0].axhline(
            y=0.7, color="red", linestyle="--", label="Success Threshold", linewidth=2
        )
        axes[0, 0].legend()
        axes[0, 0].grid(axis="y", alpha=0.3)

        # Plot 2: Pixel Accuracy
        axes[0, 1].bar(methods, pixel_accs, color=colors[: len(methods)], alpha=0.7)
        axes[0, 1].set_ylabel("Pixel Accuracy", fontsize=12)
        axes[0, 1].set_title("Pixel-wise Accuracy", fontsize=13, fontweight="bold")
        axes[0, 1].set_ylim([0, 1])
        axes[0, 1].grid(axis="y", alpha=0.3)

        # Plot 3: Boundary F1
        axes[1, 0].bar(methods, boundary_f1s, color=colors[: len(methods)], alpha=0.7)
        axes[1, 0].set_ylabel("Boundary F1 Score", fontsize=12)
        axes[1, 0].set_title(
            "Boundary Detection Quality", fontsize=13, fontweight="bold"
        )
        axes[1, 0].set_ylim([0, 1])
        axes[1, 0].grid(axis="y", alpha=0.3)

        # Plot 4: Success Rate
        axes[1, 1].bar(methods, success_rates, color=colors[: len(methods)], alpha=0.7)
        axes[1, 1].set_ylabel("Success Rate", fontsize=12)
        axes[1, 1].set_title("Success Rate (IoU > 0.7)", fontsize=13, fontweight="bold")
        axes[1, 1].set_ylim([0, 1])
        axes[1, 1].grid(axis="y", alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"✓ Saved comparison plot: {save_path}")
        else:
            plt.savefig(
                self.results_dir / "method_comparison.png", dpi=300, bbox_inches="tight"
            )
            print(
                f"✓ Saved comparison plot: {self.results_dir / 'method_comparison.png'}"
            )

        plt.close()

    def plot_per_image_comparison(
        self, results_dfs: Dict[str, pd.DataFrame], save_path: str = None
    ):
        """Plot IoU for each image across methods."""
        # Merge dataframes
        merged = None
        for method, df in results_dfs.items():
            if df.empty:
                continue
            df_subset = df[["image", "iou"]].copy()
            df_subset.columns = ["image", method]

            if merged is None:
                merged = df_subset
            else:
                merged = merged.merge(df_subset, on="image", how="outer")

        if merged is None or len(merged) == 0:
            print("⚠ No data to plot per-image comparison")
            return

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))

        x = np.arange(len(merged))
        width = 0.8 / len(results_dfs)

        for i, method in enumerate(results_dfs.keys()):
            if method in merged.columns:
                offset = width * (i - len(results_dfs) / 2 + 0.5)
                ax.bar(x + offset, merged[method], width, label=method, alpha=0.8)

        ax.set_xlabel("Image", fontsize=12)
        ax.set_ylabel("IoU Score", fontsize=12)
        ax.set_title("Per-Image IoU Comparison", fontsize=14, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(merged["image"], rotation=45, ha="right")
        ax.legend()
        ax.axhline(
            y=0.7, color="red", linestyle="--", linewidth=2, label="Success Threshold"
        )
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.savefig(
                self.results_dir / "per_image_comparison.png",
                dpi=300,
                bbox_inches="tight",
            )

        plt.close()
        print(f"✓ Saved per-image comparison plot")

    def analyze_runtime(self, metrics_files: List[str]) -> pd.DataFrame:
        """Analyze runtime performance from metrics files."""
        results = []

        for metrics_file in metrics_files:
            with open(metrics_file, "r") as f:
                data = json.load(f)

            results.append(
                {
                    "method": data["method"],
                    "image": data["image"],
                    "segmentation_time": data["segmentation_time"],
                }
            )

        df = pd.DataFrame(results)

        # Group by method
        summary = df.groupby("method")["segmentation_time"].agg(
            ["mean", "std", "min", "max"]
        )
        summary.columns = [
            "Avg Time (s)",
            "Std Time (s)",
            "Min Time (s)",
            "Max Time (s)",
        ]

        print(f"\n{'='*60}")
        print("RUNTIME ANALYSIS")
        print(f"{'='*60}")
        print(summary)
        print(f"{'='*60}\n")

        return summary


# Convenience functions
def quick_evaluate(pred_mask: str, gt_mask: str) -> Dict:
    """Quick evaluation of a single mask."""
    evaluator = RenderEaseEvaluator()
    return evaluator.evaluate_single(pred_mask, gt_mask)


def batch_evaluate(pred_dir: str, gt_dir: str, method: str = "method") -> pd.DataFrame:
    """Quick batch evaluation."""
    evaluator = RenderEaseEvaluator()
    return evaluator.evaluate_batch(pred_dir, gt_dir, method)


def compare_all_methods(
    classical_dir: str, deeplab_dir: str, sam_dir: str, gt_dir: str
):
    """Compare all three methods."""
    evaluator = RenderEaseEvaluator()

    # Evaluate each method
    results = {}

    if Path(classical_dir).exists():
        results["Classical"] = evaluator.evaluate_batch(
            classical_dir, gt_dir, "classical"
        )

    if Path(deeplab_dir).exists():
        results["DeepLab"] = evaluator.evaluate_batch(deeplab_dir, gt_dir, "deeplab")

    if Path(sam_dir).exists():
        results["SAM"] = evaluator.evaluate_batch(sam_dir, gt_dir, "sam")

    # Compare
    if results:
        comparison = evaluator.compare_methods(results)
        evaluator.plot_comparison(results)
        evaluator.plot_per_image_comparison(results)

        return comparison, results

    return None, None
