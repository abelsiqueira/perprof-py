# perprof-py

[![Build Status](https://travis-ci.org/abelsiqueira/perprof-py.svg?branch=master)](https://travis-ci.org/abelsiqueira/perprof-py)

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

Copyright (C) 2013-2017 Abel Soares Siqueira, Raniere Gaia Costa da Silva, Luiz Rafael dos Santos.
Licensed under the GNU GPL v3.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the [GNU General Public License](LICENSE) for more
details.

## Documentation

Read the documentation on [Read the Docs](https://perprof-py.readthedocs.org/en/latest/).

### Install

See [all the instructions at documentation](https://perprof-py.readthedocs.org/en/latest/install.html).

### How to use

#### Input file format

See [all the instructions at documentation](https://perprof-py.readthedocs.org/en/latest/file-format.html).

#### Command-line arguments

```bash
$ perprof -h
usage: perprof [-h] (--bokeh | --mp | --tikz | --raw | --table)
               [--html | --eps | --pdf | --png | --ps | --svg | --tex]
               [--standalone] [--pgfplotcompat PGFPLOTCOMPAT]
               [--lang {en,pt_BR}] [--free-format] [--pdf-verbose]
               [--black-and-white] [--background BACKGROUND]
               [--page-background PAGE_BACKGROUND] [--semilog]
               [--success SUCCESS] [--maxtime MAXTIME] [--mintime MINTIME]
               [--compare {exitflag,optimalvalues}] [--unconstrained]
               [--infeasibility-tolerance INFEASIBILITY_TOLERANCE]
               [--title TITLE] [--no-title] [--xlabel XLABEL]
               [--ylabel YLABEL] [-c] [-s SUBSET] [--tau TAU] [-f] [-o OUTPUT]
               [--demo]
               [file_name ...]

A python module for performance profiling (as described by Dolan and Moré).

positional arguments:
  file_name             The name of the files to be used for the performance
                        profiling (for demo use `--demo`)

options:
  -h, --help            show this help message and exit
  --lang {en,pt_BR}, -l {en,pt_BR}
                        Set language for plot
  --free-format         When parsing file handle all non `c` character as `d`
  --pdf-verbose         Print output of pdflatex
  --black-and-white     Use only black color.
  --background BACKGROUND
                        RGB values separated by commas for the background
                        color of the plot. (Values in the 0,255 range)
  --page-background PAGE_BACKGROUND
                        RGB values separated by commas for the background
                        color of the page. (Values in the 0,255 range)
  --semilog             Use logarithmic scale for the x axis of the plot
  --success SUCCESS     Flags that are interpreted as success, separated by
                        commas. Default: `c`
  --maxtime MAXTIME     Sets a maximum time for a solved problem. Any problem
                        with a time greater than this will be considered
                        failed.
  --mintime MINTIME     Sets a minimum time for a solved problem. Any problem
                        with a time smaller than this will have the time set
                        to this.
  --compare {exitflag,optimalvalues}
                        Choose the type of comparison to be made.
  --unconstrained       Set the problems to unconstrained, which implies that
                        there is no primal feasibility to check.
  --infeasibility-tolerance INFEASIBILITY_TOLERANCE
                        Tolerance for the primal and dual infeasibilities
  --title TITLE         Set the title to be show on top of the performance
                        profile
  --no-title            Removes title
  --xlabel XLABEL       Set the x label of the performance profile
  --ylabel YLABEL       Set the y label of the performance profile
  -c, --cache           Enable cache.
  -s SUBSET, --subset SUBSET
                        Name of a file with a subset of problems to compare
  --tau TAU             Limit the x-axis based this value
  -f, --force           Force overwrite the output file
  -o OUTPUT, --output OUTPUT
                        Name of the file to use as output (the correct
                        extension will be add)
  --demo                Use examples files as input

Backend options:
  --bokeh               Use bokeh as backend for the plot. Default output:
                        HTML
  --mp                  Use matplotlib as backend for the plot. Default
                        output: PNG
  --tikz                Use LaTex/TikZ/pgfplots as backend for the plot.
                        Default output: PDF
  --raw                 Print raw data. Default output: standard output
  --table               Print table of robustness and efficiency

Output formats:
  --html                The output file will be a HTML file
  --eps                 The output file will be a EPS file
  --pdf                 The output file will be a PDF file
  --png                 The output file will be a PNG file
  --ps                  The output file will be a PS file
  --svg                 The output file will be a SVG file
  --tex                 The output file will be a (La)TeX file

TikZ options:
  --standalone          Create the header as a standalone to the tex file,
                        enabling compilation of the result
  --pgfplotcompat PGFPLOTCOMPAT
                        Set pgfplots backwards compatibility mode to given
                        version
```

## Getting Help

If you didn't find something at the documentation,
want to report a bug,
or request a new feature,
please open a [issue](https://github.com/abelsiqueira/perprof-py/issues).
