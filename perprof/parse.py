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

def parse_file(fname, subset):
    """
    This function parse one file.
    """
    if len(subset) > 0:
        has_subset = True;
    else:
        has_subset = False;
    data = {}
    algname = fname
    with open(fname) as f:
        for l in f:
            ldata = l.split()
            if ldata[0] == '#Name' and len(ldata) == 2:
                algname = ldata[1]
            elif len(ldata) != 3:
                raise ValueError('Line of files must have 3 elements.')
            else:
                if has_subset and ldata[0] not in subset:
                    continue
                if ldata[1] == 'c':
                    data[ldata[0]] = float(ldata[2])
                elif ldata[1] == 'd':
                    data[ldata[0]] = float('inf')
                else:
                    raise ValueError('The second element in the lime must be `c` or `d`.')
    return data, algname
