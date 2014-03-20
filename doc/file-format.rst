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

``Metadata XX``
    is the name of metadata field
``Vallue XX``
    is the value of the metadata field
``Problem Name XX``
    is the name of the problem
``Exit Flag XX``
    is ``c`` or ``d``, meaning converged and diverged, respectively
``Cost XX``
    is the "cost" (e.g. time spent) to be used for the performance profile until solve the problem or give up.

Some examples of input file are provided at `perprof/examples`.
To see the examples already ::

    $ cd perprof/examples
    $ ./make-examples.sh

This will generate 8 simple examples in the folder `perprof/examples/plots`.

YAML header
-----------

The YAML header store some useful metadata information and optional some
configurations.
