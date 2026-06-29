# Camtasio

A Python API and CLI for working with Camtasia projects.

## Overview

Camtasio reads, modifies, and saves Camtasia project files (`.tscproj` JSON files inside `.cmproj` directories). It offers both high-level object-oriented interfaces and direct JSON manipulation.

### Key Features

- **📁 Project Management**: Read, modify, and save `.tscproj` files
- **🎬 Timeline Operations**: List tracks, analyze clips, manage markers
- **📐 Spatial Scaling**: Resize projects to different resolutions (`xyscale`)
- **⏱️ Temporal Scaling**: Change playback speed while preserving audio (`timescale`)
- **📁 Media Management**: List, clean, and replace media files (`media-ls`, `media-rm`, `media-replace`)
- **🎯 Batch Processing**: Apply operations to multiple projects (`batch`)
- **🔧 CLI Tools**: Command-line interface with readable terminal output
- **📊 Project Analysis**: Statistics, complexity scoring, and recommendations
- **✅ Version Compatibility**: Supports Camtasia 2018–2025+ (v1.0–v9.0)

## Installation

```bash
pip install camtasio
```

For development:
```bash
git clone https://github.com/twardoch/camtasio.git
cd camtasio
uv venv
uv sync
```

## Quick Start

### Command Line Interface

```bash
# Get project info
camtasio info my_project.tscproj --detailed

# Scale dimensions by 1.5x
camtasio xyscale my_project.tscproj 1.5 scaled_project.tscproj

# Double playback speed
camtasio timescale my_project.tscproj 2.0 fast_project.tscproj

# List and clean media
camtasio media_ls my_project.tscproj --detailed
camtasio media_rm my_project.tscproj  # Remove unused media

# Batch process projects
camtasio batch "projects/*.tscproj" info --detailed

# List timeline tracks and markers
camtasio track_ls my_project.tscproj --detailed
camtasio marker_ls my_project.tscproj

# Generate analysis report
camtasio analyze my_project.tscproj
```

### Python API

```python
from camtasio import ProjectLoader, ProjectSaver, PropertyTransformer, TransformConfig, TransformType
from camtasio.serialization import load_json_file

# Load a project
project_data = load_json_file("my_project.tscproj")

# Scale spatially
config = TransformConfig(TransformType.SPATIAL, factor=1.5)
transformer = PropertyTransformer(config)
scaled_data = transformer.transform_dict(project_data)

# Save result
saver = ProjectSaver()
saver.save_dict(scaled_data, "scaled_project.tscproj")

# Or use the high-level model
from camtasio import Project

loader = ProjectLoader()
project_data = loader.load("my_project.tscproj")
project = Project.from_dict(project_data)

scaled_project = project.scale_spatial(1.5)
scaled_data = scaled_project.to_dict()

saver.save_dict(scaled_data, "scaled_project.tscproj")
```

## Available Commands

| Command         | Description                  | Example                          |
|----------------|------------------------------|----------------------------------|
| `info`         | Show project info            | `camtasio info project.tscproj --detailed` |
| `validate`     | Check project integrity      | `camtasio validate project.tscproj` |
| `xyscale`      | Scale canvas dimensions      | `camtasio xyscale project.tscproj 1.5` |
| `timescale`    | Scale timeline duration      | `camtasio timescale project.tscproj 0.5` |
| `media_ls`     | List media bin contents      | `camtasio media_ls project.tscproj --detailed` |
| `media_rm`     | Remove unused media          | `camtasio media_rm project.tscproj` |
| `media_replace`| Replace media paths          | `camtasio media_replace project.tscproj old.mp4 new.mp4` |
| `track_ls`     | List timeline tracks         | `camtasio track_ls project.tscproj --detailed` |
| `marker_ls`    | List timeline markers        | `camtasio marker_ls project.tscproj` |
| `analyze`      | Generate analysis report     | `camtasio analyze project.tscproj` |
| `batch`        | Process multiple files       | `camtasio batch "*.tscproj" info` |
| `version`      | Show version info            | `camtasio version`               |

## Project Structure

A Camtasia project (`.cmproj`) is a directory containing:
- `project.tscproj` – Main JSON file
- `media/` – Imported media files
- macOS metadata files (bookmarks.plist, docPrefs)

The `.tscproj` file includes:
- Canvas size and frame rate
- Media bin with imported files
- Timeline with scenes, tracks, and clips
- Effects and annotations

## Advanced Usage

### Spatial Scaling

Resize projects while keeping relative positions:

```python
from camtasio import ProjectLoader, ProjectSaver, Project

loader = ProjectLoader()
project_data = loader.load("tutorial.tscproj")
project = Project.from_dict(project_data)

# Convert 1080p to 4K
current_width = project.canvas.width  # 1920
target_width = 3840
scale_factor = target_width / current_width

scaled_project = project.scale_spatial(scale_factor)
saver = ProjectSaver()
saver.save_dict(scaled_project.to_dict(), "tutorial_4k.tscproj")
```

### Timeline Analysis

```python
from camtasio.serialization import load_json_file

project_data = load_json_file("tutorial.tscproj")
timeline = project_data.get("timeline", {})
scene_track = timeline.get("sceneTrack", {})
scenes = scene_track.get("scenes", [])

for scene_idx, scene in enumerate(scenes):
    print(f"Scene {scene_idx}: {scene.get('csml', {}).get('duration', 0)} duration")
    
    tracks = scene.get("csml", {}).get("tracks", [])
    for track_idx, track in enumerate(tracks):
        track_id = track.get("trackId", "unknown")
        print(f"  Track {track_idx} (ID: {track_id})")
        
        for media_clip in track.get("medias", []):
            clip_name = media_clip.get("_name", "unnamed")
            start = media_clip.get("_start", 0)
            duration = media_clip.get("_duration", 0)
            print(f"    Clip: {clip_name} (start: {start}, duration: {duration})")
```

### Media Management

```python
from pathlib import Path
from camtasio.serialization import load_json_file

project_data = load_json_file("tutorial.tscproj")
source_bin = project_data.get("sourceBin", [])

print(f"Total media items: {len(source_bin)}")

missing_files = []
for item in source_bin:
    name = item.get("_name", "unnamed")
    media_type = item.get("_type", "unknown")
    
    if "src" in item:
        media_path = Path(item["src"])
        exists = media_path.exists()
        status = "✓" if exists else "✗"
        
        print(f"{status} {name} ({media_type}): {media_path}")
        
        if not exists:
            missing_files.append(str(media_path))
    else:
        print(f"? {name} ({media_type}): No source path")

if missing_files:
    print(f"\nWarning: {len(missing_files)} files not found!")
```

## Architecture

Camtasio supports two workflows:

- **High-Level API**: Object-oriented models (`Project`, `Timeline`, `Track`, `Clip`)
- **Low-Level API**: Direct JSON access for precise control
- **Domain Models**: Structured data representations
- **Operations Engine**: Recursive property traversal for transformations

## Compatibility

- ✅ Camtasia 2018–2025+ (v1.0–v9.0)
- ✅ Cross-platform: Windows, macOS, Linux
- ✅ Python 3.11+
- ✅ Future format versions

## Contributing

See [Contributing Guide](CONTRIBUTING.md).

## License

MIT – see [LICENSE](LICENSE).

## Acknowledgments

Tools used:
- 📦 `uv`, `hatch` – packaging
- 🔍 `ruff` – linting
- 🧪 `pytest` – testing
- 🎨 `rich` – CLI formatting
- 📝 `loguru` – logging