"""
Functions to parse the files

The files must be in the following format::

    ---
    <Metadata 01>: <Value 01>
    <Metadata 02>: <Value 02>
    ---
    <Problem Name 01> <Exit Flag 01> <Cost 01>
    <Problem Name 02> <Exit Flag 02> <Cost 02>
    <Problem Name 03> <Exit Flag 03> <Cost 03>
    ...
"""

import os.path
import gettext

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class _ParserConfig(object):
    """
    Class to store configuration for the parser.
    """
    def __init__(self, algname, subset, success, mintime, maxtime, free_format):
        self.algname = algname
        self.subset = subset
        self.success = success
        self.mintime = mintime
        self.maxtime = maxtime
        self.free_format = free_format

def _error_message(filename, line_number, details):
    """
    Format the error message.

    :param str filename: name of the file with the error
    :param int line_number: number of the line with the error
    :param str details: details about the error
    :return str: the error message
    """
    return _('ERROR when reading line #{} of {}:\n    {}').format(
            line_number, filename, details)

def _str_sanitize(str2sanitize):
    """
    Sanitize the problem name for LaTeX.

    :param str name: string to be sanitize
    :return: sanitized string
    """
    return str2sanitize.replace('_', '-')

def _parse_yaml(config, yaml_header):
    """
    Parse the yaml header

    :param _ParserConfig config: The configuration for the parser
    :param str yaml: The YAML header
    """
    import yaml

    metadata = yaml.load(yaml_header)
    yaml_options = ['algname', 'subset', 'success', 'mintime', 'maxtime',
            'free_format']
    for opt in metadata:
        if not opt in yaml_options:
            raise ValueError(_("'" + opt + "'" + " is not a valid option for YAML."))
        if 'algname' == opt:
            config.algname = metadata['algname']
        if 'subset' == opt:
            config.subset = metadata['subset']
        if 'success' == opt:
            config.success = metadata['success']
        if 'mintime' == opt:
            config.mintime = metadata['mintime']
        if 'maxtime' == opt:
            config.maxtime = metadata['maxtime']
        if 'free_format' == opt:
            config.free_format = metadata['free_format']

def parse_file(filename, subset=None, success='c', mintime=0,
        maxtime=float('inf'), free_format=False):
    """
    Parse one file.

    :param str filename: name of the file to be parser
    :param list subset: list with the name of the problems to use
    :param list success: list with strings to mark sucess
    :param int mintime: minimum time running the solver
    :param int maxtime: maximum time running the solver
    :param bool free_format: if False request that fail be mark with ``d``
    :return: performance profile data and name of the solver
    """
    parse_config = _ParserConfig(_str_sanitize(filename), subset, success,
            mintime, maxtime, free_format)

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
                parse_config.algname = _str_sanitize(ldata[1])
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
                ldata[0] = _str_sanitize(ldata[0])
                if parse_config.subset and ldata[0] not in parse_config.subset:
                    continue
                if ldata[0] in data:
                    raise ValueError(_error_message(filename, line_number,
                        _('Problem {} is duplicated.'.format(ldata[0]))))
                if ldata[1] in parse_config.success:
                    if len(ldata) < 3:
                        raise ValueError(_error_message(filename, line_number,
                                _('This line must have at least 3 elements.')))
                    else:
                        data[ldata[0]] = float(ldata[2])
                        if data[ldata[0]] < parse_config.mintime:
                            data[ldata[0]] = parse_config.mintime
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
