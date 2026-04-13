# Voxel Centroid Documentation

**High-precision 3D geometric centroid computation through voxelization**

## Overview

This library computes the geometric centroid (center of mass) of 3D objects from point clouds with subpixel accuracy. Works with concave shapes, cavities, and noisy data.

## Installation

```bash
pip install voxel-centroid
```

## Quick Start

```python
import numpy as np
from voxel_centroid import VoxelCentroid, VoxelConfig

# Generate sample points
points = np.random.randn(10000, 3)

# Configure algorithm
config = VoxelConfig(resolution=150, mode='subpixel')

# Compute centroid
centroid = VoxelCentroid(config).fit(points)
print(f"Centroid: {centroid}")
```

## Features

- 🎯 **Subpixel accuracy** - Error < 0.01% on test shapes
- ⚡ **High performance** - 50,000 points in ~0.05 seconds
- 📦 **Multi-format support** - PLY, STL, OBJ, XYZ, PCD, LAS, NPY
- 🛡️ **Noise robust** - Stable with up to 10% noise
- 🔧 **5 operation modes** - Balance accuracy vs speed

## Operation Modes

| Mode | Accuracy | Speed | Use Case |
|------|----------|-------|----------|
| `standard` | 0.7% | 0.08s | General purpose |
| `subpixel` | **0.01%** | 0.31s | Medical, aerospace |
| `adaptive` | 0.7% | 0.14s | Non-uniform data |
| `ensemble` | 0.3% | 0.50s | Critical calculations |
| `iterative` | 0.7% | 1.92s | Multi-component objects |

## API Reference

### VoxelConfig

Configuration class for the algorithm.

**Parameters:**
- `resolution` (int) - Voxel grid resolution (50-500, default 150)
- `mode` (str) - Operation mode ('standard', 'subpixel', 'adaptive', 'ensemble', 'iterative')
- `fill_holes` (bool) - Fill internal cavities (default True)
- `verbose` (bool) - Enable detailed output (default False)

### VoxelCentroid

Main class for centroid computation.

**Methods:**
- `fit(points)` - Compute centroid from point cloud
- `get_centroid()` - Return computed centroid
- `get_metrics()` - Return computation metrics
- `get_voxel_centers()` - Return coordinates of all filled voxels

## Examples

### Load from file

```python
from voxel_centroid import DataLoader

points = DataLoader.load_from_file("model.ply")
```

### High-precision mode

```python
config = VoxelConfig(resolution=200, mode='subpixel', fill_holes=True)
centroid = VoxelCentroid(config).fit(points)
```

### Get metrics

```python
algo = VoxelCentroid(config)
centroid = algo.fit(points)
metrics = algo.get_metrics()
print(f"Time: {metrics['time_seconds']:.3f}s")
print(f"Voxels: {metrics['total_voxels']}")
```

## License

MIT License

## Links

- [GitHub Repository](https://github.com/SkyGliderus/voxel-centroid)
- [PyPI Package](https://pypi.org/project/voxel-centroid/)