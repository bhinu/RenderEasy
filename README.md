# This is Evaluation and Benchmark

## Comparative Analysis: Traditional vs Deep Learning Segmentation

This branch focuses on **evaluating and comparing** traditional computer vision and deep learning segmentation methods for indoor scenes.  
The goal is to **measure segmentation accuracy, texture replacement quality, and computational efficiency**, enabling precise overlays (like Photoshop’s select-and-replace feature) while minimizing CPU/GPU usage.

## Environment Setup

```bash
# Create Python environment 
# Option 1 - use conda:
conda create -n renderease python=3.10
conda activate renderease

# Option 2 - use venv
python -m venv venv
source /venv/bin/activate # for bash
```

```bash
# Install dependencies
pip install torch torchvision opencv-python scikit-image segmentation-models-pytorch matplotlib pandas
```

## Evaluation Objectives

- Compare **traditional computer vision segmentation techniques** and **deep learning segmentation models**.
- Evaluate **accuracy, boundary precision, and visual realism** of texture/object replacement.  
- Assess **computational efficiency** for practical deployment on mid-range CPUs/GPUs.

## DataSets

We focus on indoor datasets with **ground truth annotations** for semantic and planar surfaces.

| Dataset | Modality | Annotations | Use Case |
|:--------|:---------|:------------|:---------|
| **[NYU Depth V2](https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html)** | RGB-D | Pixel-wise semantic labels | Baseline segmentation evaluation |
| **[Structured3D](https://structured3d-dataset.org/)** | Synthetic RGB-D | Semantic + plane + material | Texture replacement realism |
| **[Hypersim](https://machinelearning.apple.com/research/hypersim)** | Synthetic RGB | Semantic + material + reflectance | Realistic texture overlay evaluation |



## Evaluation Metrics

| Category | Metric | Description |
| :--- | :--- | :--- |
| **Segmentation Accuracy** | IoU (Intersection over Union) | Overlap with ground truth masks |
| **Segmentation Accuracy** | Mean IoU (mIoU) | Average IoU across all target classes (walls, floors, ceilings) |
| **Segmentation Accuracy** | Pixel Accuracy | Fraction of correctly classified pixels |
| **Segmentation Accuracy** | Boundary Precision / Recall (BPR) | Accuracy of object/surface boundaries |
| **Visual Quality** | SSIM (Structural Similarity) | Structural similarity after texture replacement |
| **Visual Quality** | PSNR (Peak Signal-to-Noise Ratio) | Quantifies texture fidelity vs reference |
| **Visual Quality** | LPIPS (optional) | Perceptual similarity metric for realism |
| **Efficiency** | Inference Time | Average runtime per image (CPU/GPU) |
| **Efficiency** | Memory Usage | Peak RAM or GPU memory during inference |

## Stage 1 - Segmentation Accuracy Comparision (we are currently on)

## Stage 2 - Image Overlay Quality Comparision

## Output Structure

evaluation/
│
├── metrics/
│   ├── traditional_results.csv
│   ├── deeplearning_results.csv
│   ├── comparison_summary.csv
│
├── visuals/
│   ├── masks_side_by_side/
│   ├── overlay_comparisons/
│   └── charts/
│       ├── accuracy_vs_runtime.png
│       ├── boundary_precision.png
│       └── ssim_comparison.png
│
└── logs/
    ├── runtime_profiles.txt
    └── memory_usage.txt

