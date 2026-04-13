"""Package setup configuration"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="voxel-centroid",
    version="1.0.0",
    author="SkyGliderus",
    author_email="skygliderus@gmail.com",
    description="High-precision 3D geometric centroid computation through voxelization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SkyGliderus/voxel-centroid",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "full": [
            "open3d>=0.15.0",
            "trimesh>=3.9.0",
            "laspy>=2.0.0",
            "requests>=2.25.0",
            "plotly>=5.0.0",
            "pytest>=6.0.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
    },
    keywords="3d, centroid, voxel, point-cloud, geometry, medical-imaging, lidar",
    project_urls={
        "Documentation": "https://github.com/SkyGliderus/voxel-centroid",
        "Source": "https://github.com/SkyGliderus/voxel-centroid",
        "Tracker": "https://github.com/SkyGliderus/voxel-centroid/issues",
    },
)