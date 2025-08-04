# Contributing to Camtasio

Thank you for your interest in contributing to Camtasio! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setting up the Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/camtasio.git
cd camtasio
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
uv sync
```

3. Install the package in development mode:
```bash
uv pip install -e .
```

4. Verify the installation:
```bash
camtasio version
```

## Development Workflow

### Code Quality Standards

We maintain high code quality standards using modern Python tooling:

- **Linting & Formatting**: `ruff` for fast linting and code formatting  
- **Type Checking**: `mypy` with strict mode enabled
- **Testing**: `pytest` with coverage reporting
- **Dependency Management**: `uv` for fast, reliable package management

### Before Making Changes

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Run the quality checks to ensure your environment is set up correctly:
```bash
# Format code
uv run ruff format .

# Check and fix linting issues
uv run ruff check --fix .

# Run type checking
uv run mypy src/

# Run tests
uv run pytest
```

### Making Changes

1. **Write Tests First**: We follow test-driven development. Write tests for new functionality before implementing it.

2. **Follow Code Style**: 
   - Use type hints for all function parameters and return values
   - Write clear, descriptive docstrings
   - Keep functions focused and single-purpose
   - Use modern Python features (f-strings, pathlib, dataclasses, etc.)

3. **Add Documentation**: Update docstrings, README examples, and add usage examples for new features.

### Testing

We maintain high test coverage (>80%) with comprehensive test suites:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/camtasio --cov-report=html

# Run specific test file
uv run pytest tests/test_models.py

# Run tests matching a pattern
uv run pytest -k "test_scaling"
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test complete workflows and CLI commands
- **Edge Case Tests**: Test error handling and boundary conditions
- **Performance Tests**: Ensure operations complete in reasonable time

### Code Quality Checks

Before submitting your changes, run the complete quality check suite:

```bash
# Auto-format code
uv run ruff format .

# Fix linting issues
uv run ruff check --fix --unsafe-fixes .

# Run type checking
uv run mypy src/

# Run tests with coverage
uv run pytest --cov=src/camtasio --cov-report=term-missing

# Ensure coverage is above 80%
uv run pytest --cov=src/camtasio --cov-fail-under=80
```

## Submitting Changes

### Pull Request Process

1. **Update Documentation**: Ensure README, docstrings, and CHANGELOG are updated.

2. **Add Tests**: All new code must have corresponding tests.

3. **Quality Checks**: Ensure all quality checks pass:
   - ✅ All tests pass
   - ✅ Coverage >80%
   - ✅ Zero ruff violations
   - ✅ Zero mypy errors

4. **Create Pull Request**: 
   - Use a clear, descriptive title
   - Reference any related issues
   - Provide a detailed description of changes
   - Include examples of new functionality

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Coverage remains above 80%

## Quality Checks
- [ ] Code formatted with ruff
- [ ] Linting passes with ruff
- [ ] Type checking passes with mypy
- [ ] Documentation updated

## Related Issues
Fixes #(issue number)
```

## Architecture Guidelines

### Package Structure

```
src/camtasio/
├── __init__.py           # Public API exports
├── cli/                  # Command-line interface
├── models/               # Domain models (Project, Timeline, etc.)
├── serialization/        # JSON loading/saving
├── transforms/           # Data transformation engine
├── operations/           # High-level operations
├── effects/              # Visual effects and annotations
├── utils/                # Utility functions
└── annotations/          # Callouts and text annotations
```

### Design Principles

- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Immutable Data**: Use dataclasses with immutable patterns where possible
- **Type Safety**: Comprehensive type hints and strict mypy checking
- **Error Handling**: Graceful error handling with informative messages
- **Performance**: Efficient algorithms and minimal memory usage
- **Extensibility**: Plugin-friendly architecture for future enhancements

### Adding New Features

1. **Domain Models**: Add new models to `models/` with proper type hints and validation
2. **Operations**: Add high-level operations to `operations/` that compose models and utilities
3. **CLI Commands**: Add new CLI commands to `cli/app.py` with proper error handling
4. **Tests**: Add comprehensive tests covering normal use, edge cases, and error conditions

## Common Tasks

### Adding a New CLI Command

1. Add the method to `CamtasioCLI` class in `src/camtasio/cli/app.py`
2. Use `rich.console` for beautiful output
3. Handle errors gracefully with helpful messages
4. Add comprehensive tests to `tests/test_cli.py`
5. Update the command reference table in README.md

### Adding a New Model

1. Create the model in `src/camtasio/models/`
2. Use `@dataclass` with type hints
3. Implement `to_dict()` and `from_dict()` methods for serialization
4. Add to `models/__init__.py` exports
5. Add to main `__init__.py` exports
6. Add comprehensive tests

### Fixing a Bug

1. Write a test that reproduces the bug
2. Fix the bug ensuring the test passes
3. Add regression tests to prevent the bug from reoccurring
4. Update CHANGELOG.md with the fix

## Release Process

Camtasio uses semantic versioning and automated releases:

1. **Version Numbering**: `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
2. **Git Tags**: Versions are determined by git tags (`git tag v1.2.3`)
3. **Automatic Building**: hatch + hatch-vcs handles version management
4. **Release Notes**: Update CHANGELOG.md for each release

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bug Reports**: Open a GitHub Issue with reproduction steps
- **Feature Requests**: Open a GitHub Issue with detailed description
- **Security Issues**: Email maintainers directly (see SECURITY.md)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## Recognition

All contributors are recognized in our CHANGELOG.md and GitHub contributors list. Thank you for helping make Camtasio better!