"""
Functions to parse the files

The files must be in the following format::

    problem-name c time-in-seconds
    problem-name c time-in-seconds
    problem-name d time-in-seconds
    problem-name c time-in-seconds
    problem-name d
    problem-name c time-in-seconds

The ``c`` in the second column means that the problem converged and the ``d``
that it hadn't (in this case ``time-in-seconds`` is optional and can be a string
since it will be stored as ``float("inf")``).
"""

def problem_name_sanitize(name):
    """
    This sanitize the problem name for LaTeX.
    """
    name = name.replace('_', '-')

    return name

def parse_file(fname):
    """
    This function parse one file.
    """
    data = {}
    algname = fname
    with open(fname) as f:
        for l in f:
            ldata = l.split()
            if ldata[0] == '#Name' and len(ldata) == 2:
                algname = ldata[1]
            elif len(ldata) < 2:
                raise ValueError('Line must have at least 2 elements: `{}`.'.format(l[:-1]))
            else:
                if ldata[1] == 'c':
                    if len(ldata) < 3:
                        raise ValueError('When problem converge line must have at least 3 elements: `{}`.'.format(l[:-1]))
                    else:
                        data[problem_name_sanitize(ldata[0])] = float(ldata[2])
                elif ldata[1] == 'd':
                    data[problem_name_sanitize(ldata[0])] = float('inf')
                else:
                    raise ValueError('The second element in the lime must be `c` or `d`: `{}`.'.format(l[:-1]))
    return data, algname
