Command line flags
==================

To fully customize your needs, you may need to add a few flags for ``perprof``.
There are a lot of options, to see a list with all of then::

    $ perprof --help

Some of the most important are

* ``--semilog``:: Use logarithmic scale for the x axis of the plot.
* ``--success SUCCESS``:: Set the values that are interpreted as success by
    ``perprof``. Defaults to ``c``.
* ``--free-format``:: Indicates that values that are not success should be
  accepted as failures.
* ``-o NAME``:: Sets the file name of the output.
* ``-f``:: Overwrite the output file, if it exists.

So, for instance, the call

    $ perprof FILES --mp --o prof -f --semilog --success "optimal,conv"
    --free-format

calls ``perprof`` with MatplotLib, saves to file ``prof.png``, overwrites if it
exists, uses a semilog axis, set the success strings to ``optimal`` and
``conv``, and indicates that every other exitflag string is a failure.

Store flags in a file
---------------------

When calling perprof often, it is best to create a file storing your desired
flags. You may then call this file with a ``@`` preceding the file name::

    $ perprof @flagfile [more flags] FILE1 FILE2 [FILE3 ...]

The file ``flagfile``, for our examples above, would be

    --mp
    -o
    prof
    -f
    --semilog
    --success
    "optimal,conv"
    --free-format

Please note that the arguments in the file and in the command line are
treated equally, so you can't add conflicting options.
