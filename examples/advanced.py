"""Advanced usage with different modes and custom data"""

import numpy as np
from voxel_centroid import VoxelCentroid, VoxelConfig, DataLoader


def generate_complex_shape(n_points: int = 10000) -> np.ndarray:
    """Generate a complex asymmetric shape"""
    np.random.seed(42)
    
    # Main body
    n_body = n_points // 2
    phi = np.random.uniform(0, 2*np.pi, n_body)
    theta = np.random.uniform(0, np.pi/2, n_body)
    x_body = 0.8 * np.sin(theta) * np.cos(phi)
    y_body = 0.8 * np.sin(theta) * np.sin(phi)
    z_body = 0.8 * np.cos(theta) * 1.4
    
    # Skirt (irregular base)
    n_skirt = n_points // 4
    phi_skirt = np.random.uniform(0, 2*np.pi, n_skirt)
    r_skirt = np.random.uniform(0.9, 1.5, n_skirt)
    x_skirt = r_skirt * np.cos(phi_skirt)
    y_skirt = r_skirt * np.sin(phi_skirt)
    z_skirt = np.random.uniform(-1.2, -0.5, n_skirt)
    
    # Splashes
    n_splash = n_points - n_body - n_skirt
    x_splash = np.random.uniform(-1.5, 1.5, n_splash)
    y_splash = np.random.uniform(-1.5, 1.5, n_splash)
    z_splash = np.random.uniform(-1.5, -0.8, n_splash)
    
    points = np.vstack([
        np.column_stack([x_body, y_body, z_body]),
        np.column_stack([x_skirt, y_skirt, z_skirt]),
        np.column_stack([x_splash, y_splash, z_splash])
    ])
    
    return points + np.random.normal(0, 0.01, points.shape)


def compare_modes():
    """Compare different operation modes"""
    print("Generating complex shape...")
    points = generate_complex_shape(8000)
    
    modes = ['standard', 'subpixel']
    
    print("\n" + "="*60)
    print("COMPARING MODES")
    print("="*60)
    
    for mode in modes:
        config = VoxelConfig(
            resolution=150,
            mode=mode,
            fill_holes=True,
            verbose=True
        )
        
        algo = VoxelCentroid(config)
        centroid = algo.fit(points)
        
        print(f"\n{mode.upper()} results:")
        print(f"  Centroid: [{centroid[0]:.6f}, {centroid[1]:.6f}, {centroid[2]:.6f}]")
        print(f"  Time: {algo.metrics['time_seconds']:.3f}s")


def load_external_file():
    """Example of loading external file"""
    import os
    
    # Create sample file if none exists
    if not os.path.exists("sample.xyz"):
        points = np.random.randn(1000, 3)
        np.savetxt("sample.xyz", points)
        print("Created sample.xyz")
    
    # Load and process
    points = DataLoader.load_from_file("sample.xyz")
    print(f"Loaded {len(points)} points")
    
    config = VoxelConfig(resolution=100, mode='standard')
    centroid = VoxelCentroid(config).fit(points)
    print(f"Centroid: {centroid}")


if __name__ == "__main__":
    compare_modes()
    # load_external_file()