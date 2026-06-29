# Camtasio Documentation

**Python toolkit for programmatically manipulating Camtasia project files**

## TLDR

Camtasio is a Python library that reads, modifies, and creates Camtasia project files (`.cmproj` and `.tscproj`). It's useful for batch-processing projects, automating edits, or integrating Camtasia into larger workflows.

### Key Features

- 🎥 Load, modify, and save Camtasia projects  
- ⚡ Efficient operations: scaling, timeline editing, media management  
- 🔧 Clean Python API with type hints and data validation  
- 📱 CLI tools for common tasks  
- 🎨 Support for annotations, transitions, and visual effects  
- 📊 Batch process multiple projects  

### Quick Example

```python
from camtasio import Project

# Load a Camtasia project
project = Project("my_video.cmproj")

# Scale to 1080p
project.scale_to_resolution(1920, 1080)

# Add a callout annotation
project.timeline.add_callout("Important note!", x=100, y=200, duration=3.0)

# Save the modified project
project.save()
```

## Documentation Structure

This documentation has 9 chapters:

### 📚 Table of Contents

| Chapter | Topic | Description |
|---------|-------|-------------|
| **1** | [Quick Start](quickstart.md) | Essential examples to get going fast |
| **2** | [Installation](installation.md) | How to install and manage dependencies |
| **3** | [Project Basics](project-basics.md) | Core concepts for working with projects |
| **4** | [Timeline Operations](timeline-operations.md) | Tracks, clips, and timeline structure |
| **5** | [Media Management](media-management.md) | Video, audio, and image assets |
| **6** | [Effects & Annotations](effects-annotations.md) | Callouts, transitions, visual effects |
| **7** | [Scaling Operations](scaling-operations.md) | Resolution changes and canvas adjustments |
| **8** | [Batch Processing](batch-processing.md) | Handle many projects at once |
| **9** | [File Format Details](file-format.md) | Inside the `.tscproj` file format |

---

## Quick Navigation

### Getting Started
- [Quick Start Guide](quickstart.md)
- [Installation Instructions](installation.md)

### Common Tasks
- **Project Management**: [Project Basics](project-basics.md)  
- **Timeline Editing**: [Timeline Operations](timeline-operations.md)  
- **Asset Handling**: [Media Management](media-management.md)  
- **Visual Elements**: [Effects & Annotations](effects-annotations.md)  

### Advanced Usage
- **Resolution Changes**: [Scaling Operations](scaling-operations.md)  
- **Automation**: [Batch Processing](batch-processing.md)  
- **Format Details**: [File Format Specification](file-format.md)  

---

## Community & Support

- **GitHub Repository**: [github.com/twardoch/camtasio](https://github.com/twardoch/camtasio)  
- **PyPI Package**: [pypi.org/project/camtasio/](https://pypi.org/project/camtasio/)  
- **Issues & Bug Reports**: Use GitHub Issues  
- **Contributions**: See contribution guidelines in the repo  

---

*Documentation applies to Camtasio v1.0+. For older versions, check the migration guide in Chapter 1.*