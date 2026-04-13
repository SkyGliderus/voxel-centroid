"""Configuration for the voxel centroid algorithm"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class VoxelConfig:
    """
    Configuration for the voxel centroid algorithm
    
    Attributes:
        resolution: Voxel grid resolution (50-500, recommended 150)
        padding: Bounding box padding (fraction of size)
        fill_holes: Fill internal cavities (recommended True)
        dilate_iterations: Dilation iterations (0 = disabled)
        erode_iterations: Erosion iterations (0 = disabled)
        verbose: Enable detailed output
        mode: Operation mode (standard, subpixel, adaptive, ensemble, iterative)
        subpixel_sigma: Subpixel smoothing parameter
        adaptive_focus_ratio: Focus ratio for adaptive mode
        ensemble_resolutions: Resolution list for ensemble mode
        iterative_steps: Number of iterations for iterative mode
    """
    resolution: int = 150
    padding: float = 0.05
    fill_holes: bool = True
    dilate_iterations: int = 0
    erode_iterations: int = 0
    verbose: bool = False
    
    # Operation modes
    mode: str = 'standard'  # standard, subpixel, adaptive, ensemble, iterative
    subpixel_sigma: float = 0.5
    adaptive_focus_ratio: float = 0.5
    ensemble_resolutions: List[int] = field(default_factory=lambda: [125, 150, 175])
    iterative_steps: int = 3
    
    def __post_init__(self):
        if self.ensemble_resolutions is None:
            self.ensemble_resolutions = [125, 150, 175]
        self.validate()
    
    def validate(self) -> None:
        """Validate configuration parameters"""
        if self.resolution < 10 or self.resolution > 500:
            raise ValueError(f"resolution must be in [10, 500], got {self.resolution}")
        if self.padding < 0 or self.padding > 0.5:
            raise ValueError(f"padding must be in [0, 0.5], got {self.padding}")
        if self.mode not in ['standard', 'subpixel', 'adaptive', 'ensemble', 'iterative']:
            raise ValueError(f"Unknown mode: {self.mode}")
        if self.dilate_iterations < 0 or self.erode_iterations < 0:
            raise ValueError("dilate_iterations and erode_iterations cannot be negative")