# This is the main file for perprof

class PerProfSetup():
    """This is a class to store the files to be used."""
    def __init__(self, args):
        self.free_format = args.free_format
        self.cache = args.cache
        self.files = args.file_name
        self.force = args.force
        self.semilog = args.semilog
        self.bw = args.black_and_white
        self.output = args.output
        self.subset = args.subset
        self.pgfplot_version = args.pgfplotcompat
        self.tau = args.tau
        self.pdf_verbose = args.pdf_verbose
        self.success = args.success.split(',')

        if args.pdf:
            self.output_format = 'pdf'
        elif args.tex:
            self.output_format = 'tex'
        else:
            self.output_format = None

    def using_free_format(self):
        return self.free_format

    def set_free_format(self, val):
        self.free_format = val

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

    def get_output_format(self):
        return self.output_format

    def set_output_format(self, output_format):
        self.output_format = output_format

    def using_semilog(self):
        return self.semilog

    def set_semilog(self, val):
        self.semilog = val

    def set_success(self, val):
        self.success = val

    def get_success(self):
        return self.success

    def using_black_and_white(self):
        return self.bw

    def set_black_and_white(self, val):
        self.bw = val

    def get_pdf_verbose(self):
        return self.pdf_verbose

    def set_pdf_verbose(self, val):
        self.pdf_verbose = val

    def get_subset(self):
        return self.subset

    def set_subset(self, subset):
        self.subset = subset

    def get_pgfplot_version(self):
        return self.pgfplot_version

    def set_pgfplot_version(self, version):
        self.pgfplot_version = version

    def get_tau(self):
        return self.tau

    def set_tau(self, tau):
        self.tau = tau

def main():
    """This is the entry point when calling perprof."""
    import argparse

    parser = argparse.ArgumentParser(
            description='A python module for performance profiling (as described by Dolan and Moré).',
            fromfile_prefix_chars='@')

    backend = parser.add_mutually_exclusive_group(required=True)
    backend.add_argument('--mp', action='store_true',
            help='Use matplotlib as backend for the plot')
    backend.add_argument('--tikz', action='store_true',
            help='Use LaTex/TikZ as backend for the plot (only generate the TeX file)')
    backend.add_argument('--raw', action='store_true',
            help='Print raw data')

    output_format = parser.add_mutually_exclusive_group()
    output_format.add_argument('--tex', action='store_true',
            help='The output file will be a (La)TeX file')
    output_format.add_argument('--pdf', action='store_true',
            help='The output file will be a PDF file')

    parser.add_argument('--free-format', action='store_true',
            help='When parsing file handle all non `c` character as `d`')
    parser.add_argument('--pdf-verbose', action='store_true',
            help='Print output of pdflatex')
    parser.add_argument('--black-and-white', action='store_true',
            help='Use only black color.')
    parser.add_argument('--semilog', action='store_true',
            help='Use logarithmic scale for the x axis of the plot')
    parser.add_argument('--success', type=str, default='c',
            help='Flags that are interpreted as success, separated by commas.  Default: `c`')
    parser.add_argument('--tikz-header', action='store_true',
            help='Create the header to the tikz file, enabling compilation of the result')
    parser.add_argument('--pgfplotcompat', type=float, default=None,
            help='Set pgfplots backwards compatibility mode to given version')
    parser.add_argument('-c', '--cache', action='store_true',
            help='Enable cache.')
    parser.add_argument('-s', '--subset',
            help='Name of a file with a subset of problems to compare')
    parser.add_argument('--tau', type=float,
            help='Limit the x-axis based this value')
    parser.add_argument('-f', '--force', action='store_true',
            help='Force overwrite the output file')
    parser.add_argument('-o', '--output',
            help='Name of the file to use as output (the correct extension will be add)')
    parser.add_argument('file_name', nargs='+',
            help='The name of the files to be used for the performance profiling')

    args = parser.parse_args()

    s = PerProfSetup(args)

    try:
        if args.mp:
            # matplotlib
            from . import matplotlib

            d = matplotlib.Profiler(s)
            d.plot()
        elif args.tikz:
            if args.pdf and args.output is None:
                print("ERROR: When using `--pdf` you need to provide the name of the output file.")
            else:
                # tikz
                from . import tikz

                d = tikz.Profiler(s, args.tikz_header)
                d.plot()
        elif args.raw:
            # raw
            from . import prof
            print('raw')
            
            print(prof.Pdata(s))
    except ValueError as error:
        print(error)

