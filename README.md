#perprof-py

A python module for performance profiling (as described by [Dolan and
Moré](http://arxiv.org/abs/cs/0102001)) with TikZ and matplotlib output.

## License

GPLv3. See LICENSE.

## Install

Note: This package requires Python3 and isn't compatible with Python2.

Note: You will need *pip* and *setup_tools*. Use the package manager of your
GNU/Linux distribution to install it.

In the terminal:

    # pip install -r REQUIREMENTS
    # python setup.py install

To see a demo:

    $ perprof --mp -o demo -f --demo

## How to use

### Calling `perprof`

Please use `perprof` help:

    $ perprof -h

### Input file format

With `perprof` installed, you will need to format your output to match a format
handled by it. The simplest format is

```
#Name <Solver name>
<Problem name> <exit flag> <time spent>
<Problem name> <exit flag> <time spent>
<Problem name> <exit flag> <time spent>
...
```

where `exit flag` is `c` or `d`, meaning converged and diverged, respectively.
You can then enter the command

    $ perprof BACKEND FILE1 FILE2 [FILE3 ...]

With `BACKEND` being one of `--tikz`, `--mp` or `--raw`.

### YAML header for input file

Every input file can have a YAML header with metadata. The simplest format is

```
---
name: <Solver name>
---
<Problem name> <exit flag> <time spent>
<Problem name> <exit flag> <time spent>
<Problem name> <exit flag> <time spent>
...
```

### Input file examples

Some examples of input file are provided at `perprof/examples`.
To see the examples already

    $ cd perprof/examples
    $ ./make-examples.sh

This will generate 8 simple examples in the folder `perprof/examples/plots`.
For more information, check the `perprof/examples/README.md`.

You can also use the `--demo` flag.

### Use a file for your flags

To fully customize your needs, you may need to add a few flags for `perprof`. The
best way to do this is to create a file with a flag in each line and calling
`perprof` with that file as argument, with a `@` preceding the file name:

    $ perprof @filename [more flags] FILE1 FILE2 [FILE3 ...]

For a example you can look at `test/pdf.args`. To use it, enter

    $ perprof @test/pdf.args -f -o tmp test/*.long

Please note that the arguments in the file and in the command line are
treated equally, so you can't add conflicting options.
