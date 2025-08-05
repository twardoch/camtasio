# Media Management

Comprehensive guide to working with video, audio, and image assets in Camtasia projects using Camtasio.

## Media Types and Structure

### Understanding Media Categories

Camtasia supports several types of media, each with specific properties and handling requirements:

```python
from camtasio import Project
from camtasio.models.media import VideoMedia, AudioMedia, ImageMedia

project = Project("example.cmproj")

# Categorize media by type
for media in project.source_medias:
    if isinstance(media, VideoMedia):
        print(f"Video: {media.name} ({media.width}x{media.height}, {media.duration}s)")
    elif isinstance(media, AudioMedia):
        print(f"Audio: {media.name} ({media.sample_rate}Hz, {media.duration}s)")
    elif isinstance(media, ImageMedia):
        print(f"Image: {media.name} ({media.width}x{media.height})")
```

### Media Properties

```python
# Common properties for all media types
media = project.source_medias[0]
print(f"Name: {media.name}")
print(f"Source Path: {media.src}")
print(f"Duration: {media.duration}")
print(f"File Size: {media.file_size}")
print(f"Created: {media.creation_date}")
print(f"Modified: {media.modification_date}")

# Type-specific properties
if hasattr(media, 'frame_rate'):
    print(f"Frame Rate: {media.frame_rate}")
if hasattr(media, 'sample_rate'):
    print(f"Sample Rate: {media.sample_rate}")
if hasattr(media, 'bit_depth'):
    print(f"Bit Depth: {media.bit_depth}")
```

## Video Media Management

### Video Properties and Metadata

```python
# Working with video media
video_media = project.get_video_media()[0]

# Basic video properties
print(f"Resolution: {video_media.width}x{video_media.height}")
print(f"Duration: {video_media.duration} seconds")
print(f"Frame Rate: {video_media.frame_rate} fps")
print(f"Aspect Ratio: {video_media.aspect_ratio}")

# Advanced video properties
print(f"Codec: {video_media.codec}")
print(f"Bitrate: {video_media.bitrate}")
print(f"Color Space: {video_media.color_space}")
print(f"Has Alpha: {video_media.has_alpha}")
```

### Video Operations

```python
# Resize video media
video_media.resize(
    width=1280,
    height=720,
    maintain_aspect=True
)

# Apply video transformations
video_media.rotate(90)  # Rotate 90 degrees
video_media.flip_horizontal()
video_media.flip_vertical()

# Crop video
video_media.crop(
    left=50,
    top=100,
    width=1200,
    height=800
)

# Adjust video timing
video_media.trim(
    start_offset=2.0,
    end_offset=1.5
)
```

### Video Quality and Compression

```python
# Analyze video quality
quality_info = video_media.analyze_quality()
print(f"Average bitrate: {quality_info.avg_bitrate}")
print(f"Peak bitrate: {quality_info.peak_bitrate}")
print(f"Quality score: {quality_info.quality_score}")

# Optimize video for web
video_media.optimize_for_web(
    target_bitrate=2000,  # 2 Mbps
    max_resolution=(1920, 1080)
)

# Set video compression settings
video_media.set_compression(
    quality="high",
    codec="h264",
    profile="main"
)
```

## Audio Media Management

### Audio Properties

```python
# Working with audio media
audio_media = project.get_audio_media()[0]

# Audio specifications
print(f"Sample Rate: {audio_media.sample_rate} Hz")
print(f"Bit Depth: {audio_media.bit_depth} bits")
print(f"Channels: {audio_media.channels}")
print(f"Duration: {audio_media.duration} seconds")

# Audio quality metrics
print(f"Peak Level: {audio_media.peak_level} dB")
print(f"RMS Level: {audio_media.rms_level} dB")
print(f"Dynamic Range: {audio_media.dynamic_range} dB")
```

### Audio Processing

```python
# Normalize audio levels
audio_media.normalize(
    target_level=-12.0,  # dB
    preserve_dynamics=True
)

# Apply audio filters
audio_media.apply_high_pass_filter(frequency=80)  # Remove low frequency noise
audio_media.apply_low_pass_filter(frequency=15000)  # Remove high frequency noise

# Adjust audio timing
audio_media.fade_in(duration=1.0)
audio_media.fade_out(duration=2.0)

# Audio level adjustments
audio_media.set_volume(0.8)  # 80% volume
audio_media.apply_gain(gain_db=3.0)  # +3dB gain
```

### Audio Analysis

```python
# Analyze audio content
audio_analysis = audio_media.analyze()

# Detect silence
silence_segments = audio_analysis.detect_silence(
    threshold_db=-40,
    min_duration=0.5
)

for segment in silence_segments:
    print(f"Silence: {segment.start}s - {segment.end}s")

# Detect peaks and clipping
clipping_instances = audio_analysis.detect_clipping()
if clipping_instances:
    print(f"Audio clipping detected at {len(clipping_instances)} points")

# Frequency analysis
frequency_data = audio_analysis.get_frequency_spectrum()
```

## Image Media Management

### Image Properties

```python
# Working with image media
image_media = project.get_image_media()[0]

# Image specifications
print(f"Dimensions: {image_media.width}x{image_media.height}")
print(f"Format: {image_media.format}")
print(f"Color Mode: {image_media.color_mode}")
print(f"Has Transparency: {image_media.has_alpha}")
print(f"DPI: {image_media.dpi}")
```

### Image Operations

```python
# Resize image
image_media.resize(
    width=800,
    height=600,
    method="lanczos",  # High-quality resampling
    maintain_aspect=True
)

# Apply image transformations
image_media.rotate(45)
image_media.flip_horizontal()

# Crop image
image_media.crop(
    x=100,
    y=100,
    width=500,
    height=400
)

# Adjust image properties
image_media.set_opacity(0.8)
image_media.adjust_brightness(1.2)
image_media.adjust_contrast(1.1)
image_media.adjust_saturation(0.9)
```

### Image Optimization

```python
# Optimize image for project
image_media.optimize_for_video(
    target_resolution=(1920, 1080),
    quality=85,
    format="jpeg"
)

# Convert image format
image_media.convert_format(
    format="png",
    quality=95,
    preserve_transparency=True
)
```

## Media Import and Export

### Adding New Media

```python
# Add video file
video_media = project.add_video_media(
    path="new_video.mp4",
    name="Product Demo",
    auto_analyze=True
)

# Add audio file
audio_media = project.add_audio_media(
    path="background_music.wav",
    name="Background Track",
    volume=0.6
)

# Add image with specific properties
image_media = project.add_image_media(
    path="logo.png",
    name="Company Logo",
    default_duration=5.0,  # Default duration when added to timeline
    position="top-right"
)
```

### Batch Media Import

```python
from pathlib import Path

# Import all media from directory
media_dir = Path("media_assets")

# Import videos
for video_path in media_dir.glob("*.mp4"):
    project.add_video_media(
        path=str(video_path),
        name=video_path.stem,
        auto_analyze=True
    )

# Import audio files
for audio_path in media_dir.glob("*.wav"):
    project.add_audio_media(
        path=str(audio_path),
        name=audio_path.stem
    )

# Import images
for image_path in media_dir.glob("*.png"):
    project.add_image_media(
        path=str(image_path),
        name=image_path.stem,
        default_duration=3.0
    )
```

### Media Export

```python
# Export media to new location
video_media.export(
    output_path="exported_video.mp4",
    format="mp4",
    quality="high"
)

# Export with specific settings
audio_media.export(
    output_path="exported_audio.wav",
    format="wav",
    sample_rate=48000,
    bit_depth=24
)

# Export image with optimization
image_media.export(
    output_path="exported_image.jpg",
    format="jpeg",
    quality=90,
    optimize=True
)
```

## Media Path Management

### Path Resolution

```python
# Check media file existence
for media in project.source_medias:
    if not media.file_exists():
        print(f"Missing: {media.name} ({media.src})")

# Get absolute paths
for media in project.source_medias:
    abs_path = media.get_absolute_path(project.base_path)
    print(f"{media.name}: {abs_path}")
```

### Updating Media Paths

```python
# Update single media path
video_media.update_path("new_location/video.mp4")

# Batch update media paths
path_mappings = {
    "old_video.mp4": "new_location/new_video.mp4",
    "old_audio.wav": "audio_files/new_audio.wav"
}

project.update_media_paths(path_mappings)

# Update base path for all media
project.rebase_media_paths(
    old_base="C:/old_project",
    new_base="D:/new_project"
)
```

### Media Path Validation

```python
# Validate all media paths
validation_result = project.validate_media_paths()

print(f"Valid paths: {validation_result.valid_count}")
print(f"Invalid paths: {validation_result.invalid_count}")

for invalid_media in validation_result.invalid_media:
    print(f"Invalid: {invalid_media.name} -> {invalid_media.src}")

# Attempt to fix broken paths
auto_fix_result = project.auto_fix_media_paths(
    search_directories=["./media", "./assets", "./videos"]
)

print(f"Fixed {auto_fix_result.fixed_count} media paths")
```

## Media Replacement

### Replace Media Files

```python
# Replace specific media
old_media = project.get_media_by_name("old_video.mp4")
new_media = project.replace_media(
    old_media=old_media,
    new_path="new_video.mp4",
    preserve_timing=True,
    preserve_effects=True
)

# Replace media with different format
project.replace_media(
    old_media=old_media,
    new_path="replacement.mov",
    auto_convert=True  # Convert format if needed
)
```

### Batch Media Replacement

```python
# Replace multiple media files
replacements = {
    "intro_v1.mp4": "intro_v2.mp4",
    "outro_v1.mp4": "outro_v2.mp4",
    "logo_old.png": "logo_new.png"
}

for old_name, new_path in replacements.items():
    old_media = project.get_media_by_name(old_name)
    if old_media:
        project.replace_media(old_media, new_path)
```

## Media Synchronization

### Audio-Video Sync

```python
# Sync audio to video
video_media = project.get_media_by_name("main_video.mp4")
audio_media = project.get_media_by_name("recorded_audio.wav")

# Auto-sync based on audio tracks
sync_result = project.sync_audio_to_video(
    video_media=video_media,
    audio_media=audio_media,
    method="cross_correlation"
)

print(f"Sync offset: {sync_result.offset} seconds")
print(f"Confidence: {sync_result.confidence}")
```

### Manual Sync Adjustment

```python
# Apply manual sync offset
audio_media.apply_sync_offset(-0.5)  # Move audio 0.5 seconds earlier

# Sync multiple audio tracks
for audio in project.get_audio_media():
    if "microphone" in audio.name.lower():
        audio.apply_sync_offset(-0.2)
```

## Media Metadata Management

### Reading Metadata

```python
# Access embedded metadata
metadata = video_media.get_metadata()

print(f"Title: {metadata.get('title', 'Unknown')}")
print(f"Artist: {metadata.get('artist', 'Unknown')}")
print(f"Creation Date: {metadata.get('creation_date')}")
print(f"Camera Model: {metadata.get('camera_model')}")
print(f"GPS Location: {metadata.get('gps_location')}")
```

### Custom Metadata

```python
# Add custom metadata
video_media.set_custom_metadata("project_phase", "final_cut")
video_media.set_custom_metadata("client", "Example Corp")
video_media.set_custom_metadata("shot_type", "close_up")

# Retrieve custom metadata
phase = video_media.get_custom_metadata("project_phase")
print(f"Project phase: {phase}")

# List all custom metadata
custom_meta = video_media.list_custom_metadata()
for key, value in custom_meta.items():
    print(f"{key}: {value}")
```

## Media Performance Optimization

### Caching and Preprocessing

```python
# Enable media caching for better performance
project.enable_media_caching(
    cache_directory="./cache",
    max_cache_size="2GB"
)

# Preprocess media for timeline use
for video in project.get_video_media():
    video.preprocess(
        generate_thumbnails=True,
        create_proxy=True,
        analyze_content=True
    )
```

### Memory Management

```python
# Optimize memory usage for large media files
project.optimize_media_memory_usage(
    max_resolution=(1920, 1080),
    compression_level="medium",
    unload_unused=True
)

# Clear media caches
project.clear_media_caches()
```

## Media Quality Analysis

### Comprehensive Analysis

```python
def analyze_project_media(project):
    """Analyze all media in project for quality issues."""
    analysis_results = []
    
    for media in project.source_medias:
        result = {
            'name': media.name,
            'type': type(media).__name__,
            'file_size': media.file_size,
            'issues': []
        }
        
        # Check file existence
        if not media.file_exists():
            result['issues'].append("File not found")
        
        # Type-specific analysis
        if isinstance(media, VideoMedia):
            if media.frame_rate < 24:
                result['issues'].append("Low frame rate")
            if media.width < 720:
                result['issues'].append("Low resolution")
                
        elif isinstance(media, AudioMedia):
            if media.sample_rate < 44100:
                result['issues'].append("Low sample rate")
            if media.peak_level > -3:
                result['issues'].append("Possible clipping")
                
        elif isinstance(media, ImageMedia):
            if media.width < 1280 or media.height < 720:
                result['issues'].append("Low resolution for video use")
        
        analysis_results.append(result)
    
    return analysis_results

# Run analysis
results = analyze_project_media(project)
for result in results:
    if result['issues']:
        print(f"{result['name']}: {', '.join(result['issues'])}")
```

## Next Steps

Continue exploring advanced Camtasio features:

- **[Effects & Annotations](effects-annotations.md)** - Adding visual elements and callouts
- **[Scaling Operations](scaling-operations.md)** - Resolution and size management  
- **[Batch Processing](batch-processing.md)** - Automating operations across multiple projects
- **[File Format Details](file-format.md)** - Deep dive into Camtasia file formats