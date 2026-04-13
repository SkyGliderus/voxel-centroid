"""Core voxel centroid algorithm"""

import numpy as np
import time
import warnings
from scipy.ndimage import binary_fill_holes, binary_dilation, binary_erosion
from scipy.ndimage import distance_transform_edt, center_of_mass
from typing import Tuple, Dict, Any, Optional, List

from .config import VoxelConfig


class VoxelCentroid:
    """
    Voxel-based centroid computation for 3D objects
    
    This algorithm voxelizes point clouds and computes the geometric centroid
    with subpixel accuracy. Supports multiple operation modes for different
    accuracy/speed trade-offs.
    
    Example:
        config = VoxelConfig(resolution=150, mode='standard')
        centroid = VoxelCentroid(config).fit(points)
    """
    
    def __init__(self, config: Optional[VoxelConfig] = None):
        """
        Initialize the algorithm
        
        Args:
            config: Configuration object (uses defaults if None)
        """
        self.config = config or VoxelConfig()
        self.config.validate()
        
        self.voxels: Optional[np.ndarray] = None
        self.bounds: Optional[Tuple[np.ndarray, np.ndarray]] = None
        self.metrics: Dict[str, Any] = {}
        self._centroid: Optional[np.ndarray] = None
        self._intermediate_centroids: List[np.ndarray] = []
    
    def _compute_bounds(self, points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute bounding box with padding"""
        min_bound = points.min(axis=0)
        max_bound = points.max(axis=0)
        padding = self.config.padding * (max_bound - min_bound)
        return min_bound - padding, max_bound + padding
    
    def _points_to_voxels(self, points: np.ndarray) -> np.ndarray:
        """Convert point cloud to voxel grid"""
        min_bound, max_bound = self.bounds
        norm_points = (points - min_bound) / (max_bound - min_bound)
        indices = (norm_points * (self.config.resolution - 1)).astype(int)
        indices = np.clip(indices, 0, self.config.resolution - 1)
        
        voxels = np.zeros((self.config.resolution,) * 3, dtype=bool)
        voxels[indices[:, 0], indices[:, 1], indices[:, 2]] = True
        return voxels
    
    def _process_voxels(self, voxels: np.ndarray) -> np.ndarray:
        """Post-process voxels (fill holes, dilate, erode)"""
        result = voxels.copy()
        
        if self.config.fill_holes:
            result = binary_fill_holes(result)
        
        if self.config.dilate_iterations > 0:
            structure = np.ones((3, 3, 3))
            for _ in range(self.config.dilate_iterations):
                result = binary_dilation(result, structure)
        
        if self.config.erode_iterations > 0:
            structure = np.ones((3, 3, 3))
            for _ in range(self.config.erode_iterations):
                result = binary_erosion(result, structure)
        
        return result
    
    def _centroid_standard(self, voxels: np.ndarray) -> np.ndarray:
        """Standard centroid (fast)"""
        min_bound, max_bound = self.bounds
        grid = np.indices((self.config.resolution,) * 3).reshape(3, -1).T
        occupied = voxels.flatten()
        
        if not np.any(occupied):
            return (min_bound + max_bound) / 2
        
        centers = min_bound + (grid[occupied] + 0.5) / self.config.resolution * (max_bound - min_bound)
        return np.mean(centers, axis=0)
    
    def _centroid_subpixel(self, voxels: np.ndarray) -> np.ndarray:
        """Subpixel centroid (high accuracy)"""
        min_bound, max_bound = self.bounds
        
        # Weight boundary voxels
        distances = distance_transform_edt(voxels)
        weights = np.exp(-distances / self.config.subpixel_sigma)
        
        grid = np.indices((self.config.resolution,) * 3).reshape(3, -1).T
        centers = min_bound + (grid + 0.5) / self.config.resolution * (max_bound - min_bound)
        weights_flat = weights.flatten()
        
        weighted_centroid = np.sum(centers * weights_flat[:, np.newaxis], axis=0) / np.sum(weights_flat)
        
        return weighted_centroid
    
    def _centroid_adaptive(self, points: np.ndarray) -> np.ndarray:
        """Adaptive centroid with focus on region of interest"""
        # First pass
        centroid_coarse = self._centroid_standard(self.voxels)
        
        # Focus on region around centroid
        bbox_half = self.config.adaptive_focus_ratio * (self.bounds[1] - self.bounds[0]) / 2
        mask = np.all(np.abs(points - centroid_coarse) < bbox_half, axis=1)
        points_focused = points[mask]
        
        if len(points_focused) < 100:
            return centroid_coarse
        
        # Second pass on focused region
        bounds_focused = self._compute_bounds(points_focused)
        self.bounds = bounds_focused
        voxels_focused = self._points_to_voxels(points_focused)
        voxels_focused = self._process_voxels(voxels_focused)
        
        return self._centroid_standard(voxels_focused)
    
    def _centroid_ensemble(self, points: np.ndarray) -> np.ndarray:
        """Ensemble centroid (average of multiple resolutions)"""
        centroids = []
        weights = []
        
        for res in self.config.ensemble_resolutions:
            temp_config = VoxelConfig(
                resolution=res,
                fill_holes=self.config.fill_holes,
                mode='standard'
            )
            temp_algo = VoxelCentroid(temp_config)
            centroid = temp_algo.fit(points)
            centroids.append(centroid)
            weights.append(res)
        
        weights = np.array(weights) / np.sum(weights)
        return np.average(centroids, axis=0, weights=weights)
    
    def _centroid_iterative(self, points: np.ndarray) -> np.ndarray:
        """Iterative centroid with progressive focusing"""
        centroid = np.mean(points, axis=0)
        
        for i in range(self.config.iterative_steps):
            scale = 2.0 ** (1 - i)
            bbox_half = scale * (points.max(axis=0) - points.min(axis=0)) / 2
            
            mask = np.all(np.abs(points - centroid) < bbox_half, axis=1)
            points_focused = points[mask]
            
            if len(points_focused) < 100:
                break
            
            resolution = min(300, self.config.resolution * (i + 1))
            temp_config = VoxelConfig(resolution=resolution, fill_holes=self.config.fill_holes)
            centroid = VoxelCentroid(temp_config).fit(points_focused)
            self._intermediate_centroids.append(centroid.copy())
        
        return centroid
    
    def fit(self, points: np.ndarray) -> np.ndarray:
        """
        Compute centroid from point cloud
        
        Args:
            points: Point cloud array (N, 3)
            
        Returns:
            Centroid coordinates (3,)
        """
        start_time = time.time()
        
        if len(points) < 4:
            raise ValueError(f"Insufficient points: {len(points)} (minimum 4)")
        
        self.bounds = self._compute_bounds(points)
        
        if self.config.verbose:
            print(f"[VoxelCentroid] Mode: {self.config.mode}")
            print(f"[VoxelCentroid] Resolution: {self.config.resolution}³")
            print(f"[VoxelCentroid] Points: {len(points)}")
        
        self.voxels = self._points_to_voxels(points)
        self.voxels = self._process_voxels(self.voxels)
        
        # Select method based on mode
        if self.config.mode == 'standard':
            self._centroid = self._centroid_standard(self.voxels)
        elif self.config.mode == 'subpixel':
            self._centroid = self._centroid_subpixel(self.voxels)
        elif self.config.mode == 'adaptive':
            self._centroid = self._centroid_adaptive(points)
        elif self.config.mode == 'ensemble':
            self._centroid = self._centroid_ensemble(points)
        elif self.config.mode == 'iterative':
            self._centroid = self._centroid_iterative(points)
        else:
            self._centroid = self._centroid_standard(self.voxels)
        
        total_cells = self.config.resolution ** 3
        self.metrics = {
            'resolution': self.config.resolution,
            'mode': self.config.mode,
            'total_voxels': int(np.sum(self.voxels)),
            'total_cells': total_cells,
            'fill_ratio': np.sum(self.voxels) / total_cells,
            'time_seconds': time.time() - start_time,
            'n_points': len(points)
        }
        
        if self.config.verbose:
            print(f"[VoxelCentroid] Voxels: {self.metrics['total_voxels']}/{total_cells} ({self.metrics['fill_ratio']*100:.2f}%)")
            print(f"[VoxelCentroid] Time: {self.metrics['time_seconds']:.3f}s")
            print(f"[VoxelCentroid] Centroid: [{self._centroid[0]:.6f}, {self._centroid[1]:.6f}, {self._centroid[2]:.6f}]")
        
        return self._centroid.copy()
    
    def get_centroid(self) -> np.ndarray:
        """Return computed centroid"""
        if self._centroid is None:
            raise RuntimeError("Call fit() first")
        return self._centroid.copy()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Return computation metrics"""
        if not self.metrics:
            raise RuntimeError("Call fit() first")
        return self.metrics.copy()
    
    def get_voxel_centers(self) -> np.ndarray:
        """Return coordinates of all filled voxel centers"""
        if self.voxels is None or self.bounds is None:
            raise RuntimeError("Call fit() first")
        
        min_bound, max_bound = self.bounds
        grid = np.indices((self.config.resolution,) * 3).reshape(3, -1).T
        occupied = self.voxels.flatten()
        
        return min_bound + (grid[occupied] + 0.5) / self.config.resolution * (max_bound - min_bound)