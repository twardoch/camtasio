# Effects & Annotations

Comprehensive guide to working with visual effects, callouts, annotations, and transitions in Camtasia projects.

## Understanding Effects and Annotations

### Types of Visual Elements

Camtasia supports various types of visual enhancements:

```python
from camtasio import Project
from camtasio.annotations import Callout, HighlightBox, Arrow, Sketch
from camtasio.effects import Transition, ColorAdjustment, BlurEffect

project = Project("example.cmproj")

# Get all annotations in project
annotations = project.get_all_annotations()
for annotation in annotations:
    print(f"Annotation: {annotation.type} - {annotation.name}")
    print(f"  Duration: {annotation.start_time} to {annotation.end_time}")
    print(f"  Position: ({annotation.x}, {annotation.y})")
```

### Annotation Categories

- **Callouts**: Text boxes with customizable styling
- **Shapes**: Rectangles, circles, arrows, and custom shapes  
- **Highlights**: Spotlight effects and highlight boxes
- **Sketches**: Hand-drawn annotations and markup
- **Transitions**: Scene changes and visual effects
- **Filters**: Color adjustments, blur, and distortion effects

## Working with Callouts

### Creating Basic Callouts

```python
# Add simple text callout
callout = project.add_callout(
    text="Welcome to our tutorial!",
    x=100,
    y=200,
    start_time=2.0,
    duration=4.0
)

# Callout with custom styling
styled_callout = project.add_callout(
    text="Important Note",
    x=500,
    y=300,
    start_time=8.0,
    duration=3.0,
    font_family="Arial",
    font_size=24,
    font_color="#FFFFFF",
    background_color="#FF0000",
    border_width=2,
    border_color="#000000"
)
```

### Advanced Callout Properties

```python
# Create callout with advanced properties
advanced_callout = Callout(
    text="Click here to continue",
    x=400,
    y=500,
    width=300,
    height=100,
    start_time=10.0,
    duration=5.0,
    
    # Text properties
    font_family="Helvetica",
    font_size=18,
    font_weight="bold",
    font_style="italic",
    text_align="center",
    text_color="#333333",
    
    # Background properties
    background_color="#FFFF99",
    background_opacity=0.9,
    border_radius=10,
    
    # Border properties
    border_width=3,
    border_color="#FF6600",
    border_style="solid",
    
    # Shadow properties
    shadow_enabled=True,
    shadow_color="#000000",
    shadow_opacity=0.3,
    shadow_offset_x=3,
    shadow_offset_y=3,
    shadow_blur=5
)

project.timeline.add_annotation(advanced_callout)
```

### Callout Animation

```python
# Add fade-in/fade-out animation
callout.add_fade_in(duration=0.5)
callout.add_fade_out(duration=0.5)

# Add movement animation
callout.animate_position(
    start_x=100, start_y=200,
    end_x=500, end_y=300,
    duration=2.0,
    easing="ease_in_out"
)

# Scale animation
callout.animate_scale(
    start_scale=0.5,
    end_scale=1.0,
    duration=1.0
)

# Rotation animation
callout.animate_rotation(
    start_angle=0,
    end_angle=360,
    duration=3.0
)
```

## Highlight Effects

### Highlight Boxes

```python
# Create highlight box
highlight = project.add_highlight_box(
    x=200,
    y=150,
    width=400,
    height=300,
    start_time=5.0,
    duration=4.0,
    color="#FFFF00",
    opacity=0.3,
    border_width=3,
    border_color="#FF0000"
)

# Animated highlight
highlight.add_pulse_animation(
    pulse_rate=2.0,  # pulses per second
    min_opacity=0.2,
    max_opacity=0.8
)
```

### Spotlight Effects

```python
# Create spotlight effect
spotlight = project.add_spotlight(
    center_x=500,
    center_y=400,
    radius=200,
    start_time=3.0,
    duration=6.0,
    feather=50,  # Edge softness
    opacity=0.7
)

# Moving spotlight
spotlight.animate_position(
    path_points=[
        (300, 200),
        (500, 400),
        (700, 600)
    ],
    duration=spotlight.duration,
    smooth=True
)
```

## Shape Annotations

### Basic Shapes

```python
# Rectangle annotation
rectangle = project.add_rectangle(
    x=100, y=100,
    width=200, height=150,
    start_time=1.0,
    duration=5.0,
    fill_color="#FF0000",
    fill_opacity=0.5,
    border_color="#000000",
    border_width=2
)

# Circle annotation
circle = project.add_circle(
    center_x=400,
    center_y=300,
    radius=75,
    start_time=2.0,
    duration=4.0,
    fill_color="#00FF00",
    border_color="#0000FF",
    border_width=3
)

# Line annotation
line = project.add_line(
    start_x=100, start_y=100,
    end_x=500, end_y=400,
    start_time=3.0,
    duration=3.0,
    color="#FF00FF",
    width=5,
    style="dashed"
)
```

### Arrow Annotations

```python
# Simple arrow
arrow = project.add_arrow(
    start_x=200, start_y=200,
    end_x=400, end_y=300,
    start_time=4.0,
    duration=3.0,
    color="#FF0000",
    width=4,
    head_size=20
)

# Curved arrow
curved_arrow = project.add_curved_arrow(
    start_x=100, start_y=300,
    end_x=500, end_y=300,
    control_x=300, control_y=100,  # Bezier control point
    start_time=6.0,
    duration=4.0,
    color="#0000FF",
    width=6
)

# Arrow with custom head style
custom_arrow = project.add_arrow(
    start_x=300, start_y=400,
    end_x=600, end_y=400,
    start_time=8.0,
    duration=2.0,
    color="#00FF00",
    width=3,
    head_style="filled",  # or "outlined", "diamond"
    head_size=15,
    tail_style="none"  # or "circle", "square"
)
```

## Sketch Annotations

### Freehand Drawing

```python
# Create sketch annotation
sketch = project.add_sketch(
    start_time=5.0,
    duration=8.0,
    color="#FF0000",
    width=3,
    opacity=0.8
)

# Add drawing path
sketch.add_path([
    (100, 200), (120, 180), (150, 160),
    (180, 150), (220, 160), (250, 180),
    (270, 200), (280, 230), (270, 260)
])

# Add multiple strokes
sketch.add_stroke(
    points=[(300, 300), (350, 320), (400, 300)],
    color="#0000FF",
    width=4
)
```

### Sketch Tools

```python
# Highlighter effect
highlighter = project.add_highlighter_stroke(
    points=[(100, 100), (300, 100), (300, 120), (100, 120)],
    start_time=3.0,
    duration=2.0,
    color="#FFFF00",
    opacity=0.5,
    width=20
)

# Eraser effect
sketch.add_eraser_stroke(
    points=[(200, 150), (250, 150)],
    width=15
)
```

## Visual Effects

### Color Adjustments

```python
# Apply color correction to video track
color_adjustment = ColorAdjustment(
    brightness=1.1,
    contrast=1.2,
    saturation=0.9,
    hue_shift=10,  # degrees
    start_time=0.0,
    duration=project.duration
)

video_track = project.timeline.get_video_tracks()[0]
video_track.add_effect(color_adjustment)

# Keyframe color changes
color_adjustment.add_keyframe(
    time=5.0,
    brightness=1.3,
    saturation=1.2
)
```

### Blur and Focus Effects

```python
# Gaussian blur
blur_effect = BlurEffect(
    intensity=5.0,
    start_time=2.0,
    duration=3.0,
    effect_type="gaussian"
)

# Motion blur
motion_blur = BlurEffect(
    intensity=8.0,
    angle=45,  # degrees
    start_time=8.0,
    duration=2.0,
    effect_type="motion"
)

# Progressive blur (focus pull)
progressive_blur = BlurEffect(
    start_intensity=0.0,
    end_intensity=10.0,
    start_time=10.0,
    duration=4.0,
    easing="ease_in_out"
)

video_track.add_effect(blur_effect)
video_track.add_effect(motion_blur)
video_track.add_effect(progressive_blur)
```

### Distortion Effects

```python
# Zoom effect
zoom_effect = project.add_zoom_effect(
    start_scale=1.0,
    end_scale=2.0,
    center_x=500,
    center_y=400,
    start_time=6.0,
    duration=3.0
)

# Ken Burns effect (pan and zoom)
ken_burns = project.add_ken_burns_effect(
    start_x=0, start_y=0, start_scale=1.0,
    end_x=200, end_y=100, end_scale=1.5,
    start_time=0.0,
    duration=10.0
)
```

## Transitions

### Basic Transitions

```python
# Fade transition
fade_transition = project.add_fade_transition(
    start_time=10.0,
    duration=1.0,
    fade_type="cross_fade"  # or "fade_in", "fade_out"
)

# Wipe transition
wipe_transition = project.add_wipe_transition(
    start_time=15.0,
    duration=1.5,
    direction="left_to_right",  # or "top_to_bottom", "circular"
    edge_softness=0.1
)

# Dissolve transition
dissolve_transition = project.add_dissolve_transition(
    start_time=20.0,
    duration=2.0,
    pattern="random",  # or "grid", "spiral"
)
```

### Advanced Transitions

```python
# 3D cube transition
cube_transition = project.add_cube_transition(
    start_time=25.0,
    duration=2.0,
    rotation_axis="y",  # or "x", "z"
    direction="clockwise"
)

# Page curl transition
page_curl = project.add_page_curl_transition(
    start_time=30.0,
    duration=1.8,
    curl_direction="bottom_right",
    shadow_opacity=0.3
)

# Mosaic transition
mosaic_transition = project.add_mosaic_transition(
    start_time=35.0,
    duration=2.5,
    tile_size=50,
    randomization=0.3
)
```

## Animation and Keyframes

### Keyframe Animation

```python
# Create animated callout
animated_callout = project.add_callout(
    text="Moving Text",
    x=100, y=200,
    start_time=5.0,
    duration=10.0
)

# Add position keyframes
animated_callout.add_position_keyframe(time=5.0, x=100, y=200)
animated_callout.add_position_keyframe(time=10.0, x=500, y=300)
animated_callout.add_position_keyframe(time=15.0, x=800, y=200)

# Add scale keyframes
animated_callout.add_scale_keyframe(time=5.0, scale=1.0)
animated_callout.add_scale_keyframe(time=7.5, scale=1.5)
animated_callout.add_scale_keyframe(time=15.0, scale=1.0)

# Add opacity keyframes
animated_callout.add_opacity_keyframe(time=5.0, opacity=0.0)
animated_callout.add_opacity_keyframe(time=6.0, opacity=1.0)
animated_callout.add_opacity_keyframe(time=14.0, opacity=1.0)
animated_callout.add_opacity_keyframe(time=15.0, opacity=0.0)
```

### Easing Functions

```python
# Apply different easing to animations
callout.set_position_easing("ease_in_out")
callout.set_scale_easing("bounce")
callout.set_opacity_easing("ease_out")

# Available easing types:
# - linear
# - ease_in, ease_out, ease_in_out
# - bounce, elastic
# - back_in, back_out, back_in_out
# - custom_bezier
```

## Interactive Elements

### Clickable Hotspots

```python
# Add clickable area
hotspot = project.add_hotspot(
    x=300, y=200,
    width=150, height=50,
    start_time=8.0,
    duration=5.0,
    cursor="pointer",
    tooltip="Click to learn more"
)

# Hotspot with action
hotspot.set_action(
    action_type="jump_to_time",
    target_time=20.0
)

# Hotspot with URL action
hotspot.set_action(
    action_type="open_url",
    url="https://example.com"
)
```

### Quiz Elements

```python
# Add quiz question
quiz_question = project.add_quiz_question(
    question="What is the capital of France?",
    x=200, y=300,
    start_time=15.0,
    duration=10.0,
    answers=[
        {"text": "London", "correct": False},
        {"text": "Paris", "correct": True},
        {"text": "Berlin", "correct": False},
        {"text": "Madrid", "correct": False}
    ]
)

# Customize quiz appearance
quiz_question.set_style(
    background_color="#F0F0F0",
    border_color="#333333",
    correct_color="#00FF00",
    incorrect_color="#FF0000"
)
```

## Annotation Management

### Grouping Annotations

```python
# Create annotation group
annotation_group = project.create_annotation_group(
    name="Scene 1 Annotations",
    annotations=[callout, highlight, arrow]
)

# Group operations
annotation_group.move_all(offset_x=50, offset_y=30)
annotation_group.scale_all(scale_factor=1.2)
annotation_group.set_opacity_all(0.8)

# Time-shift all annotations in group
annotation_group.shift_time_all(offset=2.0)
```

### Annotation Templates

```python
# Create reusable annotation template
template = project.create_annotation_template(
    name="Standard Callout",
    base_annotation=styled_callout,
    customizable_properties=["text", "x", "y", "start_time"]
)

# Apply template
new_callout = template.create_instance(
    text="New message",
    x=600,
    y=400,
    start_time=12.0
)
```

## Batch Operations

### Mass Annotation Updates

```python
# Update all callouts
for annotation in project.get_annotations_by_type("callout"):
    annotation.font_size = 20
    annotation.font_family = "Arial"
    annotation.border_width = 2

# Update annotations in time range
annotations_in_range = project.get_annotations_in_time_range(5.0, 15.0)
for annotation in annotations_in_range:
    annotation.opacity = 0.9

# Apply style to all annotations
style_properties = {
    "border_color": "#333333",
    "background_opacity": 0.8,
    "shadow_enabled": True
}
project.apply_style_to_annotations(style_properties, annotation_type="callout")
```

### Annotation Cleanup

```python
# Remove empty annotations
project.remove_empty_annotations()

# Remove annotations shorter than threshold
project.remove_short_annotations(min_duration=0.5)

# Merge overlapping annotations
project.merge_overlapping_annotations(tolerance=0.1)

# Optimize annotation timing
project.optimize_annotation_timing()
```

## Advanced Effect Techniques

### Chroma Key (Green Screen)

```python
from camtasio.effects import ChromaKeyEffect

# Apply chroma key effect
chroma_key = ChromaKeyEffect(
    key_color="#00FF00",  # Green
    tolerance=0.3,
    edge_softness=0.1,
    spill_suppression=0.5,
    start_time=0.0,
    duration=project.duration
)

video_track.add_effect(chroma_key)

# Fine-tune chroma key
chroma_key.add_keyframe(
    time=5.0,
    tolerance=0.4,
    edge_softness=0.15
)
```

### Mask Effects

```python
# Create circular mask
circular_mask = project.add_circular_mask(
    center_x=500,
    center_y=400,
    radius=200,
    feather=20,
    start_time=3.0,
    duration=8.0
)

# Rectangular mask with rounded corners
rect_mask = project.add_rectangular_mask(
    x=200, y=150,
    width=400, height=300,
    corner_radius=25,
    start_time=12.0,
    duration=6.0
)

# Custom shape mask
custom_mask = project.add_custom_mask(
    path_points=[
        (100, 200), (300, 100), (500, 200),
        (450, 400), (150, 400)
    ],
    start_time=20.0,
    duration=5.0
)
```

## Performance and Optimization

### Effect Optimization

```python
# Optimize effects for performance
project.optimize_effects(
    combine_similar=True,
    reduce_keyframes=True,
    simplify_paths=True
)

# Cache effect renders
project.enable_effect_caching(
    cache_directory="./effect_cache",
    max_cache_size="1GB"
)
```

### Rendering Considerations

```python
# Check effect complexity
complexity_score = project.calculate_effect_complexity()
print(f"Effect complexity: {complexity_score}")

if complexity_score > 0.8:
    print("Consider reducing effects for better performance")

# Suggest optimizations
optimizations = project.suggest_effect_optimizations()
for optimization in optimizations:
    print(f"Optimization: {optimization.description}")
```

## Next Steps

Continue exploring advanced Camtasio features:

- **[Scaling Operations](scaling-operations.md)** - Resolution and size management
- **[Batch Processing](batch-processing.md)** - Automating operations across multiple projects  
- **[File Format Details](file-format.md)** - Deep dive into Camtasia file formats