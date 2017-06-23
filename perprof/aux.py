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
            raise ValueError("'" + opt + "'" + _(" is not a valid option for YAML."))
        else:
            options[opt] = metadata[opt]
