"""

    >>> import pprint
    >>> import perprof.parse as parse
    >>> data = parse.parse_file('ipopt-4.13.sample')
    >>> pprint.pprint(data)
    {'clnlbeam': [True, '35'],
     'corkscrw': [True, '7'],
     'dtoc1nd': [True, '8'],
     'dtoc2': [True, '10'],
     'optmass': [True, '3'],
     'svanberg': [True, '10']}
    >>> data = parse.parse_file('conpt-31.8.sample')
    >>> pprint.pprint(data)
    {'clnlbeam': [False, inf],
     'corkscrw': [True, '51'],
     'dtoc1nd': [True, '144'],
     'dtoc2': [False, inf],
     'optmass': [True, '66'],
     'svanberg': [False, inf]}

"""
