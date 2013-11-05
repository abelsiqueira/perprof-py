# This is the main file for perprof

class PerProfSetup():
    """This is a class to store the files to be used."""
    def __init__(self, fnames, cache=False):
        self.cache = cache
        self.files = fnames

    def using_cache(self):
        return self.cache

    def set_cache(self, val):
        self.cache = val

    def get_files(self):
        return self.files

    def set_files(self, files):
        self.files = files

def main():
    """This is the entry point when calling perprof."""
    import argparse
    from . import prof

    parser = argparse.ArgumentParser(
            description='A python module for performance profiling (as described by Dolan and Moré).')
    parser.add_argument('-c', '--cache', action='store_true',
            help='Enable cache.')
    parser.add_argument('file_name', nargs='+',
            help='The name of the files to be used for the performance profiling')

    args = parser.parse_args()

    s = PerProfSetup(args.file_name, args.cache)
    d = prof.Pdata(s)
    d.scale()
    d.generate_perf_functions()
    d.print_tikz(True)
    
