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

def _parse_yaml(options, yaml_header):
    """
    Parse the yaml header

    :param dict options: the local options for the parser
    :param str yaml: The YAML header
    """
    import yaml

    metadata = yaml.load(yaml_header)
    for opt in metadata:
        if not opt in options:
            raise ValueError(_("'" + opt + "'" + " is not a valid option for YAML."))
        else:
            options[opt] = metadata[opt]

def parse_file(filename, parser_options):
    """
    Parse one file.

    :param str filename: name of the file to be parser
    :param dict options: dictionary with the options:
        list subset: list with the name of the problems to use
        list success: list with strings to mark sucess
        int mintime: minimum time running the solver
        int maxtime: maximum time running the solver
        bool free_format: if False request that fail be mark with ``d``
    :return: performance profile data and name of the solver
    """
    options = parser_options.copy()
    options['algname'] = _str_sanitize(filename)
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
                options['algname'] = _str_sanitize(ldata[1])
            # Handle YAML
            elif ldata[0] == '---':
                if in_yaml:
                    _parse_yaml(options, yaml_header)
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
                if options['subset'] and ldata[0] not in options['subset']:
                    continue
                if ldata[0] in data:
                    raise ValueError(_error_message(filename, line_number,
                        _('Problem {} is duplicated.'.format(ldata[0]))))
                if ldata[1] in options['success']:
                    if len(ldata) < 3 or (len(ldata) < 4 and
                            parser_options['use_obj_func']):
                        raise ValueError(_error_message(filename, line_number,
                                _('This line must have at least 3 elements.')))
                    else:
                        data[ldata[0]] = {"time": float(ldata[2]),
                                "fval": float('inf')}
                        if parser_options['use_obj_func']:
                            data[ldata[0]]["fval"] = float(ldata[3])
                        if data[ldata[0]]["time"] < options['mintime']:
                            data[ldata[0]]["time"]= options['mintime']
                        if data[ldata[0]]["time"] == 0:
                            raise ValueError(_error_message(filename,
                                    line_number, _("Time spending can't be zero.")))
                        elif data[ldata[0]]["time"] >= options['maxtime']:
                            ldata[1] = 'd'
                            data[ldata[0]]["time"] = float('inf')
                elif options['free_format'] or ldata[1] == 'd':
                    data[ldata[0]] = float('inf')
                else:
                    raise ValueError(_error_message(filename, line_number,
                            _('The second element in this lime must be {} or d.').format(
                                ', '.join(options['success']))))
    if not data:
        raise ValueError(
                _("ERROR: List of problems (intersected with subset, if any) is empty"))
    return data, options['algname']
