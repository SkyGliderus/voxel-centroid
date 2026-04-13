# Voxel Centroid

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/SkyGliderus/voxel-centroid)](https://github.com/SkyGliderus/voxel-centroid/releases)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/SkyGliderus/voxel-centroid)](https://github.com/SkyGliderus/voxel-centroid)
[![GitHub last commit](https://img.shields.io/github/last-commit/SkyGliderus/voxel-centroid)](https://github.com/SkyGliderus/voxel-centroid)

**High-precision 3D geometric centroid computation through voxelization**

Compute the geometric centroid (center of mass) of 3D objects from point clouds with subpixel accuracy. Works with concave shapes, cavities, and noisy data.

## Features

- 🎯 **Subpixel accuracy** - Error < 0.01% on test shapes
- ⚡ **High performance** - 50,000 points in 0.05 seconds
- 📦 **Multi-format support** - PLY, STL, OBJ, XYZ, PCD, LAS, NPY
- 🛡️ **Noise robust** - Stable with up to 10% noise
- 🔧 **5 operation modes** - Balance accuracy vs speed
- 🚀 **Production ready** - Thoroughly tested

## Installation

```bash
pip install voxel-centroid
```

For full format support:
```bash
pip install voxel-centroid[full]
```

## Quick Start

```python
from voxel_centroid import VoxelCentroid, VoxelConfig
import numpy as np

# Load or generate point cloud
points = np.random.randn(10000, 3)

# Configure algorithm
config = VoxelConfig(resolution=150, mode='standard')

# Compute centroid
centroid = VoxelCentroid(config).fit(points)
print(f"Centroid: {centroid}")
```

## Operation Modes

| Mode | Accuracy | Speed | Use Case |
|------|----------|-------|----------|
| `standard` | 0.7% | 0.08s | General purpose |
| `subpixel` | **0.01%** | 0.31s | Medical, aerospace |
| `adaptive` | 0.7% | 0.14s | Non-uniform data |
| `ensemble` | 0.3% | 0.50s | Critical calculations |
| `iterative` | 0.7% | 1.92s | Multi-component objects |

## Supported Formats

| Format | Extension | Requires |
|--------|-----------|----------|
| NumPy | .npy, .npz | None |
| Text | .xyz, .txt, .csv | None |
| PLY/STL/OBJ | .ply, .stl, .obj | trimesh or open3d |
| PCD | .pcd | open3d |
| LiDAR | .las, .laz | laspy |

## Advanced Usage

### Loading External Data

```python
from voxel_centroid import DataLoader

points = DataLoader.load_from_file("model.ply")
points = DataLoader.load_from_url("https://example.com/cloud.xyz")
```

### High-Precision Mode

```python
config = VoxelConfig(
    resolution=150,
    mode='subpixel',
    fill_holes=True,
    subpixel_sigma=0.5
)
centroid = VoxelCentroid(config).fit(points)
```

### Custom Configuration

```python
config = VoxelConfig(
    resolution=200,
    mode='ensemble',
    ensemble_resolutions=[150, 175, 200],
    fill_holes=True,
    verbose=True
)
```

## Performance Benchmarks

| Points | Standard | Subpixel | Adaptive |
|--------|----------|----------|----------|
| 1,000 | 0.033s | 0.180s | 0.085s |
| 10,000 | 0.059s | 0.154s | 0.083s |
| 50,000 | 0.056s | 0.171s | 0.102s |

## Accuracy Results

| Shape | Standard | Subpixel |
|-------|----------|----------|
| Cube | 0.68% | **0.01%** |
| Sphere | 0.34% | **0.01%** |
| Complex Drop | 0.42% | **0.01%** |

## Use Cases

- 🏭 **Industrial Quality Control** - Centroid verification for castings
- 🏥 **Medical Imaging** - Tumor center detection in CT/MRI
- 🗺️ **Geology** - LiDAR data analysis for mineral deposits
- 🤖 **Robotics** - Object grasping and manipulation
- 🖨️ **3D Printing** - Model positioning optimization

## Testing

Run the test suite:

```bash
pytest tests/
```

Run benchmark:

```bash
python -m voxel_centroid.benchmark
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Citation

If you use this library in academic work, please cite:

```bibtex
@software{voxel_centroid_2026,
  author = {SkyGliderus},
  title = {Voxel Centroid: High-Precision 3D Geometric Centroid Computation},
  year = {2026},
  url = {https://github.com/SkyGliderus/voxel-centroid}
}
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Contact

- Author: SkyGliderus
- Email: skygliderus@gmail.com
- GitHub: [@SkyGliderus](https://github.com/SkyGliderus)