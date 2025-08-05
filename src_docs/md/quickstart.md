# Quick Start Guide

Get up and running with Camtasio in minutes! This guide will walk you through the essential operations you can perform with Camtasio.

## Installation

```bash
# Install via pip
pip install camtasio

# Or using uv (recommended)
uv add camtasio
```

## Basic Project Operations

### Loading a Project

```python
from camtasio import Project

# Load from .cmproj directory
project = Project("my_video.cmproj")

# Or load from .tscproj file directly
project = Project("path/to/project.tscproj")

# Print basic project info
print(f"Project: {project.name}")
print(f"Duration: {project.duration}s")
print(f"Resolution: {project.width}x{project.height}")
```

### Scaling Projects

```python
# Scale to specific resolution
project.scale_to_resolution(1920, 1080)

# Scale by factor (2x larger)
project.scale_by_factor(2.0)

# Scale canvas size only (preserves media sizes)
project.scale_canvas(1280, 720)
```

### Timeline Manipulation

```python
# Access timeline
timeline = project.timeline

# Get all tracks
for track in timeline.tracks:
    print(f"Track: {track.name}, Media Count: {len(track.medias)}")

# Add a new video track
video_track = timeline.add_video_track("New Video Track")

# Add media to track
video_track.add_media("path/to/video.mp4", start_time=0.0, duration=10.0)
```

### Adding Annotations

```python
# Add a callout annotation
callout = project.add_callout(
    text="Important Note!",
    x=100, y=200,
    start_time=5.0,
    duration=3.0,
    font_size=24
)

# Add a highlight box
highlight = project.add_highlight_box(
    x=50, y=50, width=200, height=100,
    start_time=2.0,
    duration=5.0,
    color="#FF0000"
)
```

### Saving Projects

```python
# Save in place
project.save()

# Save to new location
project.save_as("new_project.cmproj")

# Save just the .tscproj file
project.save_tscproj("output.tscproj")
```

## Command Line Interface

Camtasio includes a powerful CLI for common operations:

### Project Information

```bash
# Get project details
camtasio info my_video.cmproj

# List all tracks and media
camtasio tracks my_video.cmproj
```

### Scaling Operations

```bash
# Scale to 1080p
camtasio scale my_video.cmproj --width 1920 --height 1080

# Scale by factor
camtasio scale my_video.cmproj --factor 1.5

# Batch scale multiple projects
camtasio batch-scale *.cmproj --width 1280 --height 720
```

### Media Operations

```bash
# List all media files used
camtasio media list my_video.cmproj

# Replace media file
camtasio media replace my_video.cmproj old_video.mp4 new_video.mp4

# Update media paths
camtasio media update-paths my_video.cmproj --base-path /new/media/folder
```

## Common Patterns

### Batch Processing

```python
from pathlib import Path
from camtasio import Project

# Process all .cmproj files in a directory
for project_path in Path("projects").glob("*.cmproj"):
    project = Project(project_path)
    
    # Scale to 1080p
    project.scale_to_resolution(1920, 1080)
    
    # Add watermark callout
    project.add_callout(
        text="© My Company",
        x=project.width - 200,
        y=project.height - 50,
        duration=project.duration,
        font_size=14,
        opacity=0.7
    )
    
    # Save with new name
    output_path = project_path.parent / f"processed_{project_path.name}"
    project.save_as(output_path)
```

### Media Validation

```python
def validate_project_media(project_path):
    project = Project(project_path)
    missing_files = []
    
    for track in project.timeline.tracks:
        for media in track.medias:
            if hasattr(media, 'src') and media.src:
                media_path = Path(media.src)
                if not media_path.exists():
                    missing_files.append(str(media_path))
    
    return missing_files

# Check for missing media
missing = validate_project_media("my_project.cmproj")
if missing:
    print("Missing media files:")
    for file in missing:
        print(f"  - {file}")
```

### Timeline Analysis

```python
def analyze_timeline(project):
    timeline = project.timeline
    
    stats = {
        'total_tracks': len(timeline.tracks),
        'video_tracks': 0,
        'audio_tracks': 0,
        'total_media': 0,
        'total_duration': project.duration
    }
    
    for track in timeline.tracks:
        if track.is_video_track():
            stats['video_tracks'] += 1
        elif track.is_audio_track():
            stats['audio_tracks'] += 1
        
        stats['total_media'] += len(track.medias)
    
    return stats

# Analyze project
project = Project("complex_project.cmproj")
stats = analyze_timeline(project)
print(f"Project has {stats['total_tracks']} tracks with {stats['total_media']} media items")
```

## Next Steps

Now that you've got the basics down, explore the detailed documentation:

- **[Installation Guide](installation.md)** - Advanced installation options and troubleshooting
- **[Project Basics](project-basics.md)** - Deep dive into project structure and core concepts  
- **[Timeline Operations](timeline-operations.md)** - Advanced timeline manipulation techniques
- **[Effects & Annotations](effects-annotations.md)** - Working with visual effects and callouts

## Common Issues

### Project Won't Load
- Ensure the `.cmproj` directory contains a `project.tscproj` file
- Check file permissions
- Verify the project isn't corrupted by opening it in Camtasia

### Scaling Issues
- Some very old project formats may not support all scaling operations
- Always backup projects before scaling
- Use `project.validate()` to check project integrity

### Performance Tips
- Use `project.load_lazy()` for large projects if you only need metadata
- Process projects in batches rather than loading all at once
- Consider using multiprocessing for batch operations on large project sets