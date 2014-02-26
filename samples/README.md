# Examples

There are two files in this folder that correspond to the results of two
solvers: Alpha and Beta.

In addition, a third file is generated from the combination of these two, and
is completely ficticious.

The simplest way to compare these files is

    $ perprof --tikz alpha.table beta.table gamma.table -o compare

