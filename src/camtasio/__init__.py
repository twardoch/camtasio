# this_file: src/camtasio/__init__.py
"""Camtasio - Python toolkit for programmatically manipulating Camtasia project files."""

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

# Import main components
from .models import (
    AudioMedia,
    Canvas,
    ImageMedia,
    Media,
    Project,
    ProjectMetadata,
    SourceBin,
    SourceItem,
    Timeline,
    Track,
    VideoMedia,
    create_media_from_dict,
)
from .serialization import ProjectLoader, ProjectSaver, detect_version
from .transforms import PropertyTransformer, TransformConfig, TransformType

# High-level operations (to be added from legacy camtasia)
# from .operations import scale_project, timescale_project

__all__ = [
    "AudioMedia",
    "Canvas",
    "ImageMedia",
    "Media",
    "Project",
    "ProjectLoader",
    "ProjectMetadata",
    "ProjectSaver",
    "PropertyTransformer",
    "SourceBin",
    "SourceItem",
    "Timeline",
    "Track",
    "TransformConfig",
    "TransformType",
    "VideoMedia",
    "__version__",
    "create_media_from_dict",
    "detect_version",
]
