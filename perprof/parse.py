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

from .i18n import *

def _error_message(filename, line_number, details):
    """
    Return error message.
    """
    return _('ERROR when reading line #{} of {}:\n    {}').format(
            line_number, filename, details)

def str_sanitize(name):
    """
    This sanitize the problem name for LaTeX.
    """
    name = name.replace('_', '-')

    return name

def parse_file(filename, subset=None, success='c', free_format=False):
    """
    This function parse one file.
    """
    if subset:
        has_subset = True
    else:
        has_subset = False
    data = {}
    algname = str_sanitize(filename)
    with open(filename) as file_:
        line_number = 0
        for line in file_:
            line_number += 1
            ldata = line.split()
            if ldata[0] == '#Name' and len(ldata) >= 2:
                algname = str_sanitize(ldata[1])
            elif len(ldata) < 2:
                raise ValueError(_error_message(filename, line_number,
                        _('This line must have at least 2 elements.')))
            else:
                ldata[0] = str_sanitize(ldata[0])
                if has_subset and ldata[0] not in subset:
                    continue
                if ldata[1] in success:
                    if len(ldata) < 3:
                        raise ValueError(_error_message(filename, line_number,
                                _('This line must have at least 3 elements.')))
                    else:
                        data[ldata[0]] = float(ldata[2])
                        if data[ldata[0]] == 0:
                            raise ValueError(_error_message(filename,
                                    line_number, _("Time spending can't be zero.")))
                elif free_format or ldata[1] == 'd':
                    data[ldata[0]] = float('inf')
                else:
                    raise ValueError(_error_message(filename, line_number,
                            _('The second element in this lime must be {} or d.').format(
                                ', '.join(success))))
    if not data:
        raise ValueError(
                _("ERROR: List of problems (intersected with subset, if any) is empty"))
    return data, algname
