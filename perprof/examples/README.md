# Examples

There are two files in this folder that correspond to the results of two
solvers: Alpha and Beta.

In addition, a third file can be generated from the combination of these two, and
is completely ficticious.

To generate some examples of use, execute

    $ ./make-examples.sh [-l LANG]

The optional argument LANG can be `en` or `pt_BR` currently.

## Each table

Each table has 6 columns.
The columns are, in order:

- Problem name: The name of the problem. In this case, all came from CUTEst.
- Exit flag: The result of the algorithm. Each solver uses a different
  terminology.
- Time spent: Self explanatory.
- Objective function value: The function value at the solution.
- Primal infeasibility: The infeasibility of the algorithm regarding the
  constraints, not the variable bounds. 
- Dual infeasibility: The measurement of optimality. 

The objective function and infeasibilities are not currently used by `perprof`.

## The perprof call

The `perprof` call used is

    $ perprof BACKEND --free-format -l LANG SOLVERS SEMILOG -o plots/NAME \
    --success "converged,success"

- BACKEND is either `--tikz` or `--mp`, which generates a PDF or a PNG,
respectively.
- LANG is obtained from the input. Defaults to `en`.
- SOLVERS are the solvers used, as explained below.
- SEMILOG is either empty or `--semilog` to indicate the use of a semilog axis.
- NAME is the name for each example, as explained below.
- `--free-format` is required to allow unsuccessful results different than `d`.
- `--success STR` is required to allow successful results different than `c`.

## Each example

If the examples were created correctly, you will have now 8 important files in
the folder `plots`, of which 4 are PDF files and 4 are PNG files.

The files are:

- ab - Compare solvers Alpha and Beta.
- abc - Compare sovlers Alpha, Beta and Gamma.
- ab-semilog - Compare solvers Alpha and Beta and plots on a semilog axis.
- abc-semilog - Compare sovlers Alpha, Beta and Gamma and plots on a semilog
  axis.


## Each solver

The solver Alpha returns `converged` on success. The unsuccessful results vary.

The solver Beta returns `success` on success. The unsuccessful results are
always `fail`.

The ficticious solver Gamma is a combination of both.
