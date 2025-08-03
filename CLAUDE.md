# Camtasio Project Summary & Modernization Instructions

## 1. Executive Summary

Camtasio is a Python toolkit for programmatically manipulating Camtasia project files (`.cmproj` directories containing `.tscproj` JSON files). The codebase currently exists as two separate packages that need to be unified and modernized:

1. **Legacy `camtasia` package** (v6.3.0): Comprehensive object-oriented API using setup.py
2. **Modern `tscprojpy` package**: Focused CLI tool for scaling operations using pyproject.toml

The goal is to create a unified, modern Python package that combines the best of both approaches while adding new capabilities.

## 2. Current State Analysis

### 2.1. Strengths
- Comprehensive domain model coverage in legacy package
- Modern CLI implementation in tscprojpy
- Good understanding of .tscproj file format
- Existing test coverage
- Clear separation of concerns

### 2.2. Weaknesses
- Outdated packaging (setup.py vs pyproject.toml)
- No type hints in legacy code
- Duplicate functionality between packages
- Inconsistent coding styles
- Missing modern Python features
- Limited batch processing capabilities

## 3. Modernization Instructions

### 3.1. Package Structure Migration

**FROM** (Current scattered structure):
```
/src/camtasia/          # Legacy package
/ref/tscprojpy/         # Modern package
/setup.py               # Outdated
/setup.cfg              # Outdated
```

**TO** (Unified modern structure):
```
/src/camtasio/          # Single unified package
/pyproject.toml         # Modern packaging
/tests/                 # Comprehensive tests
/docs/                  # Unified documentation
```

### 3.2. Build System Modernization

Replace setup.py/setup.cfg with modern pyproject.toml:

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "camtasio"
dynamic = ["version"]
description = "Python API and CLI for Camtasia projects"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
dependencies = [
    "pydantic>=2.0",
    "click>=8.0",
    "fire>=0.5",
    "rich>=13.0",
    "loguru>=0.7",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff>=0.1",
    "mypy>=1.0",
    "uv>=0.1",
]

[project.scripts]
camtasio = "camtasio.cli.app:main"

[tool.hatch.version]
source = "vcs"

[tool.ruff]
target-version = "py38"
line-length = 100
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "PT", "SIM"]

[tool.mypy]
python_version = "3.8"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### 3.3. Code Integration Strategy

#### 3.3.1. Step 1: Create Base Infrastructure
```python
# src/camtasio/__init__.py
"""Camtasio - Python toolkit for Camtasia projects."""
# this_file: src/camtasio/__init__.py

from camtasio.project import Project
from camtasio.models import Timeline, Track, Clip
from camtasio.operations import scale_project, timescale_project

__version__ = "1.0.0"
__all__ = ["Project", "Timeline", "Track", "Clip", "scale_project", "timescale_project"]
```

#### 3.3.2. Step 2: Merge Domain Models
Combine the best aspects of both packages:
- Use object-oriented models from legacy package
- Add pydantic validation from modern approach
- Implement comprehensive type hints

```python
# src/camtasio/models/timeline.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Timeline(BaseModel):
    """Represents a Camtasia timeline."""
    id: str
    tracks: List[Track] = Field(default_factory=list)
    duration: float = 0.0
    markers: List[Marker] = Field(default_factory=list)
    
    def add_track(self, track: Track) -> None:
        """Add a track to the timeline."""
        self.tracks.append(track)
```

#### 3.3.3. Step 3: Unify Operations
Create a unified operations module combining both approaches:

```python
# src/camtasio/operations/scaler.py
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class ProjectScaler:
    """Handles spatial scaling of Camtasia projects."""
    
    def __init__(self, preserve_aspect: bool = True):
        self.preserve_aspect = preserve_aspect
        
    def scale(self, project_data: Dict[str, Any], 
              target_width: int, target_height: int) -> Dict[str, Any]:
        """Scale project to target dimensions."""
        # Implementation combining both scaling approaches
        pass
```

### 3.4. CLI Unification

Create a unified CLI combining commands from both packages:

```python
# src/camtasio/cli/app.py
import fire
from rich.console import Console
from camtasio import Project

console = Console()

class CamtasioCLI:
    """Camtasio command-line interface."""
    
    def info(self, project_path: str):
        """Display project information."""
        project = Project(project_path)
        console.print(f"[bold]Project:[/] {project.name}")
        console.print(f"[bold]Duration:[/] {project.duration}s")
        console.print(f"[bold]Resolution:[/] {project.width}x{project.height}")
    
    def scale(self, project_path: str, width: int, height: int):
        """Scale project to new dimensions."""
        project = Project(project_path)
        project.scale(width, height)
        project.save()
        console.print(f"[green]✓[/] Scaled to {width}x{height}")

def main():
    fire.Fire(CamtasioCLI)
```

### 3.5. Type Hints Implementation

Add comprehensive type hints throughout:

```python
from __future__ import annotations
from typing import List, Optional, Dict, Any, Union, Tuple
from pathlib import Path

def load_project(path: Union[str, Path]) -> Dict[str, Any]:
    """Load a Camtasia project from disk."""
    project_path = Path(path)
    if project_path.suffix == '.cmproj':
        tscproj_path = project_path / 'project.tscproj'
    else:
        tscproj_path = project_path
    
    with open(tscproj_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### 3.6. Testing Strategy

Implement comprehensive testing:

```python
# tests/test_project.py
import pytest
from pathlib import Path
from camtasio import Project

@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    """Create a sample project for testing."""
    project_dir = tmp_path / "test.cmproj"
    project_dir.mkdir()
    # Create test project structure
    return project_dir

def test_project_loading(sample_project: Path):
    """Test project loading functionality."""
    project = Project(sample_project)
    assert project.name == "test"
    assert project.width == 1920
    assert project.height == 1080
```

### 3.7. Migration Path

For users of the legacy package:

```python
# src/camtasio/legacy.py
"""Backward compatibility layer."""
import warnings

def deprecated_function():
    warnings.warn(
        "This function is deprecated. Use camtasio.new_function instead.",
        DeprecationWarning,
        stacklevel=2
    )
    # Forward to new implementation
```

### 3.8. Performance Optimizations

Key areas to optimize:
1. **JSON parsing**: Use orjson for faster parsing
2. **File I/O**: Implement streaming for large files
3. **Scaling operations**: Use numpy for mathematical operations
4. **Caching**: Cache parsed projects in memory

### 3.9. Documentation Requirements

Create comprehensive documentation:
1. **API Reference**: Auto-generated from docstrings
2. **User Guide**: Step-by-step tutorials
3. **CLI Reference**: Command documentation
4. **Migration Guide**: For legacy users
5. **Format Specification**: Detailed .tscproj format docs

### 3.10. Quality Standards

Enforce quality through tooling:
- **Ruff**: Linting and formatting
- **Mypy**: Static type checking
- **Pytest**: Unit and integration testing
- **Coverage**: Minimum 90% code coverage
- **Pre-commit**: Automated checks

## 4. Implementation Priority

1. **Critical** (Week 1):
   - Set up modern packaging
   - Create unified structure
   - Implement core functionality

2. **Important** (Week 2-3):
   - Add type hints
   - Merge operations
   - Create unified CLI

3. **Nice to Have** (Week 4+):
   - Advanced features
   - Performance optimizations
   - Extended documentation

## 5. Success Metrics

- All tests passing with >90% coverage
- Zero mypy errors with strict mode
- Ruff compliance with selected rules
- Successful PyPI publication
- Positive user feedback

This modernization will transform Camtasio into a professional, maintainable toolkit that serves as the definitive Python solution for Camtasia project manipulation.

# Software Development Rules

## 6. Pre-Work Preparation

### 6.1. Before Starting Any Work
- **ALWAYS** read `WORK.md` in the main project folder for work progress
- Read `README.md` to understand the project
- STEP BACK and THINK HEAVILY STEP BY STEP about the task
- Consider alternatives and carefully choose the best option
- Check for existing solutions in the codebase before starting

### 6.2. Project Documentation to Maintain
- `README.md` - purpose and functionality
- `CHANGELOG.md` - past change release notes (accumulative)
- `PLAN.md` - detailed future goals, clear plan that discusses specifics
- `TODO.md` - flat simplified itemized `- [ ]`-prefixed representation of `PLAN.md`
- `WORK.md` - work progress updates

## 7. General Coding Principles

### 7.1. Core Development Approach
- Iterate gradually, avoiding major changes
- Focus on minimal viable increments and ship early
- Minimize confirmations and checks
- Preserve existing code/structure unless necessary
- Check often the coherence of the code you're writing with the rest of the code
- Analyze code line-by-line

### 7.2. Code Quality Standards
- Use constants over magic numbers
- Write explanatory docstrings/comments that explain what and WHY
- Explain where and how the code is used/referred to elsewhere
- Handle failures gracefully with retries, fallbacks, user guidance
- Address edge cases, validate assumptions, catch errors early
- Let the computer do the work, minimize user decisions
- Reduce cognitive load, beautify code
- Modularize repeated logic into concise, single-purpose functions
- Favor flat over nested structures

## 8. Tool Usage (When Available)

### 8.1. Additional Tools
- If we need a new Python project, run `curl -LsSf https://astral.sh/uv/install.sh | sh; uv venv --python 3.12; uv init; uv add fire rich; uv sync`
- Use `tree` CLI app if available to verify file locations
- Check existing code with `.venv` folder to scan and consult dependency source code
- Run `DIR="."; uvx codetoprompt --compress --output "$DIR/llms.txt"  --respect-gitignore --cxml --exclude "*.svg,.specstory,*.md,*.txt,ref,testdata,*.lock,*.svg" "$DIR"` to get a condensed snapshot of the codebase into `llms.txt`

## 9. File Management

### 9.1. File Path Tracking
- **MANDATORY**: In every source file, maintain a `this_file` record showing the path relative to project root
- Place `this_file` record near the top:
- As a comment after shebangs in code files
- In YAML frontmatter for Markdown files
- Update paths when moving files
- Omit leading `./`
- Check `this_file` to confirm you're editing the right file

## 10. Python-Specific Guidelines

### 10.1. PEP Standards
- PEP 8: Use consistent formatting and naming, clear descriptive names
- PEP 20: Keep code simple and explicit, prioritize readability over cleverness
- PEP 257: Write clear, imperative docstrings
- Use type hints in their simplest form (list, dict, | for unions)

### 10.2. Modern Python Practices
- Use f-strings and structural pattern matching where appropriate
- Write modern code with `pathlib`
- ALWAYS add "verbose" mode loguru-based logging & debug-log
- Use `uv add` 
- Use `uv pip install` instead of `pip install`
- Prefix Python CLI tools with `python -m` (e.g., `python -m pytest`)

### 10.3. CLI Scripts Setup
For CLI Python scripts, use `fire` & `rich`, and start with:
```python
#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["PKG1", "PKG2"]
# ///
# this_file: PATH_TO_CURRENT_FILE
```

### 10.4. Post-Edit Python Commands
```bash
fd -e py -x uvx autoflake -i {}; fd -e py -x uvx pyupgrade --py312-plus {}; fd -e py -x uvx ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x uvx ruff format --respect-gitignore --target-version py312 {}; python -m pytest;
```

## 11. Post-Work Activities

### 11.1. Critical Reflection
- After completing a step, say "Wait, but" and do additional careful critical reasoning
- Go back, think & reflect, revise & improve what you've done
- Don't invent functionality freely
- Stick to the goal of "minimal viable next version"

### 11.2. Documentation Updates
- Update `WORK.md` with what you've done and what needs to be done next
- Document all changes in `CHANGELOG.md`
- Update `TODO.md` and `PLAN.md` accordingly

## 12. Work Methodology

### 12.1. Virtual Team Approach
Be creative, diligent, critical, relentless & funny! Lead two experts:
- **"Ideot"** - for creative, unorthodox ideas
- **"Critin"** - to critique flawed thinking and moderate for balanced discussions

Collaborate step-by-step, sharing thoughts and adapting. If errors are found, step back and focus on accuracy and progress.

### 12.2. Continuous Work Mode
- Treat all items in `PLAN.md` and `TODO.md` as one huge TASK
- Work on implementing the next item
- Review, reflect, refine, revise your implementation
- Periodically check off completed issues
- Continue to the next item without interruption

## 13. Special Commands

### 13.1. `/plan` Command - Transform Requirements into Detailed Plans

When I say "/plan [requirement]", you must:

1. **DECONSTRUCT** the requirement:
- Extract core intent, key features, and objectives
- Identify technical requirements and constraints
- Map what's explicitly stated vs. what's implied
- Determine success criteria

2. **DIAGNOSE** the project needs:
- Audit for missing specifications
- Check technical feasibility
- Assess complexity and dependencies
- Identify potential challenges

3. **RESEARCH** additional material: 
- Repeatedly call the `perplexity_ask` and request up-to-date information or additional remote context
- Repeatedly call the `context7` tool and request up-to-date software package documentation
- Repeatedly call the `codex` tool and request additional reasoning, summarization of files and second opinion

4. **DEVELOP** the plan structure:
- Break down into logical phases/milestones
- Create hierarchical task decomposition
- Assign priorities and dependencies
- Add implementation details and technical specs
- Include edge cases and error handling
- Define testing and validation steps

5. **DELIVER** to `PLAN.md`:
- Write a comprehensive, detailed plan with:
 - Project overview and objectives
 - Technical architecture decisions
 - Phase-by-phase breakdown
 - Specific implementation steps
 - Testing and validation criteria
 - Future considerations
- Simultaneously create/update `TODO.md` with the flat itemized `- [ ]` representation

**Plan Optimization Techniques:**
- **Task Decomposition:** Break complex requirements into atomic, actionable tasks
- **Dependency Mapping:** Identify and document task dependencies
- **Risk Assessment:** Include potential blockers and mitigation strategies
- **Progressive Enhancement:** Start with MVP, then layer improvements
- **Technical Specifications:** Include specific technologies, patterns, and approaches

### 13.2. `/report` Command

1. Read all `./TODO.md` and `./PLAN.md` files
2. Analyze recent changes
3. Document all changes in `./CHANGELOG.md`
4. Remove completed items from `./TODO.md` and `./PLAN.md`
5. Ensure `./PLAN.md` contains detailed, clear plans with specifics
6. Ensure `./TODO.md` is a flat simplified itemized representation

### 13.3. `/work` Command

1. Read all `./TODO.md` and `./PLAN.md` files and reflect
2. Write down the immediate items in this iteration into `./WORK.md`
3. Work on these items
4. Think, contemplate, research, reflect, refine, revise
5. Be careful, curious, vigilant, energetic
6. Verify your changes and think aloud
7. Consult, research, reflect
8. Periodically remove completed items from `./WORK.md`
9. Tick off completed items from `./TODO.md` and `./PLAN.md`
10. Update `./WORK.md` with improvement tasks
11. Execute `/report`
12. Continue to the next item

## 14. Additional Guidelines

- Ask before extending/refactoring existing code that may add complexity or break things
- Work tirelessly without constant updates when in continuous work mode
- Only notify when you've completed all `PLAN.md` and `TODO.md` items

## 15. Command Summary

- `/plan [requirement]` - Transform vague requirements into detailed `PLAN.md` and `TODO.md`
- `/report` - Update documentation and clean up completed tasks
- `/work` - Enter continuous work mode to implement plans
- You may use these commands autonomously when appropriate

