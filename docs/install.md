# Install

Below you will find instructions to install perprof-py for any operation
system that run Python and after that more detail instructions for some
popular operation system.

## General

You can install `perprof-py` from PyPI as follow:

```bash
python -m pip install perprof-py
```

You can also use the docker image [abelsiqueira/perprof-py](https://hub.docker.com/r/abelsiqueira/perprof-py).
See the [Docker usage](cli.md#docker) for details.

## Extra requirements

To use the PGFPlots backend (`--tikz`), the LaTeX packages must be installed.
On Ubuntu, we install `texlive-pictures`, `texlive-fonts-recommended`, and `texlive-latex-extra` to have everything that we need to run the tests.
