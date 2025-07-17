# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

perprof-py is a Python package for generating performance profiles as described by Dolan and Moré. It creates visualizations comparing the performance of different solvers/algorithms using TikZ, matplotlib, or Bokeh backends.

## Development Setup

### Installation
This project uses uv for dependency management. Install uv if not already available:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync --extra dev
```

### Required System Dependencies
For full functionality (TikZ backend), install TeX dependencies:
```bash
sudo apt-get install texlive-pictures texlive-fonts-recommended texlive-latex-extra
```

## Common Development Commands

### Testing
- Run all tests: `uv run pytest -v`
- Run tests with coverage: `uv run pytest -v --cov`
- Run single test file: `uv run pytest tests/test_profile_data.py -v`

### Code Quality
- Run all pre-commit checks: `uv run pre-commit run -a`
- Run specific linter: `uv run pylint perprof/`
- Format code: `uv run black perprof/ tests/`

### Examples and Demo
- Run example generation: `cd perprof/examples && uv run ./make-examples.sh`
- Test CLI with demo data: `uv run perprof --bokeh --demo`

### Documentation
- Build docs: `uv run mkdocs build`
- Serve docs locally: `uv run mkdocs serve`

### Package Management
- Add new dependency: `uv add package-name`
- Add development dependency: `uv add --dev package-name`
- Update dependencies: `uv lock --upgrade`
- Build package: `uv build`
- Sync environment after pulling changes: `uv sync`

## Architecture

### Core Components

#### Data Processing Pipeline
1. **parse.py** - Parses solver data files in YAML format with problem results
2. **solver_data.py** - `SolverData` class representing individual solver performance
3. **profile_data.py** - `ProfileData` class computing performance profiles from multiple solvers
4. **prof.py** - Legacy `Pdata` class and data loading utilities

#### Output Backends
- **matplotlib.py** - `Profiler` class for matplotlib/pyplot output (png, pdf, svg, etc.)
- **tikz.py** - `Profiler` class for TikZ/LaTeX output (tex, pdf)
- **bokeh.py** - `Profiler` class for interactive HTML output

#### Main Entry Point
- **main.py** - CLI argument parsing and backend selection logic

### File Format
Input files use YAML front matter followed by problem results:
```
---
Solver Name: MySolver
---
problem1 converged 1.23
problem2 failed 5.67
```

### Backend Selection
The CLI supports multiple backends via flags:
- `--mp` or `--matplotlib` - matplotlib backend
- `--tikz` - TikZ/LaTeX backend
- `--bokeh` - Bokeh HTML backend
- `--raw` - Raw data processing only

## Testing Strategy

- **test_all.py** - Comprehensive backend testing with various input scenarios
- **test_profile_data.py** - Unit tests for ProfileData class
- **test_solver_data.py** - Unit tests for SolverData class
- Tests include error cases (invalid files, missing data, etc.)

### Known Issues
- pandas/numpy compatibility issues may affect bokeh backend and some tests
- Core functionality (raw, matplotlib backends) works correctly
- Use `uv run perprof --raw --demo` or `uv run perprof --mp --demo` for testing

## Release Process

1. Create release branch: `release-vx.y.z`
2. Update version in `pyproject.toml` and `perprof/__init__.py`
3. Update `CHANGELOG.md`
4. Run tests: `uv run pytest -v` and `uv run pre-commit run -a`
5. Create PR and merge after CI passes
6. Tag release on GitHub (triggers PyPI deployment)
