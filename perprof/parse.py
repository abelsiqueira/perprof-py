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

import os.path
import gettext

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class _ParserConfig(object):
    """Store configuration for the parser."""
    def __init__(self, algname, subset, success, maxtime, free_format):
        self.algname = algname
        self.subset = subset
        self.success = success
        self.maxtime = maxtime
        self.free_format = free_format

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

def _parse_yaml(config, yaml_header):
    """
    Parse the yaml header

    :param _ParserConfig config The configuration for the parser
    :param str yaml: The YAML header
    """
    import yaml

    metadata = yaml.load(yaml_header)
    if 'algname' in metadata:
        config.algname = metadata['algname']
    if 'subset' in metadata:
        config.subset = metadata['subset']
    if 'success' in metadata:
        config.success = metadata['success']
    if 'maxtime' in metadata:
        config.maxtime = metadata['maxtime']
    if 'free_format' in metadata:
        config.free_format = metadata['free_format']

def parse_file(filename, subset=None, success='c', maxtime=float('inf'), free_format=False):
    """
    This function parse one file.
    """
    parse_config = _ParserConfig(str_sanitize(filename), subset, success, maxtime, free_format)

    data = {}
    with open(filename) as file_:
        line_number = 0
        in_yaml = False
        yaml_header = ''
        for line in file_:
            line_number += 1
            ldata = line.split()
            # This is for backward compatibility
            if ldata[0] == '#Name' and len(ldata) >= 2:
                parse_config.algname = str_sanitize(ldata[1])
            # Handle YAML
            elif ldata[0] == '---':
                if in_yaml:
                    _parse_yaml(parse_config, yaml_header)
                    in_yaml = False
                else:
                    in_yaml = True
            elif in_yaml:
                yaml_header += line
            # Parse data
            elif len(ldata) < 2:
                raise ValueError(_error_message(filename, line_number,
                        _('This line must have at least 2 elements.')))
            else:
                ldata[0] = str_sanitize(ldata[0])
                if parse_config.subset and ldata[0] not in parse_config.subset:
                    continue
                if ldata[1] in parse_config.success:
                    if len(ldata) < 3:
                        raise ValueError(_error_message(filename, line_number,
                                _('This line must have at least 3 elements.')))
                    else:
                        data[ldata[0]] = float(ldata[2])
                        if data[ldata[0]] == 0:
                            raise ValueError(_error_message(filename,
                                    line_number, _("Time spending can't be zero.")))
                        elif data[ldata[0]] >= parse_config.maxtime:
                            ldata[1] = 'd'
                            data[ldata[0]] = float('inf')
                elif parse_config.free_format or ldata[1] == 'd':
                    data[ldata[0]] = float('inf')
                else:
                    raise ValueError(_error_message(filename, line_number,
                            _('The second element in this lime must be {} or d.').format(
                                ', '.join(success))))
    if not data:
        raise ValueError(
                _("ERROR: List of problems (intersected with subset, if any) is empty"))
    return data, parse_config.algname
