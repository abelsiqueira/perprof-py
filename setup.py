from distutils.core import setup
from setuptools import setup

import os

if os.access('/usr/share/bash-completion/completions/', os.W_OK):
    data_files = [
        ('/usr/share/bash-completion/completions/', ['bash-completion/perprof'])]
else:
    data_files = []

setup(
    name='perprof',
    version='1.1.2',
    author='Abel Soares Siqueira, Raniere Gaia Costa da Silva, Luiz Rafael dos Santos',
    author_email='abel.s.siqueira@gmail.com, raniere@ime.unicamp.br, l.r.santos@ufsc.br',
    packages=['perprof'],
    package_data={'perprof': ['locale/*/*/*.mo', 'examples/*.table']},
    url='https://github.com/ufpr-opt/perprof-py',
    license='LICENSE',
    description='A python module for performance profiling (as described by Dolan and Moré)',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts':['perprof = perprof.main:main']},
    data_files=data_files,
    test_suite = 'perprof.tests.test_all'
)
