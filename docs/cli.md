# Command Line Usage

The basic usage of **perprof-py** is

```bash
perprof FILES BACKEND
```

Where `FILES` are result files in the format given in [File Format](file-format.md), and `BACKEND` is one of the supported [backends](#backends).

## Backends

- `--bokeh`: Use bokeh as backend for the plot. Default output: HTML
- `--mp`: Use matplotlib as backend for the plot. Default output: PNG
- `--tikz`: Use LaTex/TikZ/pgfplots as backend for the plot. Default output: PDF
- `--raw`: Print raw data. Default output: standard output
- `--table`: Print table of robustness and efficiency

## Command line flags

To fully customize your needs, you may need to add a few flags for `perprof`.
There are a lot of options, to see a list with all of then:

```bash
perprof --help
```

Some of the most important are

- `--semilog`:: Use logarithmic scale for the x axis of the plot.
- `--success SUCCESS`:: Set the values that are interpreted as success by `perprof`. Defaults to `c`.
- `--free-format`:: Indicates that values that are not success should be accepted as failures.
- `-o NAME`:: Sets the file name of the output.
- `-f`:: Overwrite the output file, if it exists.

For instance, the call

```bash
perprof FILES --mp --o prof -f --semilog --success "optimal,conv" --free-format
```

calls `perprof` with matplotLib, saves to file `prof.png`, overwrites if it exists, uses a semilog axis, set the success strings to `optimal` and `conv`, and indicates that every other exitflag string is a failure.

### Store flags in a file

When calling perprof often, it is best to create a file storing your desired flags.
You may then call this file with a `@` preceding the file name:

```bash
perprof @flagfile [more flags] FILES
```

The file `flagfile`, for our examples above, would be

```bash
--mp -o prof -f --semilog --success "optimal,conv" --free-format
```

Please note that the arguments in the file and in the command line are treated equally, so you can't add conflicting options.

## Docker

You can use the docker image [abelsiqueira/perprof-py](https://hub.docker.com/r/abelsiqueira/perprof-py) to run perprof.
The Docker image should contain everything you need to run all backends.
Check the tags in the site to decide which one you want to use, if you want to specify it.
Don't forget to add volumes to pass the data and receive the output, for instance:

```bash
mkdir data output
cp [FILES] data/
docker run -v$PWD/data:/data -v$PWD/output:output abelsiqueira/perprof-py \
    /data/FILE1 /data/FILE2 -o /output/pp --mp -f
```
