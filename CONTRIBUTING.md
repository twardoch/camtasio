# Contributing to Camtasio

This document explains how to contribute to Camtasio.

## Development Setup

### Prerequisites

- Python 3.11+
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

Code quality is enforced through:

- **Linting & Formatting**: `ruff`  
- **Type Checking**: `mypy` with strict mode
- **Testing**: `pytest` with coverage reporting
- **Dependency Management**: `uv`

### Before Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Run quality checks:
```bash
# Format code
uv run ruff format .

# Fix linting issues
uv run ruff check --fix .

# Type checking
uv run mypy src/

# Run tests
uv run pytest
```

### Making Changes

1. **Write Tests First**: Add tests before implementing new functionality.

2. **Follow Code Style**: 
   - Use type hints for all function parameters and return values
   - Write clear docstrings
   - Keep functions single-purpose
   - Use modern Python features (f-strings, pathlib, dataclasses, etc.)

3. **Add Documentation**: Update docstrings, README examples, and add usage examples for new features.

### Testing

Test coverage must stay above 80%. Run tests with:

```bash
# All tests
uv run pytest

# With coverage report
uv run pytest --cov=src/camtasio --cov-report=html

# Specific file
uv run pytest tests/test_models.py

# Pattern matching
uv run pytest -k "test_scaling"
```

### Test Categories

- **Unit Tests**: Functions and classes
- **Integration Tests**: Workflows and CLI commands
- **Edge Case Tests**: Error handling and boundaries
- **Performance Tests**: Execution time limits

### Code Quality Checks

Before submitting changes, run:

```bash
# Auto-format
uv run ruff format .

# Fix linting
uv run ruff check --fix --unsafe-fixes .

# Type checking
uv run mypy src/

# Test coverage
uv run pytest --cov=src/camtasio --cov-report=term-missing

# Coverage threshold
uv run pytest --cov=src/camtasio --cov-fail-under=80
```

## Submitting Changes

### Pull Request Process

1. **Update Documentation**: README, docstrings, CHANGELOG.

2. **Add Tests**: New code needs tests.

3. **Quality Checks**: All must pass:
   - All tests pass
   - Coverage >80%
   - Zero ruff violations
   - Zero mypy errors

4. **Create Pull Request**: 
   - Clear title
   - Reference issues
   - Describe changes
   - Include examples

### Pull Request Template

```markdown
## Description
What changed and why.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Coverage >80%

## Quality Checks
- [ ] Code formatted with ruff
- [ ] Linting passes
- [ ] Type checking passes
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

- **Separation of Concerns**: One responsibility per module
- **Immutable Data**: Prefer immutable dataclasses
- **Type Safety**: Strict type hints and mypy checking
- **Error Handling**: Clear error messages
- **Performance**: Efficient algorithms, low memory usage
- **Extensibility**: Plugin-friendly design

### Adding New Features

1. **Domain Models**: Add to `models/` with type hints and validation
2. **Operations**: Add to `operations/` 
3. **CLI Commands**: Add to `cli/app.py`
4. **Tests**: Cover normal use, edge cases, and errors

## Common Tasks

### Adding a New CLI Command

1. Add method to `CamtasioCLI` in `src/camtasio/cli/app.py`
2. Use `rich.console` for output
3. Handle errors with clear messages
4. Add tests to `tests/test_cli.py`
5. Update README.md command reference

### Adding a New Model

1. Create model in `src/camtasio/models/`
2. Use `@dataclass` with type hints
3. Implement `to_dict()` and `from_dict()` for serialization
4. Export in `models/__init__.py`
5. Export in main `__init__.py`
6. Add tests

### Fixing a Bug

1. Write test that reproduces the bug
2. Fix bug and ensure test passes
3. Add regression tests
4. Update CHANGELOG.md

## Release Process

Camtasio uses semantic versioning:

1. **Version Numbering**: `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
2. **Git Tags**: `git tag v1.2.3`
3. **Automatic Building**: hatch + hatch-vcs handles versioning
4. **Release Notes**: Update CHANGELOG.md

## Getting Help

- **Questions**: GitHub Discussion
- **Bug Reports**: GitHub Issue with steps to reproduce
- **Feature Requests**: GitHub Issue with description
- **Security Issues**: Email maintainers (see SECURITY.md)

## Code of Conduct

Be respectful. Be constructive. See CODE_OF_CONDUCT.md.

## Recognition

Contributors appear in CHANGELOG.md and GitHub's contributors list.