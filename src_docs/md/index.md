# Camtasio Documentation

**Python toolkit for programmatically manipulating Camtasia project files**

## TLDR

Camtasio is a comprehensive Python library that enables developers to programmatically read, modify, and create Camtasia project files (`.cmproj` and `.tscproj` formats). Whether you need to batch-process projects, automate scaling operations, or integrate Camtasia workflows into larger applications, Camtasio provides the tools you need.

### Key Features

- 🎥 **Complete Project Manipulation** - Load, modify, and save Camtasia projects
- ⚡ **High-Performance Operations** - Efficient scaling, timeline editing, and media management
- 🔧 **Modern Python API** - Type-hinted, Pydantic-validated models with intuitive interfaces
- 📱 **CLI Tools** - Command-line utilities for common operations
- 🎨 **Effects & Annotations** - Full support for callouts, transitions, and visual effects
- 📊 **Batch Processing** - Process multiple projects efficiently

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

This documentation is organized into 9 comprehensive chapters:

### 📚 Table of Contents

| Chapter | Topic | Description |
|---------|-------|-------------|
| **1** | [Quick Start](quickstart.md) | Get up and running in minutes with essential examples |
| **2** | [Installation](installation.md) | Detailed installation guide and dependency management |
| **3** | [Project Basics](project-basics.md) | Core concepts for working with Camtasia projects |
| **4** | [Timeline Operations](timeline-operations.md) | Managing tracks, clips, and timeline structure |
| **5** | [Media Management](media-management.md) | Handling video, audio, and image assets |
| **6** | [Effects & Annotations](effects-annotations.md) | Working with callouts, transitions, and visual effects |
| **7** | [Scaling Operations](scaling-operations.md) | Advanced scaling and resolution management |
| **8** | [Batch Processing](batch-processing.md) | Efficient processing of multiple projects |
| **9** | [File Format Details](file-format.md) | Deep dive into `.tscproj` format specification |

---

## Quick Navigation

### Getting Started
- New to Camtasio? Start with the [Quick Start Guide](quickstart.md)
- Need to install? Check the [Installation Instructions](installation.md)

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

- **GitHub Repository**: [github.com/terragon/camtasio](https://github.com/terragon/camtasio)
- **PyPI Package**: [pypi.org/project/camtasio/](https://pypi.org/project/camtasio/)
- **Issues & Bug Reports**: Use GitHub Issues for support
- **Contributions**: See our contribution guidelines in the repository

---

*This documentation covers Camtasio v1.0+ - for legacy versions, see the migration guide in Chapter 1.*