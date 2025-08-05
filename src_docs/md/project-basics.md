# Project Basics

Understanding the fundamental concepts and structure of Camtasia projects and how to work with them using Camtasio.

## Project Structure Overview

### Camtasia Project Files

Camtasia projects consist of two main components:

1. **`.cmproj` Directory** - Contains all project assets and metadata
2. **`project.tscproj`** - JSON file with timeline, media, and configuration data

```
my_video.cmproj/
├── project.tscproj        # Main project file (JSON)
├── media/                 # Media assets directory
│   ├── video1.mp4
│   ├── audio1.wav
│   └── image1.png
├── bookmarks.plist        # Bookmark data
└── docPrefs              # Document preferences
```

### Project Object Model

Camtasio uses a hierarchical object model to represent projects:

```python
Project
├── Timeline              # Main timeline container
│   ├── Track[]          # Array of tracks (video/audio)
│   │   ├── Media[]      # Media items on each track
│   │   └── Properties   # Track-specific settings
│   └── Groups[]         # Track groupings
├── SourceMedias[]       # Media bin (all available media)
├── Canvas               # Canvas settings (resolution, etc.)
└── Metadata            # Project metadata and settings
```

## Creating and Loading Projects

### Loading Existing Projects

```python
from camtasio import Project

# Load from .cmproj directory
project = Project("path/to/project.cmproj")

# Load from .tscproj file directly  
project = Project("path/to/project.tscproj")

# Load with validation
project = Project("project.cmproj", validate=True)

# Load with custom encoding
project = Project("project.cmproj", encoding="utf-8")
```

### Creating New Projects

```python
from camtasio import Project
from camtasio.models import Canvas

# Create new project with default settings
project = Project.create_new(
    name="My New Project",
    width=1920,
    height=1080,
    frame_rate=30
)

# Create with custom canvas settings
canvas = Canvas(
    width=1280,
    height=720,
    frame_rate=25,
    background_color="#000000"
)
project = Project.create_new("HD Project", canvas=canvas)

# Save new project
project.save_as("new_project.cmproj")
```

## Project Properties

### Basic Information

```python
# Project metadata
print(f"Name: {project.name}")
print(f"Duration: {project.duration} seconds")
print(f"Frame Rate: {project.frame_rate} fps")

# Canvas dimensions
print(f"Resolution: {project.width}x{project.height}")
print(f"Aspect Ratio: {project.aspect_ratio}")

# File information
print(f"Project Path: {project.path}")
print(f"Last Modified: {project.last_modified}")
print(f"File Size: {project.file_size} bytes")
```

### Canvas Properties

```python
# Access canvas settings
canvas = project.canvas

# Canvas dimensions
print(f"Canvas Size: {canvas.width}x{canvas.height}")
print(f"Background: {canvas.background_color}")

# Modify canvas
canvas.width = 1920
canvas.height = 1080
canvas.background_color = "#FFFFFF"

# Apply changes
project.update_canvas(canvas)
```

### Project Settings

```python
# Audio settings
audio_settings = project.audio_settings
print(f"Sample Rate: {audio_settings.sample_rate}")
print(f"Bit Depth: {audio_settings.bit_depth}")

# Video settings  
video_settings = project.video_settings
print(f"Codec: {video_settings.codec}")
print(f"Quality: {video_settings.quality}")

# Modify settings
project.set_audio_sample_rate(48000)
project.set_video_quality("High")
```

## Working with the Timeline

### Timeline Structure

```python
# Access the timeline
timeline = project.timeline

# Timeline properties
print(f"Timeline Duration: {timeline.duration}")
print(f"Track Count: {len(timeline.tracks)}")
print(f"Total Media Items: {timeline.total_media_count}")

# Timeline bounds
print(f"Start Time: {timeline.start_time}")
print(f"End Time: {timeline.end_time}")
```

### Track Management

```python
# Get all tracks
for i, track in enumerate(timeline.tracks):
    print(f"Track {i}: {track.name} ({track.type})")
    print(f"  Media Count: {len(track.medias)}")
    print(f"  Enabled: {track.enabled}")

# Find specific tracks
video_tracks = timeline.get_video_tracks()
audio_tracks = timeline.get_audio_tracks()

# Get track by name
main_video = timeline.get_track_by_name("Main Video")

# Track properties
for track in video_tracks:
    print(f"Video Track: {track.name}")
    print(f"  Resolution: {track.width}x{track.height}")
    print(f"  Blend Mode: {track.blend_mode}")
    print(f"  Opacity: {track.opacity}")
```

## Media Management

### Source Media (Media Bin)

```python
# Access all available media
source_medias = project.source_medias

for media in source_medias:
    print(f"Media: {media.name}")
    print(f"  Type: {media.type}")
    print(f"  Duration: {media.duration}")
    print(f"  Path: {media.src}")
    print(f"  Used: {media.is_used_in_timeline()}")
```

### Adding Media to Project

```python
# Add media to the media bin
video_media = project.add_source_media(
    path="video.mp4",
    name="Main Video"
)

audio_media = project.add_source_media(
    path="audio.wav", 
    name="Background Music"
)

# Add media with metadata
image_media = project.add_source_media(
    path="logo.png",
    name="Company Logo",
    metadata={
        "description": "Company logo for watermark",
        "tags": ["logo", "branding"]
    }
)
```

### Timeline Media Items

```python
# Get all media on timeline
timeline_medias = timeline.get_all_media()

for media in timeline_medias:
    print(f"Media: {media.name}")
    print(f"  Track: {media.track.name}")
    print(f"  Start: {media.start} seconds")
    print(f"  Duration: {media.duration} seconds")
    print(f"  Position: ({media.x}, {media.y})")
    print(f"  Size: {media.width}x{media.height}")
```

## Project Validation

### Automatic Validation

```python
# Validate project structure and integrity
validation_result = project.validate()

if validation_result.is_valid:
    print("Project is valid!")
else:
    print("Project validation failed:")
    for error in validation_result.errors:
        print(f"  - {error.message} (severity: {error.severity})")
```

### Manual Validation

```python
# Check for missing media files
missing_media = project.find_missing_media()
if missing_media:
    print("Missing media files:")
    for media_path in missing_media:
        print(f"  - {media_path}")

# Check timeline integrity
timeline_issues = project.validate_timeline()
for issue in timeline_issues:
    print(f"Timeline issue: {issue}")

# Validate canvas settings
canvas_valid = project.validate_canvas()
print(f"Canvas valid: {canvas_valid}")
```

## Project Serialization

### Saving Projects

```python
# Save in place (overwrites original)
project.save()

# Save to new location
project.save_as("backup_project.cmproj")

# Save only the .tscproj file
project.save_tscproj("project_data.tscproj")

# Save with compression
project.save(compress=True)

# Save with backup
project.save(create_backup=True)
```

### Export Options

```python
# Export project data to JSON
json_data = project.to_json(indent=2)
with open("project_export.json", "w") as f:
    f.write(json_data)

# Export to dictionary
project_dict = project.to_dict()

# Export timeline only
timeline_data = project.timeline.to_dict()

# Export with media references
project_with_media = project.to_dict(include_media_paths=True)
```

## Project Metadata

### Built-in Metadata

```python
# Access project metadata
metadata = project.metadata

print(f"Created: {metadata.creation_date}")
print(f"Modified: {metadata.modification_date}")
print(f"Version: {metadata.camtasia_version}")
print(f"Author: {metadata.author}")
print(f"Comments: {metadata.comments}")
```

### Custom Metadata

```python
# Add custom metadata
project.set_metadata("project_id", "PRJ-2024-001")
project.set_metadata("client", "Example Corp")
project.set_metadata("status", "in_progress")

# Retrieve custom metadata
project_id = project.get_metadata("project_id")
client = project.get_metadata("client", default="Unknown")

# List all custom metadata
custom_meta = project.list_custom_metadata()
for key, value in custom_meta.items():
    print(f"{key}: {value}")
```

## Working with Project Templates

### Creating Templates

```python
# Create a template from existing project
template = project.create_template(
    name="Corporate Template",
    description="Standard corporate video template",
    include_media=False  # Don't include media files
)

# Save template
template.save("templates/corporate.cmproj")
```

### Using Templates

```python
# Create project from template
new_project = Project.from_template(
    template_path="templates/corporate.cmproj",
    name="New Corporate Video"
)

# Apply template to existing project
project.apply_template("templates/outro.cmproj", 
                      position="end")
```

## Project Comparison

### Comparing Projects

```python
from camtasio.comparison import ProjectComparator

# Compare two projects
comparator = ProjectComparator()
diff = comparator.compare(project1, project2)

print(f"Projects are {'identical' if diff.is_identical else 'different'}")

# Show differences
for difference in diff.differences:
    print(f"Difference: {difference.type}")
    print(f"  Location: {difference.path}")
    print(f"  Project 1: {difference.value1}")
    print(f"  Project 2: {difference.value2}")
```

### Change Detection

```python
# Create a snapshot for comparison
snapshot = project.create_snapshot()

# Make changes to project
project.scale_to_resolution(1920, 1080)
project.timeline.add_track("New Track")

# Compare with snapshot
changes = project.compare_with_snapshot(snapshot)
for change in changes:
    print(f"Change: {change.description}")
```

## Error Handling

### Common Exceptions

```python
from camtasio.exceptions import (
    ProjectLoadError,
    ProjectValidationError,
    MediaNotFoundError,
    TimelineError
)

try:
    project = Project("invalid_project.cmproj")
except ProjectLoadError as e:
    print(f"Failed to load project: {e}")
except ProjectValidationError as e:
    print(f"Project validation failed: {e}")

try:
    project.timeline.add_media("nonexistent.mp4")
except MediaNotFoundError as e:
    print(f"Media file not found: {e}")
```

### Safe Operations

```python
# Safe project loading with fallback
def safe_load_project(path, fallback_path=None):
    try:
        return Project(path)
    except ProjectLoadError:
        if fallback_path:
            return Project(fallback_path)
        return None

# Safe property access
duration = getattr(project, 'duration', 0.0)
width = project.get_property('width', default=1920)
```

## Performance Considerations

### Lazy Loading

```python
# Load project metadata only (faster for large projects)
project = Project.load_metadata_only("large_project.cmproj")

# Load full project when needed
project.load_full_data()

# Check if fully loaded
if project.is_fully_loaded:
    print("Project data fully loaded")
```

### Memory Management

```python
# Free unused media references
project.cleanup_unused_media()

# Optimize project structure
project.optimize()

# Clear caches
project.clear_caches()
```

## Next Steps

Now that you understand project basics, explore more advanced topics:

- **[Timeline Operations](timeline-operations.md)** - Advanced timeline manipulation
- **[Media Management](media-management.md)** - Working with video, audio, and images
- **[Effects & Annotations](effects-annotations.md)** - Adding visual elements
- **[Scaling Operations](scaling-operations.md)** - Resolution and size management