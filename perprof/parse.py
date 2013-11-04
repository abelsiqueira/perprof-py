"""
Functions to parse the files

The files must be in the following format::

    problem-name c time-in-seconds
    problem-name c time-in-seconds
    problem-name d time-in-seconds
    problem-name c time-in-seconds
    problem-name d time-in-seconds
    problem-name c time-in-seconds

The ``c`` in the second column means that the problem converged and the ``d``
that it hadn't (in this case ``time-in-seconds`` can be a string since it will
be stored as ``float("inf")``).
"""

def parse_file(fname):
    """
    This function parse one file.
    """
    data = {}
    with open(fname) as f:
        for l in f:
            ldata = l.split()
            if len(ldata) != 3:
                raise ValueError('Line of files must have 3 elements.')
            else:
                if ldata[1] == 'c':
                    data[ldata[0]] = [True, ldata[2]]
                elif ldata[1] == 'd':
                    data[ldata[0]] = [False, float('inf')]
                else:
                    raise ValueError('The second element in the lime must be `c` or `d`.')
    return data
