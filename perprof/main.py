# This is the main file for perprof

class PerProfSetup():
    """This is a class to store the files to be used."""
    def __init__(self, args):
        self.cache = args.cache
        self.files = args.file_name
        self.log = args.log

    def using_cache(self):
        return self.cache

    def set_cache(self, val):
        self.cache = val

    def get_files(self):
        return self.files

    def set_files(self, files):
        self.files = files

    def using_log(self):
        return self.log

    def set_log(self, val):
        self.log= val

def main():
    """This is the entry point when calling perprof."""
    import argparse

    parser = argparse.ArgumentParser(
            description='A python module for performance profiling (as described by Dolan and Moré).')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--mp', action='store_true',
            help='Use matplotlib as backend for the plot')
    group.add_argument('--tikz', action='store_true',
            help='Use LaTex/TikZ as backend for the plot (only generate the TeX file)')
    parser.add_argument('--log', action='store_true',
            help='Use logarithmic scale for the plot.')
    parser.add_argument('-c', '--cache', action='store_true',
            help='Enable cache.')
    parser.add_argument('file_name', nargs='+',
            help='The name of the files to be used for the performance profiling')

    args = parser.parse_args()

    s = PerProfSetup(args)

    if args.mp:
        # matplotlib
        from . import matplotlib

        d = matplotlib.Profiler(s)
    elif args.tikz:
        # tikz
        from . import tikz

        d = tikz.Profiler(s)

    d.plot()
