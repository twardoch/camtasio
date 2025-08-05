# Batch Processing

Efficient automation techniques for processing multiple Camtasia projects with Camtasio.

## Introduction to Batch Processing

Batch processing allows you to apply operations to multiple projects automatically, saving time and ensuring consistency across your video library.

### Common Batch Operations

```python
from camtasio import Project
from camtasio.batch import BatchProcessor
from pathlib import Path
import concurrent.futures

# Initialize batch processor
processor = BatchProcessor()

# Common batch operations
operations = [
    "scale_to_resolution",
    "normalize_audio",
    "update_branding",
    "export_metadata",
    "validate_projects",
    "optimize_media_paths"
]

# Set up batch job
batch_job = processor.create_job(
    name="Monthly Video Update",
    source_directory="./projects",
    output_directory="./processed",
    operations=operations
)
```

## Setting Up Batch Operations

### Project Discovery

```python
def find_projects(directory, pattern="*.cmproj", recursive=True):
    """Find all Camtasia projects in a directory."""
    search_path = Path(directory)
    
    if recursive:
        projects = list(search_path.rglob(pattern))
    else:
        projects = list(search_path.glob(pattern))
    
    # Filter out incomplete projects
    valid_projects = []
    for project_path in projects:
        if (project_path / "project.tscproj").exists():
            valid_projects.append(project_path)
        else:
            print(f"Warning: {project_path} missing project.tscproj")
    
    return valid_projects

# Find all projects
project_paths = find_projects("./video_library", recursive=True)
print(f"Found {len(project_paths)} valid projects")
```

### Batch Configuration

```python
# Create batch configuration
batch_config = {
    "parallel_processing": True,
    "max_workers": 4,
    "backup_originals": True,
    "continue_on_error": True,
    "progress_reporting": True,
    "log_level": "INFO",
    "output_format": "preserve",  # or "standardize"
    "validation": {
        "pre_process": True,
        "post_process": True
    }
}

# Apply configuration to processor
processor.configure(batch_config)
```

## Scaling Operations

### Batch Resolution Standardization

```python
def batch_standardize_resolution(project_paths, target_resolution=(1920, 1080)):
    """Standardize resolution across multiple projects."""
    results = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            original_res = (project.width, project.height)
            
            # Skip if already at target resolution
            if original_res == target_resolution:
                results.append({
                    "project": project_path.name,
                    "status": "skipped",
                    "reason": "already_target_resolution"
                })
                continue
            
            # Scale project
            project.scale_to_resolution(*target_resolution, preserve_aspect=True)
            
            # Save with backup
            backup_path = project_path.parent / f"{project_path.stem}_backup.cmproj"
            project_path.rename(backup_path)
            project.save_as(project_path)
            
            results.append({
                "project": project_path.name,
                "status": "success",
                "original_resolution": original_res,
                "new_resolution": target_resolution,
                "backup_created": str(backup_path)
            })
            
        except Exception as e:
            results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return results

# Execute batch scaling
scaling_results = batch_standardize_resolution(project_paths)

# Report results
successful = [r for r in scaling_results if r["status"] == "success"]
print(f"Successfully scaled {len(successful)} projects to 1080p")
```

### Multi-Format Scaling

```python
def batch_multi_format_scaling(project_paths, format_specs):
    """Scale projects to multiple formats for different platforms."""
    
    format_definitions = {
        "youtube": {"resolution": (1920, 1080), "suffix": "_youtube"},
        "instagram": {"resolution": (1080, 1080), "suffix": "_instagram"},
        "tiktok": {"resolution": (1080, 1920), "suffix": "_tiktok"},
        "facebook": {"resolution": (1280, 720), "suffix": "_facebook"}
    }
    
    results = []
    
    for project_path in project_paths:
        project_results = {"project": project_path.name, "formats": {}}
        
        try:
            base_project = Project(project_path)
            
            for format_name in format_specs:
                if format_name in format_definitions:
                    format_def = format_definitions[format_name]
                    
                    # Create format-specific copy
                    format_project = base_project.copy()
                    format_project.scale_to_resolution(*format_def["resolution"])
                    
                    # Optimize for platform
                    format_project.optimize_for_platform(format_name)
                    
                    # Save with format suffix
                    output_name = f"{project_path.stem}{format_def['suffix']}.cmproj"
                    output_path = project_path.parent / output_name
                    format_project.save_as(output_path)
                    
                    project_results["formats"][format_name] = {
                        "status": "success",
                        "output_path": str(output_path),
                        "resolution": format_def["resolution"]
                    }
                else:
                    project_results["formats"][format_name] = {
                        "status": "error",
                        "error": f"Unknown format: {format_name}"
                    }
            
            results.append(project_results)
            
        except Exception as e:
            project_results["status"] = "error"
            project_results["error"] = str(e)
            results.append(project_results)
    
    return results

# Scale for multiple platforms
platforms = ["youtube", "instagram", "tiktok"]
multi_format_results = batch_multi_format_scaling(project_paths, platforms)
```

## Media Management Operations

### Batch Media Path Updates

```python
def batch_update_media_paths(project_paths, path_mappings):
    """Update media file paths across multiple projects."""
    
    results = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            updates_made = 0
            
            # Check each media item
            for media in project.source_medias:
                for old_path, new_path in path_mappings.items():
                    if old_path in str(media.src):
                        # Update path
                        updated_path = str(media.src).replace(old_path, new_path)
                        media.update_path(updated_path)
                        updates_made += 1
            
            if updates_made > 0:
                project.save()
                results.append({
                    "project": project_path.name,
                    "status": "success",
                    "updates_made": updates_made
                })
            else:
                results.append({
                    "project": project_path.name,
                    "status": "no_changes"
                })
                
        except Exception as e:
            results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return results

# Update media paths
path_updates = {
    "C:/old_media": "D:/new_media",
    "old_server": "new_server",
    "temp_audio": "final_audio"
}

path_update_results = batch_update_media_paths(project_paths, path_updates)
```

### Missing Media Detection and Reporting

```python
def batch_find_missing_media(project_paths, generate_report=True):
    """Find missing media files across multiple projects."""
    
    missing_media_report = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            missing_files = []
            
            for media in project.source_medias:
                if hasattr(media, 'src') and media.src:
                    media_path = Path(media.src)
                    if not media_path.exists() and not media_path.is_absolute():
                        # Try relative to project
                        relative_path = project_path.parent / media.src
                        if not relative_path.exists():
                            missing_files.append({
                                "media_name": media.name,
                                "expected_path": str(media.src),
                                "media_type": type(media).__name__
                            })
            
            if missing_files:
                missing_media_report.append({
                    "project": project_path.name,
                    "project_path": str(project_path),
                    "missing_count": len(missing_files),
                    "missing_files": missing_files
                })
                
        except Exception as e:
            missing_media_report.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    # Generate detailed report
    if generate_report:
        report_path = Path("missing_media_report.txt")
        with open(report_path, "w") as f:
            f.write("Missing Media Report\n")
            f.write("=" * 50 + "\n\n")
            
            for entry in missing_media_report:
                if "missing_files" in entry:
                    f.write(f"Project: {entry['project']}\n")
                    f.write(f"Path: {entry['project_path']}\n")
                    f.write(f"Missing files: {entry['missing_count']}\n")
                    for missing in entry["missing_files"]:
                        f.write(f"  - {missing['media_name']} ({missing['media_type']})\n")
                        f.write(f"    Expected: {missing['expected_path']}\n")
                    f.write("\n")
        
        print(f"Missing media report saved to: {report_path}")
    
    return missing_media_report

# Find missing media across all projects
missing_report = batch_find_missing_media(project_paths)
print(f"Found missing media in {len(missing_report)} projects")
```

## Audio Processing Operations

### Batch Audio Normalization

```python
def batch_normalize_audio(project_paths, target_level=-12.0, normalize_method="peak"):
    """Normalize audio levels across multiple projects."""
    
    results = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            audio_tracks = project.timeline.get_audio_tracks()
            
            if not audio_tracks:
                results.append({
                    "project": project_path.name,
                    "status": "skipped",
                    "reason": "no_audio_tracks"
                })
                continue
            
            # Normalize each audio track
            normalized_tracks = 0
            for track in audio_tracks:
                for media in track.medias:
                    if hasattr(media, 'normalize_audio'):
                        media.normalize_audio(
                            target_level=target_level,
                            method=normalize_method
                        )
                        normalized_tracks += 1
            
            if normalized_tracks > 0:
                project.save()
                results.append({
                    "project": project_path.name,
                    "status": "success",
                    "normalized_tracks": normalized_tracks,
                    "target_level": target_level
                })
            else:
                results.append({
                    "project": project_path.name,
                    "status": "no_changes"
                })
                
        except Exception as e:
            results.append({
                "project": project_path.name,
                "status": "error", 
                "error": str(e)
            })
    
    return results

# Normalize audio across projects
audio_results = batch_normalize_audio(project_paths, target_level=-12.0)
```

### Audio Quality Analysis

```python
def batch_analyze_audio_quality(project_paths):
    """Analyze audio quality across multiple projects."""
    
    analysis_results = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            audio_analysis = {
                "project": project_path.name,
                "tracks": []
            }
            
            for track in project.timeline.get_audio_tracks():
                track_analysis = {
                    "track_name": track.name,
                    "media_count": len(track.medias),
                    "issues": []
                }
                
                for media in track.medias:
                    # Check audio properties
                    if hasattr(media, 'sample_rate'):
                        if media.sample_rate < 44100:
                            track_analysis["issues"].append(f"Low sample rate: {media.sample_rate}Hz")
                    
                    if hasattr(media, 'peak_level'):
                        if media.peak_level > -3:
                            track_analysis["issues"].append(f"Possible clipping: {media.peak_level}dB")
                        elif media.peak_level < -30:
                            track_analysis["issues"].append(f"Very low level: {media.peak_level}dB")
                
                audio_analysis["tracks"].append(track_analysis)
            
            analysis_results.append(audio_analysis)
            
        except Exception as e:
            analysis_results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return analysis_results

# Analyze audio quality
audio_quality_analysis = batch_analyze_audio_quality(project_paths)

# Report issues
for analysis in audio_quality_analysis:
    if "tracks" in analysis:
        for track in analysis["tracks"]:
            if track["issues"]:
                print(f"{analysis['project']} - {track['track_name']}: {len(track['issues'])} issues")
```

## Branding and Consistency Operations

### Batch Branding Updates

```python
def batch_apply_branding(project_paths, branding_config):
    """Apply consistent branding across multiple projects."""
    
    results = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            branding_applied = []
            
            # Add logo watermark
            if "logo" in branding_config:
                logo_config = branding_config["logo"]
                logo = project.add_image_media(
                    path=logo_config["path"],
                    name="Brand Logo"
                )
                
                # Position logo
                logo.x = logo_config.get("x", project.width - 150)
                logo.y = logo_config.get("y", 50)
                logo.opacity = logo_config.get("opacity", 0.8)
                logo.duration = project.duration
                
                branding_applied.append("logo")
            
            # Add standard intro
            if "intro_template" in branding_config:
                intro_template = Project(branding_config["intro_template"])
                project.timeline.insert_template_at_start(intro_template)
                branding_applied.append("intro")
            
            # Add standard outro
            if "outro_template" in branding_config:
                outro_template = Project(branding_config["outro_template"])
                project.timeline.append_template(outro_template)
                branding_applied.append("outro")
            
            # Update color scheme
            if "colors" in branding_config:
                colors = branding_config["colors"]
                project.update_color_scheme(colors)
                branding_applied.append("colors")
            
            if branding_applied:
                project.save()
                results.append({
                    "project": project_path.name,
                    "status": "success",
                    "branding_applied": branding_applied
                })
            else:
                results.append({
                    "project": project_path.name,
                    "status": "no_changes"
                })
                
        except Exception as e:
            results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return results

# Apply branding
branding_config = {
    "logo": {
        "path": "./assets/company_logo.png",
        "x": 1720,
        "y": 50,
        "opacity": 0.7
    },
    "intro_template": "./templates/standard_intro.cmproj",
    "outro_template": "./templates/standard_outro.cmproj",
    "colors": {
        "primary": "#FF6600",
        "secondary": "#0066FF",
        "accent": "#FFCC00"
    }
}

branding_results = batch_apply_branding(project_paths, branding_config)
```

## Validation and Quality Control

### Comprehensive Project Validation

```python
def batch_validate_projects(project_paths, validation_rules):
    """Validate multiple projects against quality standards."""
    
    validation_results = []
    
    for project_path in project_paths:
        try:
            project = Project(project_path)
            project_validation = {
                "project": project_path.name,
                "passed": True,
                "issues": [],
                "warnings": []
            }
            
            # Check resolution standards
            if "min_resolution" in validation_rules:
                min_width, min_height = validation_rules["min_resolution"]
                if project.width < min_width or project.height < min_height:
                    project_validation["issues"].append(
                        f"Resolution below minimum: {project.width}x{project.height}"
                    )
                    project_validation["passed"] = False
            
            # Check duration limits
            if "duration_limits" in validation_rules:
                min_duration, max_duration = validation_rules["duration_limits"]
                if project.duration < min_duration:
                    project_validation["warnings"].append(
                        f"Duration below recommended: {project.duration}s"
                    )
                elif project.duration > max_duration:
                    project_validation["warnings"].append(
                        f"Duration above recommended: {project.duration}s"
                    )
            
            # Check audio levels
            if "audio_standards" in validation_rules:
                for track in project.timeline.get_audio_tracks():
                    for media in track.medias:
                        if hasattr(media, 'peak_level'):
                            if media.peak_level > validation_rules["audio_standards"]["max_peak"]:
                                project_validation["issues"].append(
                                    f"Audio clipping in {track.name}"
                                )
                                project_validation["passed"] = False
            
            # Check missing media
            missing_media = project.find_missing_media()
            if missing_media:
                project_validation["issues"].append(
                    f"Missing media files: {len(missing_media)}"
                )
                project_validation["passed"] = False
            
            validation_results.append(project_validation)
            
        except Exception as e:
            validation_results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return validation_results

# Validate projects
validation_rules = {
    "min_resolution": (1280, 720),
    "duration_limits": (30, 1800),  # 30 seconds to 30 minutes
    "audio_standards": {
        "max_peak": -3.0,
        "min_rms": -24.0
    }
}

validation_results = batch_validate_projects(project_paths, validation_rules)

# Report validation results
passed = [r for r in validation_results if r.get("passed", False)]
failed = [r for r in validation_results if not r.get("passed", True)]

print(f"Validation: {len(passed)} passed, {len(failed)} failed")
```

## Parallel Processing

### Multi-threaded Batch Operations

```python
import concurrent.futures
from threading import Lock

class ThreadSafeBatchProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.results_lock = Lock()
        self.results = []
    
    def process_project(self, project_path, operations):
        """Process a single project with given operations."""
        try:
            project = Project(project_path)
            operation_results = []
            
            for operation in operations:
                if operation["type"] == "scale":
                    project.scale_to_resolution(*operation["args"])
                    operation_results.append(f"Scaled to {operation['args']}")
                
                elif operation["type"] == "normalize_audio":
                    audio_tracks = project.timeline.get_audio_tracks()
                    for track in audio_tracks:
                        for media in track.medias:
                            if hasattr(media, 'normalize_audio'):
                                media.normalize_audio(operation["level"])
                    operation_results.append("Audio normalized")
                
                elif operation["type"] == "add_watermark":
                    watermark = project.add_image_media(operation["path"])
                    watermark.x = operation.get("x", project.width - 200)
                    watermark.y = operation.get("y", 50)
                    watermark.duration = project.duration
                    operation_results.append("Watermark added")
            
            # Save project
            project.save()
            
            # Thread-safe result storage
            with self.results_lock:
                self.results.append({
                    "project": project_path.name,
                    "status": "success",
                    "operations": operation_results
                })
            
        except Exception as e:
            with self.results_lock:
                self.results.append({
                    "project": project_path.name,
                    "status": "error",
                    "error": str(e)
                })
    
    def batch_process(self, project_paths, operations):
        """Process multiple projects in parallel."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            futures = [
                executor.submit(self.process_project, path, operations)
                for path in project_paths
            ]
            
            # Wait for completion
            concurrent.futures.wait(futures)
        
        return self.results

# Use parallel processing
processor = ThreadSafeBatchProcessor(max_workers=4)

operations = [
    {"type": "scale", "args": (1920, 1080)},
    {"type": "normalize_audio", "level": -12.0},
    {"type": "add_watermark", "path": "./logo.png", "x": 1720, "y": 50}
]

parallel_results = processor.batch_process(project_paths, operations)
print(f"Processed {len(parallel_results)} projects in parallel")
```

### Progress Monitoring

```python
from tqdm import tqdm
import time

def batch_process_with_progress(project_paths, operation_func, description="Processing"):
    """Process projects with progress bar."""
    
    results = []
    
    with tqdm(total=len(project_paths), desc=description) as pbar:
        for project_path in project_paths:
            start_time = time.time()
            
            try:
                result = operation_func(project_path)
                result["processing_time"] = time.time() - start_time
                results.append(result)
                
                # Update progress description
                pbar.set_postfix({
                    "current": project_path.name[:20],
                    "status": result.get("status", "unknown")
                })
                
            except Exception as e:
                results.append({
                    "project": project_path.name,
                    "status": "error",
                    "error": str(e),
                    "processing_time": time.time() - start_time
                })
            
            pbar.update(1)
    
    return results

# Example operation function
def scale_and_validate(project_path):
    project = Project(project_path)
    project.scale_to_resolution(1920, 1080)
    validation = project.validate()
    project.save()
    
    return {
        "project": project_path.name,
        "status": "success" if validation.is_valid else "warning",
        "resolution": (1920, 1080),
        "validation_issues": len(validation.errors) if not validation.is_valid else 0
    }

# Process with progress monitoring
progress_results = batch_process_with_progress(
    project_paths,
    scale_and_validate,
    description="Scaling projects"
)
```

## Reporting and Analysis

### Comprehensive Batch Report

```python
def generate_batch_report(all_results, output_path="batch_report.html"):
    """Generate comprehensive HTML report of batch operations."""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Camtasio Batch Processing Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .summary { background: #f0f0f0; padding: 15px; border-radius: 5px; }
            .success { color: green; }
            .error { color: red; }
            .warning { color: orange; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Camtasio Batch Processing Report</h1>
    """
    
    # Summary statistics
    total_projects = len(all_results)
    successful = len([r for r in all_results if r.get("status") == "success"])
    failed = len([r for r in all_results if r.get("status") == "error"])
    warnings = len([r for r in all_results if r.get("status") == "warning"])
    
    html_content += f"""
        <div class="summary">
            <h2>Summary</h2>
            <p>Total Projects: {total_projects}</p>
            <p class="success">Successful: {successful}</p>
            <p class="error">Failed: {failed}</p>
            <p class="warning">Warnings: {warnings}</p>
        </div>
        
        <h2>Detailed Results</h2>
        <table>
            <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Operations</th>
                <th>Issues</th>
            </tr>
    """
    
    # Detailed results
    for result in all_results:
        status_class = result.get("status", "unknown")
        operations = ", ".join(result.get("operations", []))
        issues = result.get("error", "") or ", ".join(result.get("issues", []))
        
        html_content += f"""
            <tr>
                <td>{result.get('project', 'Unknown')}</td>
                <td class="{status_class}">{status_class}</td>
                <td>{operations}</td>
                <td>{issues}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    # Save report
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Batch report saved to: {output_path}")

# Generate comprehensive report
all_batch_results = scaling_results + audio_results + branding_results
generate_batch_report(all_batch_results)
```

## Best Practices

### Error Handling and Recovery

```python
def robust_batch_processor(project_paths, operations, max_retries=3):
    """Robust batch processor with error handling and retry logic."""
    
    results = []
    failed_projects = []
    
    for project_path in project_paths:
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                # Attempt to process project
                project = Project(project_path)
                
                # Validate project before processing
                validation = project.validate()
                if not validation.is_valid:
                    raise ValueError(f"Project validation failed: {validation.errors}")
                
                # Apply operations
                for operation in operations:
                    getattr(project, operation["method"])(**operation.get("params", {}))
                
                # Save and validate result
                project.save()
                final_validation = project.validate()
                
                if final_validation.is_valid:
                    results.append({
                        "project": project_path.name,
                        "status": "success",
                        "retry_count": retry_count
                    })
                    success = True
                else:
                    raise ValueError("Post-processing validation failed")
                
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    failed_projects.append({
                        "project": project_path.name,
                        "status": "failed",
                        "error": str(e),
                        "retry_count": retry_count
                    })
                else:
                    print(f"Retry {retry_count}/{max_retries} for {project_path.name}")
                    time.sleep(1)  # Brief delay before retry
    
    return results + failed_projects

# Use robust processing
operations = [
    {"method": "scale_to_resolution", "params": {"width": 1920, "height": 1080}},
    {"method": "normalize_audio", "params": {"target_level": -12.0}}
]

robust_results = robust_batch_processor(project_paths, operations)
```

## Next Steps

You've now learned comprehensive batch processing techniques with Camtasio. Continue exploring:

- **[File Format Details](file-format.md)** - Deep dive into Camtasia file formats
- **[Quick Start](quickstart.md)** - Return to basic operations
- **[Installation](installation.md)** - Advanced setup and configuration