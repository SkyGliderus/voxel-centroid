"""Basic usage example"""

import numpy as np
from voxel_centroid import VoxelCentroid, VoxelConfig


def main():
    # Generate sample data (cube with 5000 points)
    np.random.seed(42)
    points = np.random.uniform(-1, 1, (5000, 3))
    
    # Configure algorithm
    config = VoxelConfig(
        resolution=150,
        mode='standard',
        fill_holes=True,
        verbose=True
    )
    
    # Compute centroid
    algo = VoxelCentroid(config)
    centroid = algo.fit(points)
    
    # Display results
    print(f"\nResults:")
    print(f"  Centroid: [{centroid[0]:.6f}, {centroid[1]:.6f}, {centroid[2]:.6f}]")
    print(f"  Time: {algo.metrics['time_seconds']:.3f}s")
    print(f"  Fill ratio: {algo.metrics['fill_ratio']*100:.2f}%")


if __name__ == "__main__":
    main()