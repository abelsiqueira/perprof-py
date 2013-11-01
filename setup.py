from distutils.core import setup
from setuptools import setup

setup(
    name='perprof',
    version='0.0.0',
    author='Abel Soares Siqueira, Raniere Gaia Costa da Silva, Luiz Rafael dos Santos',
    author_email='abel@ime.unicamp.br, raniere@ime.unicamp.br, lrsantos@ime.unicamp.br',
    packages=['perprof'],
    url='https://github.com/abelsiqueira/perprof-py',
    license='LICENSE',
    description='A python module for performance profiling (as described by Dolan and Moré)',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts':['perprof = perprof.main:main']}
)
