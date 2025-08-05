# Scaling Operations

Advanced resolution management and scaling techniques for Camtasia projects using Camtasio.

## Understanding Scaling Concepts

### Types of Scaling Operations

Camtasio supports several types of scaling operations, each suited for different use cases:

```python
from camtasio import Project
from camtasio.scaler import ProjectScaler, MediaScaler

project = Project("example.cmproj")

# 1. Canvas scaling - changes project resolution
project.scale_canvas(1920, 1080)

# 2. Content scaling - scales all media proportionally  
project.scale_content(scale_factor=1.5)

# 3. Resolution scaling - changes resolution and scales content
project.scale_to_resolution(1920, 1080, preserve_aspect=True)

# 4. Individual media scaling
for media in project.timeline.get_all_media():
    media.scale(1.2)
```

### Scaling Modes

```python
# Different scaling approaches
scaler = ProjectScaler()

# Proportional scaling (maintains aspect ratio)
scaler.scale_proportional(
    project=project,
    target_width=1920,
    target_height=1080
)

# Stretch scaling (may distort content)
scaler.scale_stretch(
    project=project,
    target_width=1280,
    target_height=720
)

# Fit scaling (fits content within bounds)
scaler.scale_fit(
    project=project,
    target_width=1920,
    target_height=1080,
    fill_background=True,
    background_color="#000000"
)

# Crop scaling (maintains aspect, crops excess)
scaler.scale_crop(
    project=project,
    target_width=1920,
    target_height=1080,
    crop_position="center"  # or "top", "bottom", "left", "right"
)
```

## Canvas and Resolution Management

### Canvas Properties

```python
# Get current canvas settings
canvas = project.canvas
print(f"Current resolution: {canvas.width}x{canvas.height}")
print(f"Frame rate: {canvas.frame_rate}")
print(f"Aspect ratio: {canvas.aspect_ratio}")
print(f"Background color: {canvas.background_color}")

# Check if project needs scaling
if canvas.width < 1920 or canvas.height < 1080:
    print("Project could benefit from upscaling")
```

### Resolution Presets

```python
# Common resolution presets
RESOLUTION_PRESETS = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "4K": (3840, 2160),
    "instagram_square": (1080, 1080),
    "instagram_story": (1080, 1920),
    "youtube_thumbnail": (1280, 720),
    "facebook_cover": (1200, 630)
}

# Scale to preset
def scale_to_preset(project, preset_name):
    if preset_name in RESOLUTION_PRESETS:
        width, height = RESOLUTION_PRESETS[preset_name]
        project.scale_to_resolution(width, height, preserve_aspect=True)
        print(f"Scaled to {preset_name}: {width}x{height}")
    else:
        print(f"Unknown preset: {preset_name}")

# Usage
scale_to_preset(project, "1080p")
```

### Canvas Background Management

```python
# Set canvas background
project.canvas.background_color = "#FFFFFF"  # White background
project.canvas.background_opacity = 1.0

# Background image
project.canvas.set_background_image(
    image_path="background.jpg",
    scaling_mode="stretch"  # or "fit", "fill", "tile"
)

# Gradient background
project.canvas.set_gradient_background(
    start_color="#FF0000",
    end_color="#0000FF",
    direction="vertical"  # or "horizontal", "diagonal"
)
```

## Media Scaling Techniques

### Individual Media Scaling

```python
# Scale specific media item
media_item = project.timeline.tracks[0].medias[0]

# Simple scaling
media_item.scale(1.5)  # 150% size

# Aspect-aware scaling
media_item.scale_to_size(
    target_width=800,
    target_height=600,
    maintain_aspect=True
)

# Scale to fit canvas
media_item.scale_to_fit_canvas(
    canvas_width=project.width,
    canvas_height=project.height,
    margin=50  # 50px margin on all sides
)
```

### Batch Media Scaling

```python
# Scale all video media
video_media = project.timeline.get_video_media()
for media in video_media:
    media.scale(1.2)

# Scale media by type
image_media = project.timeline.get_image_media()
for media in image_media:
    media.scale_to_size(400, 300, maintain_aspect=True)

# Conditional scaling
for media in project.timeline.get_all_media():
    # Scale up small media
    if media.width < 1280:
        scale_factor = 1280 / media.width
        media.scale(scale_factor)
    
    # Scale down oversized media
    elif media.width > 1920:
        scale_factor = 1920 / media.width
        media.scale(scale_factor)
```

### Smart Media Positioning

```python
# Auto-position scaled media
def smart_position_media(project):
    canvas_width = project.width
    canvas_height = project.height
    
    for track in project.timeline.tracks:
        for i, media in enumerate(track.medias):
            # Calculate grid position for multiple media
            grid_cols = 2
            grid_rows = 2
            
            col = i % grid_cols
            row = (i // grid_cols) % grid_rows
            
            # Position in grid
            cell_width = canvas_width / grid_cols
            cell_height = canvas_height / grid_rows
            
            media.x = col * cell_width + (cell_width - media.width) / 2
            media.y = row * cell_height + (cell_height - media.height) / 2

# Apply smart positioning
smart_position_media(project)
```

## Advanced Scaling Algorithms

### Quality-Preserving Scaling

```python
from camtasio.scaler import AdvancedScaler

# High-quality scaling with interpolation
advanced_scaler = AdvancedScaler()

# Lanczos resampling (best quality)
advanced_scaler.scale_with_lanczos(
    project=project,
    target_resolution=(1920, 1080),
    preserve_sharpness=True
)

# Bicubic interpolation (good quality, faster)
advanced_scaler.scale_with_bicubic(
    project=project,
    target_resolution=(1920, 1080)
)

# AI-powered upscaling (experimental)
advanced_scaler.scale_with_ai(
    project=project,
    target_resolution=(3840, 2160),
    model="esrgan"  # Enhanced Super-Resolution GAN
)
```

### Content-Aware Scaling

```python
# Analyze content for optimal scaling
content_analyzer = project.analyze_content()

for media in project.timeline.get_all_media():
    analysis = content_analyzer.analyze_media(media)
    
    # Scale based on content type
    if analysis.content_type == "text":
        # Preserve text sharpness
        media.scale_with_text_optimization(1.5)
    elif analysis.content_type == "face":
        # Preserve facial features
        media.scale_with_face_optimization(1.3)
    elif analysis.content_type == "diagram":
        # Preserve line clarity
        media.scale_with_line_optimization(1.2)
```

### Multi-Pass Scaling

```python
# Progressive scaling for large size changes
def progressive_scale(media, target_scale):
    current_scale = 1.0
    
    while abs(current_scale - target_scale) > 0.1:
        # Scale in steps to maintain quality
        if target_scale > current_scale:
            step_scale = min(current_scale * 1.5, target_scale)
        else:
            step_scale = max(current_scale * 0.7, target_scale)
        
        scale_factor = step_scale / current_scale
        media.scale(scale_factor)
        current_scale = step_scale

# Apply progressive scaling
for media in project.timeline.get_all_media():
    progressive_scale(media, 2.0)  # Scale to 200%
```

## Aspect Ratio Management

### Aspect Ratio Conversion

```python
# Convert between aspect ratios
def convert_aspect_ratio(project, target_ratio, method="letterbox"):
    current_ratio = project.width / project.height
    target_width, target_height = target_ratio
    new_ratio = target_width / target_height
    
    if method == "letterbox":
        # Add black bars to maintain content
        if new_ratio > current_ratio:
            # Add side bars
            new_width = int(project.height * new_ratio)
            project.scale_canvas(new_width, project.height)
        else:
            # Add top/bottom bars
            new_height = int(project.width / new_ratio)
            project.scale_canvas(project.width, new_height)
            
    elif method == "crop":
        # Crop content to fit new ratio
        if new_ratio > current_ratio:
            # Crop top/bottom
            new_height = int(project.width / new_ratio)
            crop_offset = (project.height - new_height) / 2
            project.crop_canvas(0, crop_offset, project.width, new_height)
        else:
            # Crop sides
            new_width = int(project.height * new_ratio)
            crop_offset = (project.width - new_width) / 2
            project.crop_canvas(crop_offset, 0, new_width, project.height)
    
    elif method == "stretch":
        # Stretch content to fit (may distort)
        project.scale_to_resolution(target_width, target_height, preserve_aspect=False)

# Convert to different aspect ratios
convert_aspect_ratio(project, (16, 9), method="letterbox")  # Widescreen
convert_aspect_ratio(project, (4, 3), method="crop")       # Standard
convert_aspect_ratio(project, (1, 1), method="letterbox")  # Square
```

### Social Media Optimizations

```python
# Optimize for different social platforms
def optimize_for_platform(project, platform):
    platform_specs = {
        "youtube": {
            "resolution": (1920, 1080),
            "aspect_ratio": 16/9,
            "safe_area_margin": 60
        },
        "instagram_feed": {
            "resolution": (1080, 1080),
            "aspect_ratio": 1/1,
            "safe_area_margin": 40
        },
        "instagram_story": {
            "resolution": (1080, 1920),
            "aspect_ratio": 9/16,
            "safe_area_margin": 100
        },
        "tiktok": {
            "resolution": (1080, 1920),
            "aspect_ratio": 9/16,
            "safe_area_margin": 120
        },
        "facebook": {
            "resolution": (1280, 720),
            "aspect_ratio": 16/9,
            "safe_area_margin": 50
        }
    }
    
    if platform in platform_specs:
        specs = platform_specs[platform]
        
        # Scale to platform resolution
        project.scale_to_resolution(*specs["resolution"])
        
        # Add safe area margins
        margin = specs["safe_area_margin"]
        project.add_safe_area_guide(margin)
        
        # Adjust text sizes for platform
        project.optimize_text_for_platform(platform)

# Optimize for specific platforms
optimize_for_platform(project, "youtube")
```

## Scaling Quality Control

### Quality Assessment

```python
# Assess scaling quality
def assess_scaling_quality(original_project, scaled_project):
    quality_metrics = {
        "resolution_change": scaled_project.width / original_project.width,
        "media_quality_loss": 0.0,
        "text_readability": 0.0,
        "overall_score": 0.0
    }
    
    # Check media quality loss
    media_issues = 0
    total_media = len(scaled_project.timeline.get_all_media())
    
    for original, scaled in zip(
        original_project.timeline.get_all_media(),
        scaled_project.timeline.get_all_media()
    ):
        # Check for pixelation
        if scaled.width > original.width * 1.5:
            media_issues += 1
        
        # Check for over-compression
        if scaled.width < original.width * 0.5:
            media_issues += 1
    
    quality_metrics["media_quality_loss"] = media_issues / total_media if total_media > 0 else 0
    
    # Assess text readability
    text_elements = scaled_project.get_text_elements()
    readable_text = sum(1 for text in text_elements if text.font_size >= 12)
    quality_metrics["text_readability"] = readable_text / len(text_elements) if text_elements else 1.0
    
    # Calculate overall score
    quality_metrics["overall_score"] = (
        (1.0 - quality_metrics["media_quality_loss"]) * 0.4 +
        quality_metrics["text_readability"] * 0.4 +
        min(quality_metrics["resolution_change"], 2.0) / 2.0 * 0.2
    )
    
    return quality_metrics

# Use quality assessment
scaled_project = project.copy()
scaled_project.scale_to_resolution(3840, 2160)

quality = assess_scaling_quality(project, scaled_project)
print(f"Scaling quality score: {quality['overall_score']:.2f}")
```

### Automatic Quality Optimization

```python
# Auto-optimize scaling parameters
def auto_optimize_scaling(project, target_resolution):
    best_quality = 0.0
    best_settings = None
    
    # Test different scaling methods
    methods = ["lanczos", "bicubic", "bilinear"]
    preserve_aspect_options = [True, False]
    
    for method in methods:
        for preserve_aspect in preserve_aspect_options:
            # Create test scaling
            test_project = project.copy()
            test_project.scale_to_resolution(
                *target_resolution,
                method=method,
                preserve_aspect=preserve_aspect
            )
            
            # Assess quality
            quality = assess_scaling_quality(project, test_project)
            
            if quality["overall_score"] > best_quality:
                best_quality = quality["overall_score"]
                best_settings = {
                    "method": method,
                    "preserve_aspect": preserve_aspect,
                    "quality_score": best_quality
                }
    
    return best_settings

# Auto-optimize and apply best settings
best_settings = auto_optimize_scaling(project, (1920, 1080))
print(f"Best scaling method: {best_settings['method']}")
print(f"Quality score: {best_settings['quality_score']:.2f}")

# Apply optimized scaling
project.scale_to_resolution(
    1920, 1080,
    method=best_settings["method"],
    preserve_aspect=best_settings["preserve_aspect"]
)
```

## Batch Scaling Operations

### Multi-Project Scaling

```python
from pathlib import Path

def batch_scale_projects(project_dir, target_resolution, output_dir):
    """Scale multiple projects to target resolution."""
    project_paths = Path(project_dir).glob("*.cmproj")
    results = []
    
    for project_path in project_paths:
        try:
            # Load project
            project = Project(project_path)
            
            # Store original stats
            original_resolution = (project.width, project.height)
            
            # Scale project
            project.scale_to_resolution(*target_resolution)
            
            # Save to output directory
            output_path = Path(output_dir) / project_path.name
            project.save_as(output_path)
            
            results.append({
                "project": project_path.name,
                "original_resolution": original_resolution,
                "new_resolution": target_resolution,
                "status": "success"
            })
            
        except Exception as e:
            results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return results

# Batch scale all projects
results = batch_scale_projects(
    project_dir="./projects",
    target_resolution=(1920, 1080),
    output_dir="./scaled_projects"
)

# Report results
for result in results:
    if result["status"] == "success":
        print(f"✓ {result['project']}: {result['original_resolution']} → {result['new_resolution']}")
    else:
        print(f"✗ {result['project']}: {result['error']}")
```

### Conditional Scaling

```python
def smart_batch_scale(project_paths, rules):
    """Apply different scaling rules based on project characteristics."""
    
    for project_path in project_paths:
        project = Project(project_path)
        
        # Analyze project characteristics
        duration = project.duration
        resolution = (project.width, project.height)
        media_count = len(project.timeline.get_all_media())
        
        # Apply appropriate rule
        for rule in rules:
            if rule["condition"](project, duration, resolution, media_count):
                target_res = rule["target_resolution"]
                method = rule.get("method", "lanczos")
                
                project.scale_to_resolution(*target_res, method=method)
                
                # Save with rule identifier
                output_name = f"{rule['name']}_{project_path.stem}.cmproj"
                project.save_as(project_path.parent / output_name)
                break

# Define scaling rules
scaling_rules = [
    {
        "name": "4k_long_form",
        "condition": lambda p, d, r, m: d > 600 and r[0] >= 1920,  # Long videos in HD+
        "target_resolution": (3840, 2160),
        "method": "lanczos"
    },
    {
        "name": "1080p_standard",
        "condition": lambda p, d, r, m: d > 60 and r[0] >= 1280,   # Standard videos
        "target_resolution": (1920, 1080),
        "method": "bicubic"
    },
    {
        "name": "720p_short",
        "condition": lambda p, d, r, m: d <= 60,                    # Short clips
        "target_resolution": (1280, 720),
        "method": "bilinear"
    }
]

# Apply smart scaling
project_list = list(Path("./projects").glob("*.cmproj"))
smart_batch_scale(project_list, scaling_rules)
```

## Performance Optimization

### Memory-Efficient Scaling

```python
# Scale large projects efficiently
def memory_efficient_scale(project, target_resolution, chunk_size=10):
    """Scale project in chunks to manage memory usage."""
    
    all_media = project.timeline.get_all_media()
    
    # Process media in chunks
    for i in range(0, len(all_media), chunk_size):
        chunk = all_media[i:i + chunk_size]
        
        for media in chunk:
            # Calculate scaling factor
            scale_x = target_resolution[0] / project.width
            scale_y = target_resolution[1] / project.height
            
            # Apply scaling
            media.scale_x *= scale_x
            media.scale_y *= scale_y
            
            # Update position
            media.x *= scale_x
            media.y *= scale_y
        
        # Force garbage collection after each chunk
        import gc
        gc.collect()
    
    # Update canvas last
    project.canvas.width = target_resolution[0]
    project.canvas.height = target_resolution[1]

# Use memory-efficient scaling for large projects
memory_efficient_scale(project, (1920, 1080))
```

### Parallel Scaling

```python
import concurrent.futures
from multiprocessing import Pool

def scale_single_project(args):
    """Scale a single project (for multiprocessing)."""
    project_path, target_resolution, output_dir = args
    
    try:
        project = Project(project_path)
        project.scale_to_resolution(*target_resolution)
        
        output_path = Path(output_dir) / Path(project_path).name
        project.save_as(output_path)
        
        return {"project": project_path, "status": "success"}
    except Exception as e:
        return {"project": project_path, "status": "error", "error": str(e)}

def parallel_batch_scale(project_paths, target_resolution, output_dir, max_workers=4):
    """Scale multiple projects in parallel."""
    
    # Prepare arguments for parallel processing
    args_list = [(path, target_resolution, output_dir) for path in project_paths]
    
    # Process in parallel
    with Pool(processes=max_workers) as pool:
        results = pool.map(scale_single_project, args_list)
    
    return results

# Scale projects in parallel
project_paths = list(Path("./projects").glob("*.cmproj"))
results = parallel_batch_scale(
    project_paths=project_paths,
    target_resolution=(1920, 1080),
    output_dir="./scaled_output",
    max_workers=4
)

# Report results
successful = [r for r in results if r["status"] == "success"]
failed = [r for r in results if r["status"] == "error"]

print(f"Successfully scaled: {len(successful)} projects")
print(f"Failed: {len(failed)} projects")
```

## Scaling Validation and Testing

### Automated Testing

```python
def test_scaling_operations():
    """Test various scaling operations for reliability."""
    test_results = []
    
    # Create test project
    test_project = Project.create_test_project()
    
    # Test different scaling operations
    test_cases = [
        {"operation": "scale_to_resolution", "args": (1920, 1080), "preserve_aspect": True},
        {"operation": "scale_content", "args": (1.5,)},
        {"operation": "scale_canvas", "args": (1280, 720)},
    ]
    
    for test_case in test_cases:
        try:
            project_copy = test_project.copy()
            
            # Apply scaling operation
            operation = getattr(project_copy, test_case["operation"])
            operation(*test_case["args"])
            
            # Validate result
            validation_result = project_copy.validate()
            
            test_results.append({
                "operation": test_case["operation"],
                "args": test_case["args"],
                "status": "pass" if validation_result.is_valid else "fail",
                "issues": validation_result.errors if not validation_result.is_valid else []
            })
            
        except Exception as e:
            test_results.append({
                "operation": test_case["operation"],
                "args": test_case["args"],
                "status": "error",
                "error": str(e)
            })
    
    return test_results

# Run scaling tests
test_results = test_scaling_operations()
for result in test_results:
    status_icon = "✓" if result["status"] == "pass" else "✗"
    print(f"{status_icon} {result['operation']}{result['args']}: {result['status']}")
```

## Next Steps

Continue exploring advanced Camtasio features:

- **[Batch Processing](batch-processing.md)** - Automating operations across multiple projects
- **[File Format Details](file-format.md)** - Deep dive into Camtasia file formats
- **[Quick Start](quickstart.md)** - Return to basic operations and examples