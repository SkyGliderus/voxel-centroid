"""Accuracy tests for voxel centroid algorithm"""

import numpy as np
import pytest
from voxel_centroid import VoxelCentroid, VoxelConfig


def generate_cube(n_points=5000, side=2.0):
    """Generate cube with known center at origin"""
    np.random.seed(42)
    return np.random.uniform(-side/2, side/2, (n_points, 3))


def generate_sphere(n_points=5000):
    """Generate sphere with known center at origin"""
    np.random.seed(42)
    phi = np.random.uniform(0, 2*np.pi, n_points)
    theta = np.random.uniform(0, np.pi, n_points)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.column_stack([x, y, z])


def test_cube_accuracy():
    """Test centroid accuracy on cube"""
    points = generate_cube(5000)
    true_centroid = np.array([0, 0, 0])
    
    config = VoxelConfig(resolution=150, mode='standard')
    centroid = VoxelCentroid(config).fit(points)
    error = np.linalg.norm(centroid - true_centroid)
    
    # Error should be less than 1% of half-size
    assert error < 0.02, f"Error too large: {error}"


def test_sphere_accuracy():
    """Test centroid accuracy on sphere"""
    points = generate_sphere(5000)
    true_centroid = np.array([0, 0, 0])
    
    config = VoxelConfig(resolution=150, mode='standard')
    centroid = VoxelCentroid(config).fit(points)
    error = np.linalg.norm(centroid - true_centroid)
    
    # Error should be less than 0.5% of radius
    assert error < 0.01, f"Error too large: {error}"


def test_subpixel_accuracy():
    """Test subpixel mode accuracy"""
    points = generate_cube(8000)
    true_centroid = np.array([0, 0, 0])
    
    config = VoxelConfig(resolution=120, mode='subpixel')
    centroid = VoxelCentroid(config).fit(points)
    error = np.linalg.norm(centroid - true_centroid)
    
    # Subpixel should be extremely accurate
    assert error < 0.001, f"Subpixel error too large: {error}"


def test_noise_robustness():
    """Test robustness to noise"""
    points = generate_sphere(5000)
    true_centroid = np.array([0, 0, 0])
    
    # Add noise
    noisy_points = points + np.random.normal(0, 0.05, points.shape)
    
    config = VoxelConfig(resolution=150, mode='standard')
    centroid = VoxelCentroid(config).fit(noisy_points)
    error = np.linalg.norm(centroid - true_centroid)
    
    # Should still be accurate despite noise
    assert error < 0.03, f"Noise robustness failed: {error}"