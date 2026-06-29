# Installation Guide

Install Camtasio in any environment.

## Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, Linux
- **Dependencies**: See `pyproject.toml` for the full list

### Core Dependencies

- `pydantic >= 2.0` – Data validation and serialization  
- `click >= 8.0` – Command-line interface framework  
- `fire >= 0.5` – Alternative CLI framework  
- `rich >= 13.0` – Rich terminal output  
- `loguru >= 0.7` – Advanced logging  

## Installation Methods

### Standard Installation (pip)

```bash
# Latest stable version
pip install camtasio

# Specific version
pip install camtasio==1.0.0

# With development dependencies
pip install camtasio[dev]
```

### Modern Installation (uv) – Recommended

```bash
# Install uv first (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add camtasio to your project
uv add camtasio

# With development dependencies
uv add camtasio[dev]

# Global installation
uv tool install camtasio
```

### Development Installation

For contributors or early adopters:

```bash
# Clone the repository
git clone https://github.com/twardoch/camtasio.git
cd camtasio

# Install in development mode with uv
uv venv
uv sync --all-extras

# Or with pip
pip install -e .[dev]
```

### Container Installation

#### Docker

```dockerfile
FROM python:3.11-slim

# Install uv
RUN pip install uv

# Install camtasio
RUN uv pip install camtasio

# Your application code
COPY . /app
WORKDIR /app
```

#### Dev Container (VS Code)

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "Camtasio Development",
  "image": "python:3.11",
  "features": {
    "ghcr.io/astral-sh/uv-features/uv:latest": {}
  },
  "postCreateCommand": "uv pip install camtasio[dev]",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.mypy-type-checker",
        "charliermarsh.ruff"
      ]
    }
  }
}
```

## Platform-Specific Instructions

### Windows

```powershell
# Using pip
pip install camtasio

# Using uv (install via PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
uv tool install camtasio
```

**Notes:**
- Make sure Python is in your PATH.
- Use Windows Terminal for a better CLI experience.
- Quote file paths with spaces.

### macOS

```bash
# Using Homebrew (recommended for uv)
brew install uv
uv tool install camtasio

# Or using pip
pip3 install camtasio
```

**Notes:**
- Use `pip3` if you have both Python 2 and 3 installed.
- Consider using pyenv for managing Python versions.

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip
pip3 install camtasio

# Or using uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install camtasio

# Fedora/RHEL
sudo dnf install python3-pip
pip3 install camtasio
```

**Notes:**
- Some systems require `python3-dev` for certain dependencies.
- Use your package manager to install Python when possible.

## Virtual Environment Setup

### Using venv (Built-in)

```bash
# Create virtual environment
python -m venv camtasio-env

# Activate (Linux/macOS)
source camtasio-env/bin/activate

# Activate (Windows)
camtasio-env\Scripts\activate

# Install camtasio
pip install camtasio
```

### Using uv (Modern Approach)

```bash
# Create and activate virtual environment
uv venv camtasio-env
source camtasio-env/bin/activate  # Linux/macOS
# or: camtasio-env\Scripts\activate  # Windows

# Install camtasio
uv pip install camtasio
```

### Using conda

```bash
# Create conda environment
conda create -n camtasio python=3.11
conda activate camtasio

# Install via pip (not on conda-forge yet)
pip install camtasio
```

## Verification

Check that installation worked:

```bash
# Check CLI installation
camtasio --version

# Test Python import
python -c "import camtasio; print(camtasio.__version__)"

# Run basic functionality test
python -c "
from camtasio.models import Project
print('Camtasio installed successfully!')
"
```

## Optional Dependencies

### Performance Optimizations

```bash
# Fast JSON parsing
uv add orjson

# Numerical operations
uv add numpy

# Image processing
uv add pillow
```

### Development Tools

```bash
# Full development environment
uv add camtasio[dev]

# Individual tools
uv add pytest pytest-cov mypy ruff pre-commit
```

### Documentation Building

```bash
# MkDocs with Material theme
uv add mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin
```

## Configuration

### CLI Configuration

Create `~/.camtasio/config.yaml`:

```yaml
# Default output directory
output_dir: "./processed"

# Default scaling options
scaling:
  preserve_aspect: true
  interpolation: "lanczos"

# Logging level
log_level: "INFO"

# Default project settings
projects:
  backup_on_save: true
  validate_on_load: true
```

### Environment Variables

```bash
# Set default project directory
export CAMTASIO_PROJECT_DIR="/path/to/projects"

# Enable debug logging
export CAMTASIO_LOG_LEVEL="DEBUG"

# Configure temp directory
export CAMTASIO_TEMP_DIR="/tmp/camtasio"
```

## Troubleshooting

### Common Installation Issues

#### "No module named 'camtasio'"

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall in current environment
pip uninstall camtasio
pip install camtasio
```

#### Permission Errors (Linux/macOS)

```bash
# Install to user directory
pip install --user camtasio

# Or use uv (recommended)
uv tool install camtasio
```

#### Version Conflicts

```bash
# Check installed version
pip show camtasio

# Force upgrade
pip install --upgrade --force-reinstall camtasio

# Clean installation
pip uninstall camtasio
pip cache purge
pip install camtasio
```

### Platform-Specific Issues

#### Windows: "Python not found"

1. Install Python from python.org  
2. Check "Add to PATH" during setup  
3. Restart your terminal  

#### macOS: SSL Certificate Errors

```bash
# Update certificates
/Applications/Python\ 3.11/Install\ Certificates.command
```

#### Linux: Missing Development Headers

```bash
# Ubuntu/Debian
sudo apt install python3-dev

# Fedora/RHEL
sudo dnf install python3-devel
```

## Performance Tuning

### Memory Usage

For large projects or batch processing:

```python
import os

# Limit memory usage
os.environ['CAMTASIO_MAX_MEMORY'] = '2GB'

# Enable streaming mode for large files
os.environ['CAMTASIO_STREAMING'] = 'true'
```

### CPU Usage

```python
# Set number of worker processes
os.environ['CAMTASIO_WORKERS'] = '4'

# Enable multiprocessing for batch operations
from camtasio.batch import BatchProcessor
processor = BatchProcessor(workers=4)
```

## IDE Integration

### VS Code

Install these extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.mypy-type-checker", 
    "charliermarsh.ruff",
    "ms-python.debugpy"
  ]
}
```

### PyCharm

1. Set up a Python interpreter pointing to your virtual environment  
2. Install Camtasio in that interpreter  
3. Mark the `src` directory as Sources Root  

## Next Steps

- **[Quick Start](quickstart.md)** – Begin with basic operations  
- **[Project Basics](project-basics.md)** – Understand core concepts  
- **[CLI Reference](../cli-reference.md)** – Full command documentation  

## Getting Help

- **GitHub Issues** – Report bugs or suggest features  
- **Documentation** – Read everything else  
- **Community** – Join discussions on GitHub