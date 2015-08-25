Input File Format
=================

The current format start with a optional YAML header for metadata follow by the
data as show in the template below::

    ---
    <Metadata 01>: <Value 01>
    <Metadata 02>: <Value 02>
    ---
    <Problem Name 01> <Exit Flag 01> <Cost 01>
    <Problem Name 02> <Exit Flag 02> <Cost 02>
    <Problem Name 03> <Exit Flag 03> <Cost 03>
    ...

where

``<Metadata XX>``
    is the name of metadata field
``<Value XX>``
    is the value of the metadata field
``<Problem Name XX>``
    is the name of the problem
``<Exit Flag XX>``
    is ``c`` or ``d``, meaning converged and diverged, respectively
``<Cost XX>``
    is the "cost" (e.g. time spent) to be used for the performance profile until solve the problem or give up.

Some examples of input file are provided at ``perprof/examples`` (`see it on
GitHub <https://github.com/ufpr-opt/perprof-py/tree/master/perprof/examples>`_).
To see the examples already ::

    $ cd perprof/examples
    $ ./make-examples.sh

This will generate 8 simple examples in the folder ``perprof/examples/plots``.

YAML header
-----------

The YAML header store some useful metadata information and optionally some
configurations.

Metadata
^^^^^^^^

``algname``
    The name of the algorithmic/solver to be used in the plot.
    Default: File name.
``col_dual``
    The column corresponding to the dual feasibility at the solution.
    Default: 6
``col_exit``
    The column corresponding to the exit flag.
    Default: 2
``col_fval``
    The column corresponding to the objective function value at the solution.
    Default: 4
``col_name``
    The column corresponding to the problem names.
    Default: 1
``col_primal``
    The column corresponding to the primal feasibility at the solution.
    Default: 5
``col_time``
    The column corresponding to the time/cost spent on the problem.
    Default: 3
``free_format``
    Only check for mark of success.
    Default: False
``maxtime``
    The maximum time that a algorithmic/solver can run.
    Default: inf (i.e. not verified)
``mintime``
    The minimum time that a algorithmic/solver need to run.
    Default: 0
``subset``
    The name of the file to be used for the subset.
    Default: None
``success``
    List of strings to mark success.
    Default: 'c'
