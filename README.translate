Translation
===========

This you will find instructions of how add a new translation to perprof-py.

Setup
-----

To setup a translation to a new language you need to create the directory
`locale/xx_yy/LC_MESSAGES` where `xx_yy` is the location code of your
translation. To create the directory you can use

    $ mkdir -p perprof/locale/xx_yy/LC_MESSAGES

After create the directory you need to create the file
`perprof/locale/xx_yy/LC_MESSAGES/perprof.po` and for that you can use

    $ cp perprof/locale/perprof.pot perprof/locale/xx_yy/LC_MESSAGES/perprof.po

Now you translate the strings in the file
`perprof/locale/xx_yy/LC_MESSAGES/perprof.po` and after that create the file
`perprof/locale/xx_yy/LC_MESSAGES/perprof.mo` using

    $ msgfmt.py -o perprof/locale/xx_yy/LC_MESSAGES/perprof.{mo,po}

Testing
-------

To test add `LC_MESSAGES=xx_yy` before the normal call of `perprof`.

**Note**: if `perprof/locale/xx_yy/LC_MESSAGES/perprof.mo` don't exist it will
raise a error.

Updating
--------

The strings to be translate are mark using _(...). Once you add more strings to
translate you need to update the file `perprof/locale/perprof.pot` and for that you
could use

    $ pygettext.py -p perprof/locale/ -o perprof.pot \
    perprof/*.py
