#perprof-py 

A python module for performance profiling (as described by Dolan and Moré) with
tikz and matplotlib outputing.

## License

GPLv3. See LICENSE.

## Install

Note: You will need *pip* and *setup_tools*. Use the package manager of your
GNU/Linux distribution to install it.

In the terminal:

    # pip install -r REQUIREMENTS
    # python setup.py install

## How to use

Some examples of input file are provided at `test`. You can get a list of they
with

    $ ls test/*.sample

For create a PNG file using matplotlib:

    $ perprof --mp file_name [file_name ...]

Example:

    $ perprof --mp test/*.long

For create a PDF using LaTeX and TikZ:

    $ perprof --tikz --tikz-header file_name [file_name ...]

Example:

    $ perprof --tikz --tikz-header test/*.long

For create the `.tex` file to be include in another document:

    $ perprof --tikz file_name [file_name ...]

Example:

    $ perprof --tikz test/*.long

And for help

    $ perprof -h
