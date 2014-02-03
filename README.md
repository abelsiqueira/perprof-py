#perprof-py 

A python module for performance profiling (as described by [Dolan and
Moré](http://arxiv.org/abs/cs/0102001)) with tikz and matplotlib output.

## License

GPLv3. See LICENSE.

## Install

Note: You will need *pip* and *setup_tools*. Use the package manager of your
GNU/Linux distribution to install it.

In the terminal:

    # pip install -r REQUIREMENTS
    # python setup.py install

If you use bash and bash-completion, you can, and should, also copy the
`perprof.bash-completion` to your completions folder. This folder is
`/usr/share/bash-completion/completions` for some distributions. Change the name
of the file `perprof.bash-completion` to `perprof`.

## How to use

Some examples of input file are provided at `test`. You can get a list of they
with

    $ ls test/*.sample

To create a PNG file using matplotlib:

    $ perprof --mp file_name [file_name ...]

Example:

    $ perprof --mp test/*.long

To create a PDF using LaTeX and TikZ:

    $ perprof --tikz --tikz-header file_name [file_name ...]

Example:

    $ perprof --tikz --tikz-header test/*.long

To create the `.tex` file to be include in another document:

    $ perprof --tikz file_name [file_name ...]

Example:

    $ perprof --tikz test/*.long

And for help

    $ perprof -h

## Use a file for your flags

To fully customize your needs, you may need to add a few flags for perprof. The
best way to do this is to create a file with a flag in each line and calling
`perprof` with that file as argument, with a `@` preceding the file name:

    $ perprof @filename [more flags]

A file test/pdf.args in included as example. To use it, enter

    $ perprof test/*.long -f -o tmp @test/pdf.args

Please note that the arguments in the the file and in the command line are
treated equally, so you can't add confliting options.
