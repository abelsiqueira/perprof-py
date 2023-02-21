# doctest: +ELLIPSIS

Some test for parse.py.

Test for errors::

    >>> import perprof.parse as parse
    >>> data, algname = parse.parse_file('tests/only-name.sample')
    Traceback (most recent call last):
        ...
    ValueError: ERROR when reading line #1 of tests/only-name.sample:
        This line must have at least 2 elements.
    >>> data, algname = parse.parse_file('tests/without-time.sample')
    Traceback (most recent call last):
        ...
    ValueError: ERROR when reading line #1 of tests/without-time.sample:
        This line must have at least 3 elements.
    >>> data, algname = parse.parse_file('tests/c-or-d.sample')
    Traceback (most recent call last):
        ...
    ValueError: ERROR when reading line #1 of tests/c-or-d.sample:
        The second element in this lime must be c or d.
    >>> data, algname = parse.parse_file('tests/c-or-d.sample', success='cv')
    Traceback (most recent call last):
        ...
    ValueError: ERROR when reading line #1 of tests/c-or-d.sample:
        The second element in this lime must be c, v or d.
    >>> data, algname = parse.parse_file('tests/float-sanitize.sample')
    Traceback (most recent call last):
        ...
    ValueError: ERROR when reading line #1 of tests/float-sanitize.sample:
        Time spending can't be zero.

Test for parser::

    >>> import pprint
    >>> import perprof.parse as parse
    >>> data, algname = parse.parse_file('tests/str-sanitize.sample')
    >>> data
    {'3-K': 0.0133}
