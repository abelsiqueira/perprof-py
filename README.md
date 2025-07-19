# perprof-py

[![Tests](https://github.com/abelsiqueira/perprof-py/actions/workflows/tests.yml/badge.svg)](https://github.com/abelsiqueira/perprof-py/actions/workflows/tests.yml)
[![Lint](https://github.com/abelsiqueira/perprof-py/actions/workflows/lint.yml/badge.svg)](https://github.com/abelsiqueira/perprof-py/actions/workflows/lint.yml)
![PyPI](https://img.shields.io/pypi/v/perprof-py)
[![](https://img.shields.io/badge/docs-latest-blue)](https://abelsiqueira.github.io/perprof-py/latest)
[![](https://img.shields.io/badge/docs-dev-blue)](https://abelsiqueira.github.io/perprof-py/dev)

A Python module for performance profiling (as described by [Dolan and
Moré](http://arxiv.org/abs/cs/0102001)) with TikZ and matplotlib output.

## Reference

When using this software for publications, please cite the paper below, which
describes this project:

> Siqueira, A. S., Costa da Silva, R. G. and Santos, L.-R., (2016).
Perprof-py: A Python Package for Performance Profile of Mathematical
Optimization Software. Journal of Open Research Software. 4(1), p.e12.
DOI: [http://doi.org/10.5334/jors.81](http://doi.org/10.5334/jors.81).

## License

Copyright (C) 2013-2023 Abel Soares Siqueira, Raniere Gaia Costa da Silva, Luiz Rafael dos Santos.
Licensed under the GNU GPL v3.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the [GNU General Public License](LICENSE) for more
details.

## Install

### For Users

```bash
pip install perprof-py
```

### For Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
# Install uv if not already available
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/abelsiqueira/perprof-py.git
cd perprof-py

# Create virtual environment and install dependencies
uv sync --extra dev
```

For more details, see the [documentation](https://abelsiqueira.github.io/perprof-py/latest).

## How to use

```bash
perprof [OPTIONS] FILES
```

### Quick Start

```bash
# Generate performance profile using matplotlib backend
perprof --mp solver1.table solver2.table solver3.table

# Generate interactive HTML profile with Bokeh
perprof --bokeh solver1.table solver2.table solver3.table

# Generate TikZ/LaTeX output
perprof --tikz solver1.table solver2.table solver3.table

# Try the demo data
perprof --demo --bokeh
```

### Available Backends

- `--mp` or `--matplotlib`: Generate plots using matplotlib (PNG, PDF, SVG)
- `--bokeh`: Generate interactive HTML plots using Bokeh
- `--tikz`: Generate TikZ/LaTeX code for publication-quality plots
- `--raw`: Process data without generating plots

For more details on the file format and options, see the [documentation](https://abelsiqueira.github.io/perprof-py/latest).

## Getting Help

If you didn't find something at the documentation, want to report a bug, or request a new feature, please open an [issue](https://github.com/abelsiqueira/perprof-py/issues).
