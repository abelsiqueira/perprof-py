Command line flags
==================

perprof-py have a lot of options. To see a list with all of then::

    $ perprof --help

Store flags in a file
---------------------

To fully customize your needs, you may need to add a few flags for `perprof`. The
best way to do this is to create a file with a flag in each line and calling
`perprof` with that file as argument, with a `@` preceding the file name::

    $ perprof @filename [more flags] FILE1 FILE2 [FILE3 ...]

For a example you can look at `test/pdf.args`. To use it, enter ::

    $ perprof @test/pdf.args -f -o tmp test/*.long

Please note that the arguments in the file and in the command line are
treated equally, so you can't add conflicting options.
