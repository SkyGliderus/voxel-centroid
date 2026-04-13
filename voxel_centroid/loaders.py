"""Universal 3D data loaders for various formats"""

import numpy as np
import warnings
import os
from pathlib import Path
from typing import Union, List, Optional, Tuple

# Optional imports with fallbacks
try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ImportError:
    OPEN3D_AVAILABLE = False

try:
    import laspy
    LASP_AVAILABLE = True
except ImportError:
    LASP_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import trimesh
    TRIMESH_AVAILABLE = True
except ImportError:
    TRIMESH_AVAILABLE = False


class DataLoader:
    """Universal 3D data loader supporting multiple formats"""
    
    @staticmethod
    def load_from_file(filepath: Union[str, Path], **kwargs) -> np.ndarray:
        """
        Load points from file
        
        Supported formats:
        - .npy, .npz - NumPy arrays
        - .xyz, .txt, .csv, .asc - Text coordinates
        - .ply, .stl, .obj, .off - 3D models
        - .pcd - Point Cloud Library
        - .las, .laz - LiDAR data
        
        Args:
            filepath: Path to the file
            **kwargs: Additional arguments (delimiter, etc.)
            
        Returns:
            Array of points (N, 3)
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        ext = filepath.suffix.lower()
        
        # NumPy formats
        if ext == '.npy':
            data = np.load(filepath)
            return DataLoader._ensure_points_format(data)
        
        elif ext == '.npz':
            data = np.load(filepath)
            for key in ['points', 'vertices', 'data', 'arr_0']:
                if key in data:
                    return DataLoader._ensure_points_format(data[key])
            raise ValueError(f"NPZ file contains no point array. Keys: {list(data.keys())}")
        
        # Text formats
        elif ext in ['.xyz', '.txt', '.csv', '.asc']:
            delimiter = kwargs.get('delimiter', None)
            if ext == '.csv':
                delimiter = delimiter or ','
            data = np.loadtxt(filepath, delimiter=delimiter)
            return DataLoader._ensure_points_format(data)
        
        # 3D model formats
        elif ext in ['.ply', '.stl', '.obj', '.off', '.gltf', '.glb']:
            if TRIMESH_AVAILABLE:
                mesh = trimesh.load(str(filepath))
                if hasattr(mesh, 'vertices'):
                    points = mesh.vertices
                elif hasattr(mesh, 'points'):
                    points = mesh.points
                else:
                    points = mesh.sample(10000)
                return DataLoader._ensure_points_format(points)
            elif OPEN3D_AVAILABLE:
                mesh = o3d.io.read_triangle_mesh(str(filepath))
                points = np.asarray(mesh.vertices)
                return DataLoader._ensure_points_format(points)
            else:
                raise ImportError("Install trimesh or open3d: pip install trimesh")
        
        # PCD format
        elif ext == '.pcd':
            if OPEN3D_AVAILABLE:
                pcd = o3d.io.read_point_cloud(str(filepath))
                points = np.asarray(pcd.points)
                return DataLoader._ensure_points_format(points)
            else:
                raise ImportError("Install open3d: pip install open3d")
        
        # LAS/LAZ format (LiDAR)
        elif ext in ['.las', '.laz']:
            if LASP_AVAILABLE:
                las = laspy.read(str(filepath))
                points = np.vstack([las.x, las.y, las.z]).T
                return DataLoader._ensure_points_format(points)
            else:
                raise ImportError("Install laspy: pip install laspy")
        
        else:
            raise ValueError(f"Unsupported format: {ext}")
    
    @staticmethod
    def load_from_url(url: str, **kwargs) -> np.ndarray:
        """
        Load points from URL
        
        Args:
            url: URL to the file
            **kwargs: Additional arguments
            
        Returns:
            Array of points (N, 3)
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("Install requests: pip install requests")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        import tempfile
        suffix = kwargs.get('suffix', '.npy')
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        
        try:
            points = DataLoader.load_from_file(tmp_path, **kwargs)
        finally:
            os.unlink(tmp_path)
        
        return points
    
    @staticmethod
    def _ensure_points_format(data: np.ndarray) -> np.ndarray:
        """Convert data to (N, 3) format"""
        data = np.asarray(data)
        
        if data.ndim == 1:
            n_points = len(data) // 3
            data = data.reshape(n_points, 3)
        elif data.ndim == 2 and data.shape[1] > 3:
            data = data[:, :3]
        elif data.ndim != 2 or data.shape[1] != 3:
            raise ValueError(f"Invalid data shape: {data.shape}. Expected (N, 3)")
        
        # Remove NaN and Inf
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            warnings.warn("Data contains NaN or Inf. Cleaning...")
            data = data[~np.any(np.isnan(data) | np.isinf(data), axis=1)]
        
        return data.astype(np.float64)
    
    @staticmethod
    def list_supported_formats() -> List[str]:
        """Return list of supported file formats"""
        formats = ['.npy', '.npz', '.xyz', '.txt', '.csv', '.ply', '.stl', '.obj', '.off', '.pcd']
        if LASP_AVAILABLE:
            formats.extend(['.las', '.laz'])
        if TRIMESH_AVAILABLE:
            formats.extend(['.gltf', '.glb'])
        return formats