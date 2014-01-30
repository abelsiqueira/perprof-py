"""
Functions to parse the files

The files must be in the following format::

    problem-name c time-in-seconds
    problem-name c time-in-seconds
    problem-name d time-in-seconds
    problem-name c time-in-seconds
    problem-name d
    problem-name c time-in-seconds

The first column is the problem name.  The second column indicates if the
problem converged, where ``c`` means yes, and ``d`` means no.  The third column
is the elapsed time the solver used to reach the solution. If the solver did not
converge, this column is ignored.
"""

import re

def str_sanitize(name):
    """
    This sanitize the problem name for LaTeX.
    """
    name = name.replace('_', '-')

    return name

def parse_file(fname, subset, success, free_format=False):
    """
    This function parse one file.
    """
    if len(subset) > 0:
        has_subset = True;
    else:
        has_subset = False;
    data = {}
    algname = str_sanitize(fname)
    with open(fname) as f:
        for l in f:
            ldata = l.split()
            if ldata[0] == '#Name' and len(ldata) >= 2:
                algname = str_sanitize(ldata[1])
            elif len(ldata) < 2:
                raise ValueError('ERROR: Line must have at least 2 elements: `{}`.'.format(l.strip()))
            else:
                ldata[0] = str_sanitize(ldata[0])
                if has_subset and ldata[0] not in subset:
                    continue
                if ldata[1] in success:
                    if len(ldata) < 3:
                        raise ValueError('ERROR: When problem converge line must have at least 3 elements: `{}`.'.format(l.strip()))
                    else:
                        data[ldata[0]] = float(ldata[2])
                        if data[ldata[0]] == 0:
                            raise ValueError("ERROR: Time spending can't be zero: Problem '{:1}' from '{:2}'.".format(ldata[0], fname))
                elif free_format or ldata[1] == 'd':
                    data[ldata[0]] = float('inf')
                else:
                    raise ValueError('ERROR: The second element in the lime must be `c` or `d`: `{}`.'.format(l[:-1]))
    return data, algname
