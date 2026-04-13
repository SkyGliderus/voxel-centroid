"""Tests for data loaders"""

import numpy as np
import tempfile
import os
import pytest
from voxel_centroid import DataLoader


def test_npy_loader():
    """Test loading from .npy file"""
    points = np.random.randn(100, 3)
    
    with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as f:
        np.save(f.name, points)
        temp_path = f.name
    
    try:
        loaded = DataLoader.load_from_file(temp_path)
        assert loaded.shape == (100, 3)
        assert np.allclose(loaded, points)
    finally:
        os.unlink(temp_path)


def test_txt_loader():
    """Test loading from .txt file"""
    points = np.random.randn(100, 3)
    
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        np.savetxt(f.name, points)
        temp_path = f.name
    
    try:
        loaded = DataLoader.load_from_file(temp_path)
        assert loaded.shape == (100, 3)
    finally:
        os.unlink(temp_path)


def test_format_detection():
    """Test format detection"""
    formats = DataLoader.list_supported_formats()
    assert isinstance(formats, list)
    assert len(formats) > 0
    assert '.npy' in formats
    assert '.xyz' in formats


def test_invalid_file():
    """Test handling of invalid files"""
    with pytest.raises(FileNotFoundError):
        DataLoader.load_from_file("nonexistent_file.xyz")