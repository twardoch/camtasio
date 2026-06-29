# Camtasia .tscproj Format Overview

## Purpose and Usage

The `.tscproj` file is the native project format for TechSmith Camtasia, a screen recording and video editing application. These files store all project data including:

- Media references (video, audio, images)
- Timeline structure and edits
- Visual effects and transitions
- Annotations and callouts
- Project settings and metadata

## File Format

`.tscproj` files are JSON (JavaScript Object Notation) documents, which means they are:
- Human-readable in any text editor
- Easily parsed and modified by scripts
- Suitable for version control systems
- Cross-platform compatible

## JSON Structure Overview

Top-level structure example:

```json
{
  "title": "Project Title",
  "author": "Author Name",
  "description": "Project Description",
  "width": 1920.0,
  "height": 1080.0,
  "videoFormatFrameRate": 60,
  "audioFormatSampleRate": 44100,
  "version": "9.0",
  "editRate": 705600000,
  "authoringClientName": {
    "name": "Camtasia",
    "platform": "Mac",
    "version": "2025.1.4"
  },
  "sourceBin": [...],
  "timeline": {...}
}
```

## Main Components

### 1. Root Properties
Global project settings:
- Canvas size (`width`, `height`)
- Frame rate and audio parameters
- Format version info
- Audio normalization preferences

### 2. Source Bin (`sourceBin`)
Array of imported media assets:
- Unique ID per item
- File paths relative to project location
- Metadata like dimensions, duration, track count
- Import timestamps

### 3. Timeline (`timeline`)
The edit timeline:
- Scene organization
- Multiple tracks/layers
- Clip timing and placement
- Applied effects and transitions

## File References

Media files use relative paths from the project file:

```json
"src": "./media/1752976336.728338/video.mp4"
```

Folder structure:
- `./media/` – Default media directory
- `{timestamp}/` – Session-specific folder
- `{filename}` – Media file name

## Coordinate System

Standard 2D layout:
- Top-left corner is (0,0)
- X grows right
- Y grows down
- All units in pixels

## Time Representation

Timing depends on version:
- **Version 4.0**: 60 ticks per second
- **Version 9.0**: High-resolution time based on `editRate`

Convert time to seconds:
```
seconds = timeValue / editRate
```

## Common Use Cases

### 1. Project Scaling
Resize canvas and adjust content:
- Change root `width` and `height`
- Scale `rect` values accordingly
- Update position and keyframe data

### 2. Media Management
Handle moved or missing assets:
- Replace outdated file paths
- Repair broken references
- Reconnect media when relocating projects

### 3. Batch Processing
Automate repetitive tasks:
- Apply uniform edits across multiple projects
- Generate templates or new projects via script

### 4. Analysis and Reporting
Extract useful data:
- Gather project stats
- Audit media usage
- Create edit decision lists (EDL)

## File Size Considerations

`.tscproj` files are small (typically KB to low MB) because they contain:
- References to external media
- Edit metadata
- Effect configurations

Actual video/audio content lives in the separate media folder.

## Best Practices

1. **Backup Strategy**
   - Store `.tscproj` with its media folder
   - Use relative paths for portability
   - Track `.tscproj` changes with version control

2. **Compatibility**
   - Check the `version` field before processing
   - Support both v4.0 and v9.0 formats
   - Retain unrecognized fields to avoid breaking future versions

3. **Validation**
   - Confirm referenced media files exist
   - Check that canvas dimensions match content
   - Validate time values against `editRate`

## Error Handling

Common issues:
- Missing media files
- Version mismatches
- Invalid JSON formatting
- Inconsistent canvas sizes or timing data

Always validate JSON syntax and verify media availability before running any automated process.