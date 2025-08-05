# Timeline Operations

Advanced techniques for manipulating timelines, tracks, and media placement in Camtasia projects.

## Timeline Structure Deep Dive

### Understanding the Timeline Hierarchy

```python
from camtasio import Project

project = Project("example.cmproj")
timeline = project.timeline

# Timeline contains multiple tracks
print(f"Total tracks: {len(timeline.tracks)}")

# Each track contains media items
for track_idx, track in enumerate(timeline.tracks):
    print(f"Track {track_idx}: {track.name}")
    print(f"  Type: {track.type}")
    print(f"  Media count: {len(track.medias)}")
    print(f"  Duration: {track.duration}")
```

### Timeline Properties

```python
# Timeline boundaries
print(f"Timeline start: {timeline.start_time}")
print(f"Timeline end: {timeline.end_time}")  
print(f"Timeline duration: {timeline.duration}")

# Timeline resolution
print(f"Timeline resolution: {timeline.width}x{timeline.height}")

# Playback settings
print(f"Frame rate: {timeline.frame_rate}")
print(f"Time base: {timeline.time_base}")
```

## Track Management

### Track Types and Properties

```python
# Different track types
for track in timeline.tracks:
    if track.is_video_track():
        print(f"Video track: {track.name}")
        print(f"  Dimensions: {track.width}x{track.height}")
        print(f"  Blend mode: {track.blend_mode}")
        print(f"  Opacity: {track.opacity}")
        
    elif track.is_audio_track():
        print(f"Audio track: {track.name}")
        print(f"  Volume: {track.volume}")
        print(f"  Pan: {track.pan}")
        print(f"  Muted: {track.muted}")
        
    elif track.is_annotation_track():
        print(f"Annotation track: {track.name}")
        print(f"  Callouts: {len(track.get_callouts())}")
```

### Creating and Managing Tracks

```python
# Add new tracks
video_track = timeline.add_video_track(
    name="Secondary Video",
    width=1920,
    height=1080
)

audio_track = timeline.add_audio_track(
    name="Background Music",
    volume=0.8
)

annotation_track = timeline.add_annotation_track(
    name="Callouts and Highlights"
)

# Reorder tracks
timeline.move_track(from_index=2, to_index=0)

# Duplicate track
duplicated_track = timeline.duplicate_track(track_index=1)

# Remove track
timeline.remove_track(track_index=3)
```

### Track Properties Modification

```python
# Modify video track properties
video_track = timeline.tracks[0]
video_track.name = "Main Video Content"
video_track.opacity = 0.9
video_track.blend_mode = "multiply"

# Modify audio track properties
audio_track = timeline.get_audio_tracks()[0]
audio_track.volume = 0.75
audio_track.pan = -0.2  # Slightly left
audio_track.muted = False

# Enable/disable tracks
video_track.enabled = True
audio_track.enabled = False
```

## Media Item Operations

### Adding Media to Timeline

```python
# Add video media to track
video_media = video_track.add_media(
    source_media_id="video1",  # Reference to source media
    start_time=0.0,
    duration=10.0,
    x=0,
    y=0,
    width=1920,
    height=1080
)

# Add audio media
audio_media = audio_track.add_media(
    source_media_id="audio1",
    start_time=0.0,
    duration=15.0,
    volume=0.8
)

# Add image media with specific timing
image_media = video_track.add_media(
    source_media_id="logo",
    start_time=5.0,
    duration=3.0,
    x=1600,  # Top-right corner
    y=50,
    width=200,
    height=100
)
```

### Media Positioning and Timing

```python
# Move media in time
media_item = video_track.medias[0]
media_item.start_time = 2.5
media_item.duration = 8.0

# Calculate end time
end_time = media_item.start_time + media_item.duration

# Position media on canvas
media_item.x = 100
media_item.y = 200
media_item.width = 800
media_item.height = 600

# Scale media proportionally
media_item.scale_proportional(scale_factor=1.5)

# Center media on canvas
media_item.center_on_canvas(canvas_width=1920, canvas_height=1080)
```

### Media Transformations

```python
# Rotate media
media_item.rotation = 15.0  # degrees

# Apply scaling
media_item.scale_x = 1.2
media_item.scale_y = 0.8

# Crop media
media_item.crop(
    left=10,
    top=20, 
    right=10,
    bottom=20
)

# Apply opacity
media_item.opacity = 0.7
```

## Timeline Editing Operations

### Cutting and Splitting

```python
# Split media at specific time
original_media = video_track.medias[0]
left_part, right_part = timeline.split_media(
    media=original_media,
    split_time=5.0
)

# Split all tracks at specific time
timeline.split_all_at_time(3.0)

# Cut section from timeline
timeline.cut_section(
    start_time=2.0,
    end_time=5.0,
    delete=True  # Remove cut section
)
```

### Copying and Moving

```python
# Copy media item
copied_media = timeline.copy_media(
    source_media=original_media,
    target_track=video_track,
    new_start_time=10.0
)

# Move media between tracks
timeline.move_media(
    media=original_media,
    target_track=timeline.tracks[2],
    new_start_time=7.0
)

# Duplicate media in place
duplicated = timeline.duplicate_media(
    media=original_media,
    offset_time=15.0  # Place 15 seconds later
)
```

### Timeline Ripple Operations

```python
# Insert gap in timeline
timeline.insert_gap(
    at_time=5.0,
    duration=2.0,
    affect_all_tracks=True
)

# Remove gap from timeline
timeline.remove_gap(
    start_time=3.0,
    end_time=5.0,
    ripple_following=True
)

# Ripple delete (remove and close gap)
timeline.ripple_delete(
    start_time=10.0,
    end_time=12.0
)
```

## Advanced Timeline Features

### Timeline Markers

```python
# Add markers to timeline
timeline.add_marker(
    time=5.0,
    name="Scene Change",
    color="#FF0000"
)

timeline.add_marker(
    time=10.0,
    name="Call to Action",
    color="#00FF00",
    description="Add CTA overlay here"
)

# Get all markers
markers = timeline.get_markers()
for marker in markers:
    print(f"Marker: {marker.name} at {marker.time}s")

# Find markers in range
markers_in_range = timeline.get_markers_in_range(5.0, 15.0)
```

### Timeline Groups

```python
# Create track group
group = timeline.create_group(
    name="Main Content",
    tracks=[timeline.tracks[0], timeline.tracks[1]]
)

# Group properties
group.locked = False
group.solo = False
group.muted = False

# Add tracks to existing group
group.add_track(timeline.tracks[2])

# Remove track from group
group.remove_track(timeline.tracks[1])

# Ungroup tracks
timeline.ungroup(group)
```

### Timeline Effects

```python
# Apply effect to entire track
from camtasio.effects import BlurEffect, ColorAdjustment

blur_effect = BlurEffect(
    intensity=5.0,
    start_time=0.0,
    duration=timeline.duration
)
video_track.add_effect(blur_effect)

# Apply time-based effect
color_effect = ColorAdjustment(
    brightness=1.2,
    contrast=1.1,
    saturation=0.9,
    start_time=5.0,
    duration=10.0
)
video_track.add_effect(color_effect)
```

## Timeline Analysis

### Timeline Statistics

```python
def analyze_timeline(timeline):
    """Generate comprehensive timeline statistics."""
    stats = {
        'total_duration': timeline.duration,
        'track_count': len(timeline.tracks),
        'media_count': 0,
        'video_tracks': 0,
        'audio_tracks': 0,
        'annotation_tracks': 0,
        'gaps': [],
        'overlaps': []
    }
    
    # Count tracks by type
    for track in timeline.tracks:
        stats['media_count'] += len(track.medias)
        
        if track.is_video_track():
            stats['video_tracks'] += 1
        elif track.is_audio_track():
            stats['audio_tracks'] += 1
        elif track.is_annotation_track():
            stats['annotation_tracks'] += 1
    
    # Find gaps and overlaps
    for track in timeline.tracks:
        gaps = track.find_gaps()
        overlaps = track.find_overlaps()
        
        stats['gaps'].extend(gaps)
        stats['overlaps'].extend(overlaps)
    
    return stats

# Use the analysis
stats = analyze_timeline(timeline)
print(f"Timeline has {stats['media_count']} media items across {stats['track_count']} tracks")
```

### Finding Timeline Issues

```python
# Find empty tracks
empty_tracks = timeline.find_empty_tracks()
print(f"Empty tracks: {[t.name for t in empty_tracks]}")

# Find tracks with gaps
tracks_with_gaps = timeline.find_tracks_with_gaps()

# Find overlapping media
overlapping_media = timeline.find_overlapping_media()
for overlap in overlapping_media:
    print(f"Overlap: {overlap.media1.name} and {overlap.media2.name}")
    print(f"  Time: {overlap.start_time} - {overlap.end_time}")

# Find unused source media
unused_media = timeline.find_unused_source_media()
```

## Timeline Optimization

### Cleanup Operations

```python
# Remove empty tracks
timeline.remove_empty_tracks()

# Consolidate gaps
timeline.consolidate_gaps(min_gap_duration=0.1)

# Remove duplicate media
timeline.remove_duplicate_media()

# Optimize media order
timeline.optimize_media_order()
```

### Performance Optimization

```python
# Reduce timeline complexity
timeline.simplify_keyframes(tolerance=0.01)

# Merge adjacent similar media
timeline.merge_adjacent_media(similarity_threshold=0.95)

# Optimize track structure
timeline.optimize_track_structure()
```

## Timeline Export and Import

### Exporting Timeline Data

```python
# Export timeline to various formats
timeline_json = timeline.to_json(indent=2)

# Export with media references
timeline_with_refs = timeline.to_dict(include_media_refs=True)

# Export specific time range
partial_timeline = timeline.extract_range(
    start_time=10.0,
    end_time=20.0
)
```

### Timeline Templates

```python
# Save timeline as template
timeline_template = timeline.create_template(
    name="Standard Intro Template",
    description="3-second intro with logo",
    duration=3.0
)

# Apply template to project
project.apply_timeline_template(
    template=timeline_template,
    position="start"  # or "end", "replace"
)
```

## Working with Multiple Timelines

### Timeline Comparison

```python
# Compare two timelines
from camtasio.comparison import TimelineComparator

comparator = TimelineComparator()
differences = comparator.compare(timeline1, timeline2)

for diff in differences:
    print(f"Difference: {diff.type} at {diff.location}")
```

### Timeline Merging

```python
# Merge two timelines
merged_timeline = timeline1.merge_with(
    other_timeline=timeline2,
    mode="append",  # or "overlay", "replace"
    start_time=timeline1.duration
)

# Combine specific tracks
timeline1.import_tracks_from(
    source_timeline=timeline2,
    track_indices=[0, 2],
    start_time=5.0
)
```

## Timeline Synchronization

### Audio-Video Sync

```python
# Sync video to audio track
timeline.sync_video_to_audio(
    video_track_index=0,
    audio_track_index=1,
    sync_point_time=5.0
)

# Auto-detect sync points
sync_points = timeline.detect_sync_points()
for point in sync_points:
    print(f"Sync point at {point.time}: confidence {point.confidence}")
```

### Multi-track Alignment

```python
# Align all tracks to specific marker
timeline.align_tracks_to_marker("Scene Start")

# Align tracks by content analysis
timeline.auto_align_tracks(
    reference_track_index=0,
    analysis_method="audio_waveform"
)
```

## Next Steps

Continue exploring advanced Camtasio features:

- **[Media Management](media-management.md)** - Working with video, audio, and images
- **[Effects & Annotations](effects-annotations.md)** - Adding visual elements and callouts
- **[Scaling Operations](scaling-operations.md)** - Resolution and size management
- **[Batch Processing](batch-processing.md)** - Automating operations across multiple projects