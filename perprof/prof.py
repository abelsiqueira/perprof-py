"""
The functions related with the perform (not the output).
"""

import perprof.parse as parse

def load_data(setup):
    """
    Load the data.

    :param setup: the setup configurations
    :type setup: main.PerProfSetup
    """
    data = {}
    for f in setup.get_files():
        data[f] = parse.parse_file(f)
    return data

def scale():
    """
    Scale time.
    """
    pass
