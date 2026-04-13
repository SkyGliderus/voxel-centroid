"""
Voxel Centroid - High-precision 3D geometric centroid computation

This library uses voxelization to compute the center of mass for complex 3D shapes,
including concave objects, with subpixel accuracy.

Example:
    from voxel_centroid import VoxelCentroid, VoxelConfig
    
    config = VoxelConfig(resolution=150, mode='standard')
    centroid = VoxelCentroid(config).fit(points)
    print(f"Centroid: {centroid}")
"""

from .core import VoxelCentroid
from .config import VoxelConfig
from .loaders import DataLoader

__version__ = "1.0.0"
__author__ = "SkyGliderus"
__email__ = "skygliderus@gmail.com"
__all__ = ["VoxelCentroid", "VoxelConfig", "DataLoader"]