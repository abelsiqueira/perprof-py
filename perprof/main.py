# This is the main file for perprof

class PerProfSetup():
    """This is a class to store the files to be used."""
    def __init__(self, args):
        self.cache = args.cache
        self.files = args.file_name
        self.force = args.force
        self.semilog = args.semilog
        self.output = args.output

    def using_cache(self):
        return self.cache

    def set_cache(self, val):
        self.cache = val

    def get_files(self):
        return self.files

    def set_files(self, files):
        self.files = files

    def using_force(self):
        return self.force

    def set_force(self, force):
        self.force = force

    def get_output(self):
        return self.output

    def set_output(self, output):
        self.output = output

    def using_semilog(self):
        return self.semilog

    def set_semilog(self, val):
        self.semilog= val

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
    parser.add_argument('--semilog', action='store_true',
            help='Use logarithmic scale for the x axis of the plot.')
    parser.add_argument('--tikz-header', action='store_true',
            help='Create the header to the tikz file, enabling compilation of the result')
    parser.add_argument('-c', '--cache', action='store_true',
            help='Enable cache.')
    parser.add_argument('-o', '--output',
            help='Name of the file to use as output (the correct extension will be add)')
    parser.add_argument('-f', '--force', action='store_true',
            help='Force overwrite the output file')
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

        d = tikz.Profiler(s, args.tikz_header)

    d.plot()
