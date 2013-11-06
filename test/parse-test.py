"""

    >>> import pprint
    >>> import perprof.parse as parse
    >>> data = parse.parse_file('ipopt-4.13.sample')
    >>> pprint.pprint(data)
    {'clnlbeam': 35.0,
     'corkscrw': 7.0,
     'dtoc1nd': 8.0,
     'dtoc2': 10.0,
     'optmass': 3.0,
     'svanberg': 10.0}
    >>> data = parse.parse_file('conpt-31.8.sample')
    >>> pprint.pprint(data)
    {'clnlbeam': inf,
     'corkscrw': 51.0,
     'dtoc1nd': 144.0,
     'dtoc2': inf,
     'hs35': 1.0,
     'optmass': 66.0,
     'svanberg': inf}

"""
