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

## How to use

With perprof installed, you will need to format your output to match a format
handled by it.
The simplest format is 

```
#Name <Solver name>
<Problem name> <exitflag> <time spent>
<Problem name> <exitflag> <time spent>
<Problem name> <exitflag> <time spent>
...
```

where exitflag is `c` or `d`, meaning converged and diverged, respectively.
You can then enter the command

    $ perprof BACKEND FILE1 FILE2 [FILE3 ...]

With BACKEND being one of `--tikz`, `--mp` or `--raw`.
To use another format for the exitflag, or set more options, you can use

    $ perprof -h

to obtain all options. For examples, check the next section.

## Examples

Some examples of input file are provided at `samples`. 
To see the examples already, enter the folder and enter

    $ ./make-examples.sh

This will generate 8 simple examples in the folder `samples/plots`.
For more information, check the README.md in `samples`.

## Use a file for your flags

To fully customize your needs, you may need to add a few flags for perprof. The
best way to do this is to create a file with a flag in each line and calling
`perprof` with that file as argument, with a `@` preceding the file name:

    $ perprof @filename [more flags]

A file test/pdf.args in included as example. To use it, enter

    $ perprof test/*.long -f -o tmp @test/pdf.args

Please note that the arguments in the the file and in the command line are
treated equally, so you can't add confliting options.
