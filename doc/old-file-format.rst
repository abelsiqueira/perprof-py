Old Input File Format
=====================

.. important::

   This is keep to backward compatibility.

The old format follow the template below::

    #Name <Solver Name>
    <Problem Name 01> <Exit Flag 01> <Cost 01>
    <Problem Name 02> <Exit Flag 02> <Cost 02>
    <Problem Name 03> <Exit Flag 03> <Cost 03>
    ...

where

``<Solver Name>``
    is the name of the solver to be used in the plot
``<Problem Name XX>``
    is the name of the problem
``<Exit Flag XX>``
    is ``c`` or ``d``, meaning converged and diverged, respectively
``<Cost XX>``
    is the "cost" (e.g. time spent) to be used for the performance profile until solve the problem or give up.
