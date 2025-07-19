# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and human contributors when working with code in this repository.

## Project Overview

perprof-py is a Python package for generating performance profiles as described by Dolan and Moré. It creates visualizations comparing the performance of different solvers/algorithms using TikZ, matplotlib, or Bokeh backends.

**Requirements**: Python 3.8+ (tested on 3.8-3.12)

## Development Setup

### Prerequisites

**All platforms**: Ensure you have Python 3.8+ and git installed.

### Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast dependency management.

#### Setup Development Environment

**From the project root directory**:

```bash
# Create virtual environment and install all dependencies
uv sync --group dev
```

**Alternative setup** (if uv is unavailable):

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
```

### Optional System Dependencies

**TikZ backend** (for publication-quality LaTeX output):

**Ubuntu/Debian**:

```bash
sudo apt-get install texlive-pictures texlive-fonts-recommended texlive-latex-extra
```

**macOS** (with Homebrew):

```bash
brew install --cask mactex
```

**Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)

**Note**: TikZ backend will fail gracefully if LaTeX is not available. Other backends work without LaTeX.

## Common Development Commands

### Testing

**Run all tests** (includes doctests):

```bash
uv run pytest -v
```

**Coverage analysis**:

```bash
uv run pytest --cov=perprof --cov-report=html --cov-report=term
# View report: open htmlcov/index.html in browser
```

**Specific test categories**:

```bash
# Single test file
uv run pytest tests/test_profile_data.py -v

# Only doctests (documentation examples)
uv run pytest --doctest-modules perprof/ --ignore=perprof/examples/ -v

# Only unit tests (exclude doctests)
uv run pytest tests/ -v
```

**Alternative testing** (if uv unavailable):

```bash
python -m pytest -v
```

**Test counts**: 41 total (33 unit tests + 8 doctest modules)

### Code Quality

**All quality checks** (recommended before committing):

```bash
uv run pre-commit run --all-files
```

**Individual tools**:

```bash
# Fast linting and formatting
uv run ruff check perprof/ tests/ --fix
uv run ruff format perprof/ tests/

# Additional linting (slower)
uv run pylint perprof/

# Type checking
uv run mypy perprof/
```

**Setup pre-commit hooks** (runs automatically on git commit):

```bash
uv run pre-commit install
```

### Quick Start / Demo

**Try the tool immediately**:

```bash
# Interactive HTML output
uv run perprof --bokeh --demo

# Static plot output
uv run perprof --matplotlib --png --demo

# With logging to see what happens
uv run perprof --verbose --bokeh --demo -o my_profile
```

**Generate example plots**:

```bash
cd perprof/examples && uv run ./make-examples.sh
```

### Documentation

**Local development** (with auto-reload):

```bash
uv run mkdocs serve
# Open http://127.0.0.1:8000
```

**Build documentation**:

```bash
uv run mkdocs build
```

### Package Management

**Adding dependencies**:

```bash
# Runtime dependency
uv add package-name

# Development dependency (specific group)
uv add --group test package-name     # Testing tools
uv add --group lint package-name     # Linting/formatting
uv add --group type-check package-name  # Type checking

# Optional dependency (for end users)
uv add --optional docs package-name

# Install only specific dependency groups (use --no-dev for granular control)
uv sync --group test --no-dev        # Only testing tools
uv sync --group lint --no-dev        # Only linting/formatting tools
uv sync --group type-check --no-dev  # Only type checking tools
uv sync --group dev                   # All development tools (includes test, lint, type-check)
```

**Maintenance**:

```bash
# Update all dependencies to latest compatible versions
uv lock --upgrade

# Sync environment after pulling changes
uv sync

# Refresh lock file after dependency structure changes
uv lock --refresh

# Build distributable package
uv build
```

## Architecture

### High-Level Workflow

1. **Input**: Solver data files (YAML + tabular format)
2. **Processing**: Parse files → Create performance ratios → Compute profiles
3. **Output**: Generate visualizations using chosen backend

### Core Components

#### Data Processing Pipeline

1. **parse.py** - Parses solver data files in YAML+tabular format
2. **solver_data.py** - `SolverData` class for individual solver performance data
3. **profile_data.py** - `ProfileData` class implementing Dolan-Moré profile computation
4. **prof.py** - Legacy `Pdata` base class (still used by backends)

#### Visualization Backends

- **matplotlib.py** - Static plots (PNG, PDF, SVG, EPS, PS)
- **tikz.py** - Publication-quality LaTeX/TikZ output (TEX, PDF)
- **bokeh.py** - Interactive HTML plots with zoom/pan
- **Raw mode** - Data processing only (tables, no plots)

#### CLI Interface

- **main.py** - Command-line argument parsing and backend routing

### Input File Format

**Structure**: YAML metadata + whitespace-separated data

```yaml
---
Solver Name: MySolver
Success: converged,optimal
---
problem1 converged 1.23 0.001
problem2 failed   5.67 0.1
problem3 optimal  2.45 0.01
```

**Column meanings**:

1. Problem name (required)
2. Exit status (required)
3. Time in seconds (required)
4. Function value (optional)
5. Primal residual (optional)
6. Dual residual (optional)

### Backend Selection

**Command patterns**:

```bash
# Matplotlib (static plots)
perprof --mp --png file1.txt file2.txt
perprof --matplotlib --pdf file1.txt file2.txt

# Bokeh (interactive HTML)
perprof --bokeh file1.txt file2.txt

# TikZ (LaTeX/academic)
perprof --tikz --pdf file1.txt file2.txt

# Raw data only
perprof --raw file1.txt file2.txt
```

**Output defaults**:

- No backend specified → matplotlib PNG
- No output filename → `performance-profile.{ext}`

## Troubleshooting

### Common Issues

**"Module not found" errors**:

```bash
# Ensure virtual environment is activated and dependencies installed
uv sync --group dev
```

**TikZ/LaTeX compilation fails**:

- TikZ backend requires LaTeX installation (see system dependencies above)
- Use `--tikz --tex` to generate .tex file without compilation
- Other backends work without LaTeX

**Tests fail with pandas/numpy warnings**:

- Warnings are expected (numpy 2.0 compatibility constraints)
- All functionality works correctly despite warnings

**Pre-commit hooks fail**:

```bash
# Fix formatting issues automatically
uv run pre-commit run --all-files
```

**Performance/memory issues with large datasets**:

- Consider using `--raw` mode for data processing only
- Profile computation scales O(n×m×k) where n=problems, m=solvers, k=breakpoints

### Getting Help

- **Documentation**: [perprof-py.readthedocs.org](https://perprof-py.readthedocs.org/en/latest/)
- **Issues**: [GitHub Issues](https://github.com/abelsiqueira/perprof-py/issues)
- **Examples**: See `perprof/examples/` directory

## Technical Details

### Dependency Constraints

**Compatibility matrix**:

- **Python**: 3.8+ (tested on 3.8-3.12)
- **numpy**: `<2.0` (ABI compatibility with pandas 1.x and bokeh 2.x)
- **pandas**: 1.x series (performance and API stability)
- **bokeh**: 2.x series (compatible with numpy <2.0)

**Why these constraints**: Resolves import errors and ensures all backends work correctly. All functionality is preserved.

### Code Quality Tools

**Pre-commit hooks** (run automatically on `git commit`):

- **ruff** - Fast Python linting and formatting (replaces black, isort, flake8)
- **mypy** - Static type checking
- **markdownlint** - Markdown formatting consistency
- **lychee** - Fast link checking for documentation
- **prospector** - Additional static analysis
- **validate-pyproject** - TOML file validation

**Manual quality checks**:

```bash
# Complete quality assessment
uv run pre-commit run --all-files
```

### Test Coverage

**Test categories**:

- **Unit tests** (33): Core functionality, edge cases, error handling
- **Doctests** (8 modules): Documentation examples, API usage patterns
- **Integration tests**: Full CLI workflow with all backends

**Coverage targets**:

- Overall: ~67% (focusing on core algorithms)
- ProfileData/SolverData: 100% (critical data processing)
- Backend coverage varies (matplotlib > bokeh > tikz)

## Development Workflow

### Making Changes

**Standard workflow**:

```bash
# 1. Get latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-improvement

# 3. Install development dependencies
uv sync --group dev

# 4. Make your changes...

# 5. Test your changes
uv run pytest -v
uv run pre-commit run --all-files

# 6. Commit (pre-commit hooks run automatically)
git add .
git commit -m "Your descriptive commit message"

# 7. Push and create pull request
git push origin feature/your-improvement
```

### Improvement Planning

**Structured improvement process**:

- **IMPROVEMENT_SUGGESTIONS.md** - 13 analyzed improvements by priority/effort
- **EVALUATION_CHECKLIST.md** - Implementation tracking with decisions

**When implementing improvements**:

1. Check EVALUATION_CHECKLIST.md for current status
2. Update checklist with progress and decisions (✅ Implement / ❌ Skip / ⏸️ Defer)
3. Document implementation details and reasoning

### Release Process

**For maintainers**:

```bash
# 1. Create release branch
git checkout -b release-v1.x.y

# 2. Update version numbers
# Edit: pyproject.toml, perprof/__init__.py, CHANGELOG.md

# 3. Verify everything works
uv run pytest -v
uv run pre-commit run --all-files

# 4. Create PR, merge after CI passes

# 5. Tag release (triggers PyPI deployment)
git tag v1.x.y
git push origin v1.x.y
```

**Versioning**: Follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)

### Contributing Guidelines

**For external contributors**:

1. Fork the repository on GitHub
2. Follow the standard workflow above
3. Ensure all tests pass and pre-commit hooks succeed
4. Write clear commit messages explaining the "why" not just "what"
5. Reference any related issues in your PR description

**Code style**: Automatically enforced by pre-commit hooks (ruff, mypy, etc.)

## Important Instruction Reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
