# File Format Details

Deep dive into Camtasia file formats, structure specifications, and low-level manipulation techniques.

## Camtasia Project File Structure

### Overview of File Formats

Camtasia projects use a combination of file formats to store project data and media assets:

```python
from camtasio import Project
from camtasio.serialization import JSONHandler, VersionHandler
import json

# Understanding project structure
project = Project("example.cmproj")

print("Project Structure:")
print(f"- Main file: project.tscproj (JSON)")
print(f"- Media directory: media/ (various formats)")
print(f"- Bookmarks: bookmarks.plist (XML)")
print(f"- Preferences: docPrefs (binary)")
print(f"- Cache files: *.cache (binary)")
```

### The .tscproj Format

The core project file is a JSON document with a specific schema:

```python
# Load and examine raw project data
def examine_tscproj_structure(project_path):
    """Examine the internal structure of a .tscproj file."""
    
    with open(project_path / "project.tscproj", "r", encoding="utf-8") as f:
        project_data = json.load(f)
    
    # Top-level structure
    print("Top-level keys in .tscproj:")
    for key in project_data.keys():
        print(f"  - {key}: {type(project_data[key]).__name__}")
    
    # Timeline structure
    if "timeline" in project_data:
        timeline = project_data["timeline"]
        print(f"\nTimeline structure:")
        print(f"  - Tracks: {len(timeline.get('sceneTrack', {}).get('scenes', []))}")
        print(f"  - Parameters: {len(timeline.get('parameters', []))}")
    
    # Media bin
    if "sourceBin" in project_data:
        source_bin = project_data["sourceBin"]
        print(f"\nSource bin:")
        print(f"  - Media items: {len(source_bin.get('sources', []))}")
    
    return project_data

# Examine project structure
project_data = examine_tscproj_structure(Path("example.cmproj"))
```

## JSON Schema and Validation

### Core Schema Elements

```python
from camtasio.serialization.schema import TSCProjSchema
import jsonschema

# Define core schema elements
TSCPROJ_SCHEMA = {
    "type": "object",
    "required": ["version", "timeline", "sourceBin"],
    "properties": {
        "version": {
            "type": "string",
            "pattern": r"^\d+\.\d+\.\d+$"
        },
        "timeline": {
            "type": "object",
            "required": ["sceneTrack", "parameters"],
            "properties": {
                "sceneTrack": {
                    "type": "object",
                    "properties": {
                        "scenes": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/scene"}
                        }
                    }
                },
                "parameters": {
                    "type": "object",
                    "properties": {
                        "width": {"type": "number"},
                        "height": {"type": "number"},
                        "framerate": {"type": "number"}
                    }
                }
            }
        },
        "sourceBin": {
            "type": "object",
            "properties": {
                "sources": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/source"}
                }
            }
        }
    },
    "definitions": {
        "scene": {
            "type": "object",
            "required": ["trackIndex", "medias"],
            "properties": {
                "trackIndex": {"type": "integer"},
                "medias": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/media"}
                }
            }
        },
        "media": {
            "type": "object",
            "required": ["start", "duration", "mediaType"],
            "properties": {
                "start": {"type": "number"},
                "duration": {"type": "number"},
                "mediaType": {"type": "string"},
                "src": {"type": "string"}
            }
        },
        "source": {
            "type": "object",
            "required": ["id", "src", "rect"],
            "properties": {
                "id": {"type": "string"},
                "src": {"type": "string"},
                "rect": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 4,
                    "maxItems": 4
                }
            }
        }
    }
}

# Validate project against schema
def validate_project_schema(project_data):
    """Validate project data against the schema."""
    try:
        jsonschema.validate(project_data, TSCPROJ_SCHEMA)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": [str(e)]}

# Use schema validation
validation_result = validate_project_schema(project_data)
if validation_result["valid"]:
    print("Project schema is valid")
else:
    print(f"Schema validation errors: {validation_result['errors']}")
```

### Custom Schema Extensions

```python
# Extend schema for custom properties
EXTENDED_SCHEMA = TSCPROJ_SCHEMA.copy()
EXTENDED_SCHEMA["properties"]["customMetadata"] = {
    "type": "object",
    "properties": {
        "projectId": {"type": "string"},
        "client": {"type": "string"},
        "version": {"type": "string"},
        "tags": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

# Custom media type definitions
EXTENDED_SCHEMA["definitions"]["media"]["properties"]["customProperties"] = {
    "type": "object",
    "additionalProperties": True
}
```

## Version Compatibility

### Version Detection and Handling

```python
from camtasio.serialization import VersionHandler

class VersionCompatibilityManager:
    """Manage compatibility across different Camtasia versions."""
    
    SUPPORTED_VERSIONS = {
        "9.0.0": "legacy",
        "9.1.0": "legacy", 
        "2018.0.0": "stable",
        "2019.0.0": "stable",
        "2020.0.0": "stable",
        "2021.0.0": "current",
        "2022.0.0": "current",
        "2023.0.0": "current",
        "2024.0.0": "current"
    }
    
    def __init__(self):
        self.version_handlers = {}
        self._register_handlers()
    
    def _register_handlers(self):
        """Register version-specific handlers."""
        self.version_handlers["legacy"] = self._handle_legacy_version
        self.version_handlers["stable"] = self._handle_stable_version
        self.version_handlers["current"] = self._handle_current_version
    
    def detect_version(self, project_data):
        """Detect project version from data."""
        version = project_data.get("version", "unknown")
        
        if version in self.SUPPORTED_VERSIONS:
            return version, self.SUPPORTED_VERSIONS[version]
        
        # Try to infer from structure
        if "timeline" in project_data and "sceneTrack" in project_data["timeline"]:
            if "scenes" in project_data["timeline"]["sceneTrack"]:
                return "inferred_current", "current"
            else:
                return "inferred_legacy", "legacy"
        
        return "unknown", "unknown"
    
    def _handle_legacy_version(self, project_data):
        """Handle legacy version compatibility."""
        # Convert old structure to new format
        if "tracks" in project_data:
            # Old format used "tracks" instead of "timeline.sceneTrack.scenes"
            tracks = project_data["tracks"]
            project_data["timeline"] = {
                "sceneTrack": {
                    "scenes": self._convert_tracks_to_scenes(tracks)
                },
                "parameters": project_data.get("parameters", {})
            }
            del project_data["tracks"]
        
        return project_data
    
    def _handle_stable_version(self, project_data):
        """Handle stable version compatibility."""
        # Minor adjustments for stable versions
        return project_data
    
    def _handle_current_version(self, project_data):
        """Handle current version (no conversion needed)."""
        return project_data
    
    def _convert_tracks_to_scenes(self, tracks):
        """Convert old track format to new scene format."""
        scenes = []
        for i, track in enumerate(tracks):
            scene = {
                "trackIndex": i,
                "medias": track.get("medias", []),
                "locked": track.get("locked", False),
                "visible": track.get("visible", True)
            }
            scenes.append(scene)
        return scenes
    
    def upgrade_project(self, project_data):
        """Upgrade project to current version."""
        version, version_type = self.detect_version(project_data)
        
        if version_type in self.version_handlers:
            upgraded_data = self.version_handlers[version_type](project_data)
            upgraded_data["version"] = max(
                v for v, t in self.SUPPORTED_VERSIONS.items() 
                if t == "current"
            )
            return upgraded_data
        
        raise ValueError(f"Unsupported version: {version}")

# Use version compatibility
version_manager = VersionCompatibilityManager()
upgraded_project = version_manager.upgrade_project(project_data)
```

### Migration Utilities

```python
def migrate_project_batch(project_paths, target_version="2024.0.0"):
    """Migrate multiple projects to target version."""
    
    migration_results = []
    version_manager = VersionCompatibilityManager()
    
    for project_path in project_paths:
        try:
            # Load project
            with open(project_path / "project.tscproj", "r") as f:
                project_data = json.load(f)
            
            # Detect current version
            current_version, version_type = version_manager.detect_version(project_data)
            
            if current_version == target_version:
                migration_results.append({
                    "project": project_path.name,
                    "status": "skipped",
                    "reason": "already_target_version"
                })
                continue
            
            # Create backup
            backup_path = project_path.parent / f"{project_path.stem}_backup_v{current_version}.cmproj"
            shutil.copytree(project_path, backup_path)
            
            # Upgrade project
            upgraded_data = version_manager.upgrade_project(project_data)
            
            # Save upgraded version
            with open(project_path / "project.tscproj", "w") as f:
                json.dump(upgraded_data, f, indent=2)
            
            migration_results.append({
                "project": project_path.name,
                "status": "success",
                "from_version": current_version,
                "to_version": target_version,
                "backup_path": str(backup_path)
            })
            
        except Exception as e:
            migration_results.append({
                "project": project_path.name,
                "status": "error",
                "error": str(e)
            })
    
    return migration_results
```

## Low-Level Data Manipulation

### Direct JSON Manipulation

```python
class LowLevelProjectEditor:
    """Direct manipulation of project JSON data."""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.data = None
        self.load()
    
    def load(self):
        """Load project data from file."""
        tscproj_path = self.project_path / "project.tscproj"
        with open(tscproj_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
    
    def save(self, backup=True):
        """Save project data to file."""
        if backup:
            self._create_backup()
        
        tscproj_path = self.project_path / "project.tscproj"
        with open(tscproj_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
    
    def _create_backup(self):
        """Create backup of original file."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"project_backup_{timestamp}.tscproj"
        backup_path = self.project_path / backup_name
        
        original_path = self.project_path / "project.tscproj"
        shutil.copy2(original_path, backup_path)
    
    def get_timeline_structure(self):
        """Get detailed timeline structure."""
        timeline = self.data.get("timeline", {})
        scene_track = timeline.get("sceneTrack", {})
        scenes = scene_track.get("scenes", [])
        
        structure = {
            "total_scenes": len(scenes),
            "scenes": []
        }
        
        for i, scene in enumerate(scenes):
            scene_info = {
                "index": i,
                "track_index": scene.get("trackIndex", 0),
                "media_count": len(scene.get("medias", [])),
                "medias": []
            }
            
            for media in scene.get("medias", []):
                media_info = {
                    "start": media.get("start", 0),
                    "duration": media.get("duration", 0),
                    "type": media.get("mediaType", "unknown"),
                    "source": media.get("src", "")
                }
                scene_info["medias"].append(media_info)
            
            structure["scenes"].append(scene_info)
        
        return structure
    
    def modify_media_timing(self, scene_index, media_index, new_start=None, new_duration=None):
        """Directly modify media timing."""
        scenes = self.data["timeline"]["sceneTrack"]["scenes"]
        
        if scene_index >= len(scenes):
            raise IndexError(f"Scene index {scene_index} out of range")
        
        medias = scenes[scene_index]["medias"]
        if media_index >= len(medias):
            raise IndexError(f"Media index {media_index} out of range")
        
        media = medias[media_index]
        
        if new_start is not None:
            media["start"] = new_start
        
        if new_duration is not None:
            media["duration"] = new_duration
    
    def add_custom_property(self, path, key, value):
        """Add custom property at specified path."""
        parts = path.split(".")
        current = self.data
        
        # Navigate to parent
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set value
        current[parts[-1]] = {key: value}
    
    def extract_media_references(self):
        """Extract all media file references."""
        references = []
        
        # Source bin references
        source_bin = self.data.get("sourceBin", {})
        for source in source_bin.get("sources", []):
            references.append({
                "type": "source",
                "id": source.get("id", ""),
                "path": source.get("src", ""),
                "rect": source.get("rect", [])
            })
        
        # Timeline media references
        timeline = self.data.get("timeline", {})
        scenes = timeline.get("sceneTrack", {}).get("scenes", [])
        
        for scene_idx, scene in enumerate(scenes):
            for media_idx, media in enumerate(scene.get("medias", [])):
                if "src" in media:
                    references.append({
                        "type": "timeline_media",
                        "scene_index": scene_idx,
                        "media_index": media_idx,
                        "path": media["src"],
                        "start": media.get("start", 0),
                        "duration": media.get("duration", 0)
                    })
        
        return references

# Use low-level editor
editor = LowLevelProjectEditor("example.cmproj")

# Examine structure
structure = editor.get_timeline_structure()
print(f"Project has {structure['total_scenes']} scenes")

# Modify timing
editor.modify_media_timing(0, 0, new_start=5.0, new_duration=10.0)

# Add custom metadata
editor.add_custom_property("customMetadata", "processing_version", "camtasio_1.0")

# Save changes
editor.save()
```

### Binary Format Handling

```python
import struct

class BinaryFormatHandler:
    """Handle binary formats in Camtasia projects."""
    
    def read_cache_file(self, cache_path):
        """Read binary cache file."""
        with open(cache_path, "rb") as f:
            # Read header
            header = f.read(16)
            magic, version, size, flags = struct.unpack("<4sIII", header)
            
            cache_data = {
                "magic": magic.decode("ascii"),
                "version": version,
                "size": size,
                "flags": flags,
                "entries": []
            }
            
            # Read entries
            while f.tell() < size:
                entry_header = f.read(8)
                if len(entry_header) < 8:
                    break
                
                entry_type, entry_size = struct.unpack("<II", entry_header)
                entry_data = f.read(entry_size)
                
                cache_data["entries"].append({
                    "type": entry_type,
                    "size": entry_size,
                    "data": entry_data
                })
            
            return cache_data
    
    def parse_doc_prefs(self, prefs_path):
        """Parse document preferences binary file."""
        preferences = {}
        
        with open(prefs_path, "rb") as f:
            # Simple key-value parsing (format varies by version)
            while True:
                # Read key length
                key_len_data = f.read(4)
                if len(key_len_data) < 4:
                    break
                
                key_len = struct.unpack("<I", key_len_data)[0]
                if key_len > 1000:  # Sanity check
                    break
                
                # Read key
                key = f.read(key_len).decode("utf-8", errors="ignore")
                
                # Read value length
                value_len_data = f.read(4)
                if len(value_len_data) < 4:
                    break
                
                value_len = struct.unpack("<I", value_len_data)[0]
                if value_len > 10000:  # Sanity check
                    break
                
                # Read value
                value_data = f.read(value_len)
                
                # Try to parse as different types
                try:
                    if value_len == 4:
                        value = struct.unpack("<I", value_data)[0]
                    elif value_len == 8:
                        value = struct.unpack("<d", value_data)[0]
                    else:
                        value = value_data.decode("utf-8", errors="ignore")
                except:
                    value = value_data.hex()
                
                preferences[key] = value
        
        return preferences

# Use binary format handler
binary_handler = BinaryFormatHandler()

# Read cache files if they exist
cache_files = list(Path("example.cmproj").glob("*.cache"))
for cache_file in cache_files:
    cache_data = binary_handler.read_cache_file(cache_file)
    print(f"Cache {cache_file.name}: {len(cache_data['entries'])} entries")

# Read document preferences
doc_prefs_path = Path("example.cmproj") / "docPrefs"
if doc_prefs_path.exists():
    prefs = binary_handler.parse_doc_prefs(doc_prefs_path)
    print(f"Document preferences: {len(prefs)} settings")
```

## Custom Format Extensions

### Creating Custom Media Types

```python
class CustomMediaType:
    """Define custom media type with specific properties."""
    
    def __init__(self, type_name, schema_extension):
        self.type_name = type_name
        self.schema = schema_extension
    
    def validate_media(self, media_data):
        """Validate media data against custom schema."""
        try:
            jsonschema.validate(media_data, self.schema)
            return True
        except jsonschema.ValidationError:
            return False
    
    def create_media_instance(self, **properties):
        """Create new media instance of this type."""
        media_data = {
            "mediaType": self.type_name,
            **properties
        }
        
        if self.validate_media(media_data):
            return media_data
        else:
            raise ValueError(f"Invalid properties for {self.type_name}")

# Define custom annotation type
annotation_schema = {
    "type": "object",
    "required": ["mediaType", "start", "duration", "annotationType"],
    "properties": {
        "mediaType": {"const": "customAnnotation"},
        "start": {"type": "number"},
        "duration": {"type": "number"},
        "annotationType": {
            "type": "string",
            "enum": ["highlight", "callout", "arrow", "shape"]
        },
        "properties": {
            "type": "object",
            "properties": {
                "color": {"type": "string"},
                "opacity": {"type": "number", "minimum": 0, "maximum": 1},
                "text": {"type": "string"},
                "position": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number"},
                        "y": {"type": "number"}
                    }
                }
            }
        }
    }
}

# Create custom media type
custom_annotation = CustomMediaType("customAnnotation", annotation_schema)

# Create instance
annotation_instance = custom_annotation.create_media_instance(
    start=5.0,
    duration=3.0,
    annotationType="callout",
    properties={
        "color": "#FF0000",
        "opacity": 0.8,
        "text": "Custom annotation",
        "position": {"x": 100, "y": 200}
    }
)
```

### Plugin System for Custom Formats

```python
class FormatPlugin:
    """Base class for format plugins."""
    
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
    def can_handle(self, file_path):
        """Check if plugin can handle the file."""
        raise NotImplementedError
    
    def read(self, file_path):
        """Read file and return data."""
        raise NotImplementedError
    
    def write(self, data, file_path):
        """Write data to file."""
        raise NotImplementedError

class CSVTimelinePlugin(FormatPlugin):
    """Plugin to export/import timeline as CSV."""
    
    def __init__(self):
        super().__init__("CSV Timeline", "1.0")
    
    def can_handle(self, file_path):
        return Path(file_path).suffix.lower() == ".csv"
    
    def read(self, file_path):
        """Import timeline from CSV."""
        import csv
        timeline_data = {"scenes": []}
        
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            current_scene = None
            
            for row in reader:
                scene_index = int(row["scene"])
                
                if current_scene is None or current_scene["trackIndex"] != scene_index:
                    current_scene = {
                        "trackIndex": scene_index,
                        "medias": []
                    }
                    timeline_data["scenes"].append(current_scene)
                
                media = {
                    "start": float(row["start"]),
                    "duration": float(row["duration"]),
                    "mediaType": row["type"],
                    "src": row["source"]
                }
                current_scene["medias"].append(media)
        
        return timeline_data
    
    def write(self, timeline_data, file_path):
        """Export timeline to CSV."""
        import csv
        
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["scene", "media", "start", "duration", "type", "source"])
            
            for scene in timeline_data.get("scenes", []):
                scene_index = scene.get("trackIndex", 0)
                
                for media_index, media in enumerate(scene.get("medias", [])):
                    writer.writerow([
                        scene_index,
                        media_index,
                        media.get("start", 0),
                        media.get("duration", 0),
                        media.get("mediaType", ""),
                        media.get("src", "")
                    ])

# Use plugin system
csv_plugin = CSVTimelinePlugin()

# Export timeline to CSV
timeline_data = editor.data["timeline"]["sceneTrack"]
csv_plugin.write(timeline_data, "timeline_export.csv")

# Import timeline from CSV
imported_timeline = csv_plugin.read("timeline_export.csv")
```

## Performance Optimization

### Efficient JSON Processing

```python
import orjson  # Fast JSON library

class OptimizedJSONHandler:
    """Optimized JSON handling for large projects."""
    
    @staticmethod
    def load_fast(file_path):
        """Load JSON using fastest available parser."""
        with open(file_path, "rb") as f:
            return orjson.loads(f.read())
    
    @staticmethod
    def save_fast(data, file_path, indent=2):
        """Save JSON using fastest available serializer."""
        options = orjson.OPT_INDENT_2 if indent else 0
        with open(file_path, "wb") as f:
            f.write(orjson.dumps(data, option=options))
    
    @staticmethod
    def stream_process_large_project(file_path, processor_func):
        """Process large project files in streaming fashion."""
        # For very large projects, process in chunks
        import ijson  # Streaming JSON parser
        
        with open(file_path, "rb") as f:
            # Stream parse specific sections
            scenes = ijson.items(f, "timeline.sceneTrack.scenes.item")
            
            for scene in scenes:
                processed_scene = processor_func(scene)
                yield processed_scene

# Example streaming processor
def optimize_scene(scene):
    """Optimize individual scene data."""
    # Remove unnecessary precision from timing values
    for media in scene.get("medias", []):
        if "start" in media:
            media["start"] = round(media["start"], 3)
        if "duration" in media:
            media["duration"] = round(media["duration"], 3)
    
    return scene

# Use optimized processing
optimized_handler = OptimizedJSONHandler()

# Fast loading
project_data = optimized_handler.load_fast("project.tscproj")

# Stream processing for large projects
processed_scenes = list(
    optimized_handler.stream_process_large_project(
        "large_project.tscproj",
        optimize_scene
    )
)
```

## Debugging and Validation Tools

### Project Integrity Checker

```python
class ProjectIntegrityChecker:
    """Comprehensive project file integrity checking."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def check_project(self, project_path):
        """Perform comprehensive integrity check."""
        self.issues = []
        self.warnings = []
        
        # Check file structure
        self._check_file_structure(project_path)
        
        # Check JSON validity
        self._check_json_validity(project_path)
        
        # Check media references
        self._check_media_references(project_path)
        
        # Check timeline consistency
        self._check_timeline_consistency(project_path)
        
        return {
            "issues": self.issues,
            "warnings": self.warnings,
            "is_valid": len(self.issues) == 0
        }
    
    def _check_file_structure(self, project_path):
        """Check basic file structure."""
        required_files = ["project.tscproj"]
        
        for required_file in required_files:
            file_path = project_path / required_file
            if not file_path.exists():
                self.issues.append(f"Missing required file: {required_file}")
    
    def _check_json_validity(self, project_path):
        """Check JSON file validity."""
        tscproj_path = project_path / "project.tscproj"
        
        try:
            with open(tscproj_path, "r") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.issues.append(f"Invalid JSON in project.tscproj: {e}")
        except Exception as e:
            self.issues.append(f"Cannot read project.tscproj: {e}")
    
    def _check_media_references(self, project_path):
        """Check media file references."""
        try:
            editor = LowLevelProjectEditor(project_path)
            references = editor.extract_media_references()
            
            for ref in references:
                media_path = Path(ref["path"])
                
                # Check if absolute path exists
                if media_path.is_absolute():
                    if not media_path.exists():
                        self.issues.append(f"Missing media file: {ref['path']}")
                else:
                    # Check relative to project
                    relative_path = project_path.parent / ref["path"]
                    if not relative_path.exists():
                        self.issues.append(f"Missing media file: {ref['path']}")
        
        except Exception as e:
            self.issues.append(f"Cannot check media references: {e}")
    
    def _check_timeline_consistency(self, project_path):
        """Check timeline logical consistency."""
        try:
            editor = LowLevelProjectEditor(project_path)
            structure = editor.get_timeline_structure()
            
            # Check for overlapping media
            for scene in structure["scenes"]:
                medias = scene["medias"]
                for i, media1 in enumerate(medias):
                    for j, media2 in enumerate(medias[i+1:], i+1):
                        # Check for overlap
                        m1_end = media1["start"] + media1["duration"]
                        m2_start = media2["start"]
                        m2_end = media2["start"] + media2["duration"]
                        
                        if (media1["start"] < m2_end and m1_end > m2_start):
                            self.warnings.append(
                                f"Overlapping media in scene {scene['index']}: "
                                f"media {i} and {j}"
                            )
        
        except Exception as e:
            self.issues.append(f"Cannot check timeline consistency: {e}")

# Use integrity checker
integrity_checker = ProjectIntegrityChecker()
check_result = integrity_checker.check_project(Path("example.cmproj"))

if check_result["is_valid"]:
    print("Project integrity check passed")
else:
    print(f"Found {len(check_result['issues'])} issues:")
    for issue in check_result["issues"]:
        print(f"  - {issue}")

if check_result["warnings"]:
    print(f"Found {len(check_result['warnings'])} warnings:")
    for warning in check_result["warnings"]:
        print(f"  - {warning}")
```

## Conclusion

Understanding the Camtasia file format in depth allows for:

- **Advanced Automation**: Create sophisticated batch processing workflows
- **Custom Tools**: Build specialized tools for specific use cases  
- **Integration**: Integrate Camtasia projects with other video production pipelines
- **Debugging**: Diagnose and fix project file issues
- **Extension**: Add custom functionality beyond standard Camtasio features

Continue exploring Camtasio's capabilities by returning to the practical guides:

- **[Quick Start](quickstart.md)** - Basic operations and examples
- **[Batch Processing](batch-processing.md)** - Automation workflows
- **[Scaling Operations](scaling-operations.md)** - Resolution management