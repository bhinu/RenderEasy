# This is Evaluation and Benchmark

## ⚙️ Environment Setup

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

### Comparative Analysis: Traditional vs Deep Learning Segmentation

This branch focuses on **evaluating and comparing** traditional computer vision and deep learning segmentation methods for indoor scenes.  
The goal is to **measure segmentation accuracy, texture replacement quality, and computational efficiency**, enabling precise overlays (like Photoshop’s select-and-replace feature) while minimizing CPU/GPU usage.


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

