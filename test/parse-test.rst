# doctest: +ELLIPSIS

Here are some test for parse.py.

Test for errors::

    >>> import perprof.parse as parse
    >>> data = parse.parse_file('parse-error0.sample')
    Traceback (most recent call last):
        ...
    ValueError: Line must have at least 2 elements: `3PK`.
    >>> data = parse.parse_file('parse-error1.sample')
    Traceback (most recent call last):
        ...
    ValueError: When problem converge line must have at least 3 elements: `3PK c`.
    >>> data = parse.parse_file('parse-error2.sample')
    Traceback (most recent call last):
        ...
    ValueError: The second element in the lime must be `c` or `d`: `3PK x`.

Test for parser::

    >>> import pprint
    >>> import perprof.parse as parse
    >>> data = parse.parse_file('ipopt-4.13.sample')
    >>> pprint.pprint(data)
    ({'clnlbeam': 35.0,
      'corkscrw': 7.0,
      'dtoc1nd': 8.0,
      'dtoc2': 10.0,
      'optmass': 3.0,
      'svanberg': 10.0},
     'ipopt-4.13.sample')
    >>> data = parse.parse_file('conpt-31.8.sample')
    >>> pprint.pprint(data)
    ({'clnlbeam': inf,
      'corkscrw': 51.0,
      'dtoc1nd': 144.0,
      'dtoc2': inf,
      'hs35': 1.0,
      'optmass': 66.0,
      'svanberg': inf},
     'conpt-31.8.sample')

