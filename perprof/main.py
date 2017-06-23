"""
This is the main file for perprof
"""

SUPPORT_BOKEH = ['html']
SUPPORT_MP = ['eps', 'pdf', 'png', 'ps', 'svg']
SUPPORT_TIKZ = ['tex', 'pdf']

import gettext
import os.path
import sys
import warnings

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

def process_arguments(args):
    """Generates the dictionaries with options"""
    options = {
            'black_and_white': args.black_and_white,
            'cache': args.cache,
            'compare': args.compare,
            'free_format': args.free_format,
            'files': args.file_name,
            'force': args.force,
            'infeas_tol': args.infeasibility_tolerance,
            'lang': args.lang,
            'maxtime': args.maxtime,
            'mintime': args.mintime,
            'output': args.output,
            'pdf_verbose': args.pdf_verbose,
            'pgfplot_version': args.pgfplotcompat,
            'semilog': args.semilog,
            'standalone': args.standalone,
            'success': args.success.split(','),
            'unc': args.unconstrained,
            'tau': args.tau,
            'title': args.title,
            'xlabel': args.xlabel,
            'ylabel': args.ylabel
            }

    if args.no_title:
        options['title'] = None

    if args.background is None:
        options['background'] = None
    else:
        # Set a tuple of integer
        options['background'] = tuple([int(i) for i in
            args.background.split(',')])
        assert len(options['background']) == 3, \
                _("RGB for background must have 3 integers")
    if args.page_background is None:
        options['page_background'] = None
    else:
        options['page_background'] = tuple([int(i) for i in args.page_background.split(',')])
        assert len(options['page_background']) == 3, \
                _("RGB for page background must have 3 integers")

    if args.html:
        options['output_format'] = 'html'
    elif args.eps:
        options['output_format'] = 'eps'
    elif args.pdf:
        options['output_format'] = 'pdf'
    elif args.png:
        options['output_format'] = 'png'
    elif args.ps:
        options['output_format'] = 'ps'
    elif args.svg:
        options['output_format'] = 'svg'
    elif args.tex:
        options['output_format'] = 'tex'
    else:
        if args.bokeh:
            options['output_format'] = 'html'
        elif args.mp:
            options['output_format'] = 'png'
        elif args.tikz:
            options['output_format'] = 'pdf'
        else:
            options['output_format'] = None

    if args.bokeh and options['output_format'] not in SUPPORT_BOKEH:
        raise NotImplementedError(_("Output option {} not supported by "
                "bokeh").format(options['output_format'].upper()))
    elif args.mp and options['output_format'] not in SUPPORT_MP:
        raise NotImplementedError(_("Output option {} not supported by "
                "matplotlib").format(options['output_format'].upper()))
    elif args.tikz and options['output_format'] not in SUPPORT_TIKZ:
        raise NotImplementedError(_("Output option {} not supported by "
                "TikZ").format(options['output_format'].upper()))
    elif args.raw and options['output_format']:
        raise NotImplementedError(
                _("--raw does not support output except standard output"))
    elif args.table and options['output_format']:
        raise NotImplementedError(
                _("--table only write to .tex or to standard output"))

    if args.subset:
        with open(args.subset, 'r') as subset_file:
            options['subset'] = [l.strip() for l in subset_file]
        if len(options['subset']) == 0:
            raise AttributeError(_("ERROR: Subset is empty"))
    else:
        options['subset'] = []

    return options

def set_arguments(args):
    """
    Set all the arguments of perprof
    """
    import argparse

    parser = argparse.ArgumentParser(
            description=_('A python module for performance profiling '
            '(as described by Dolan and Moré).'),
            fromfile_prefix_chars='@')

    proftype_args = parser.add_argument_group(_("Profile types"))
    proftype = proftype_args.add_mutually_exclusive_group(required=False)
    proftype.add_argument('--performance-profile', dest='type',
            action='store_const', const='perf',
            help=_('Performance profile (classic). Default'))
    proftype.add_argument('--data-profile', dest='type',
            action='store_const', const='data',
            help=_('Data profile.'))
    proftype.add_argument('--extended-profile', dest='type',
            action='store_const', const='extended',
            help=_('Extended performance profile. Not implemented'))
    proftype.set_defaults(type='perf')

    backend_args = parser.add_argument_group(_("Backend options"))
    backend = backend_args.add_mutually_exclusive_group(required=True)
    backend.add_argument('--bokeh', action='store_true',
            help=_('Use bokeh as backend for the plot. Default '
            'output: HTML'))
    backend.add_argument('--mp', action='store_true',
            help=_('Use matplotlib as backend for the plot. Default '
            'output: PNG'))
    backend.add_argument('--tikz', action='store_true',
            help=_('Use LaTex/TikZ/pgfplots as backend for the plot. '
            'Default output: PDF'))
    backend.add_argument('--raw', action='store_true',
            help=_('Print raw data. Default output: standard output'))
    backend.add_argument('--table', action='store_true',
            help=_('Print table of robustness and efficiency'))

    output_format_args = parser.add_argument_group(_("Output formats"))
    output_format = output_format_args.add_mutually_exclusive_group()
    output_format.add_argument('--html', action='store_true',
            help=_('The output file will be a HTML file'))
    output_format.add_argument('--eps', action='store_true',
            help=_('The output file will be a EPS file'))
    output_format.add_argument('--pdf', action='store_true',
            help=_('The output file will be a PDF file'))
    output_format.add_argument('--png', action='store_true',
            help=_('The output file will be a PNG file'))
    output_format.add_argument('--ps', action='store_true',
            help=_('The output file will be a PS file'))
    output_format.add_argument('--svg', action='store_true',
            help=_('The output file will be a SVG file'))
    output_format.add_argument('--tex', action='store_true',
            help=_('The output file will be a (La)TeX file'))

    tikz_options = parser.add_argument_group(_("TikZ options"))
    tikz_options.add_argument('--standalone', action='store_true',
            help=_('Create the header as a standalone to the tex file, '
                    'enabling compilation of the result'))
    tikz_options.add_argument('--pgfplotcompat', type=float, default=None,
            help=_('Set pgfplots backwards compatibility mode to given version'))

    parser.add_argument('--lang', '-l', choices=['en', 'pt_BR'], default='en',
            help=_('Set language for plot'))
    parser.add_argument('--free-format', action='store_true',
            help=_('When parsing file handle all non `c` character as `d`'))
    parser.add_argument('--pdf-verbose', action='store_true',
            help=_('Print output of pdflatex'))
    parser.add_argument('--black-and-white', action='store_true',
            help=_('Use only black color.'))
    parser.add_argument('--background',
            help=_('RGB values separated by commas for the background color '
                    'of the plot. (Values in the 0,255 range)'))
    parser.add_argument('--page-background',
            help=_('RGB values separated by commas for the background color '
                    'of the page. (Values in the 0,255 range)'))
    parser.add_argument('--semilog', action='store_true',
            help=_('Use logarithmic scale for the x axis of the plot'))
    parser.add_argument('--success', type=str, default='c',
            help=_('Flags that are interpreted as success, '
                    'separated by commas.  Default: `c`'))
    parser.add_argument('--maxtime', type=float, default=float('inf'),
            help=_('Sets a maximum time for a solved problem. Any problem with a '
                    'time greater than this will be considered failed.'))
    parser.add_argument('--mintime', type=float, default=0,
            help=_('Sets a minimum time for a solved problem. Any problem with a '
                    'time smaller than this will have the time set to this.'))
    parser.add_argument('--compare', choices=['exitflag', 'optimalvalues'],
            default='exitflag', help=_('Choose the type of comparison to be made.'))
    parser.add_argument('--unconstrained', action='store_true',
            help=_('Set the problems to unconstrained, which implies that there '
                    'is no primal feasibility to check.'))
    parser.add_argument('--infeasibility-tolerance', type=float, default=1e-4,
            help=_('Tolerance for the primal and dual infeasibilities'))
    parser.add_argument('--title', type=str,
            default=_("Performance Profile"),
            help=_('Set the title to be show on top of the performance profile'))
    parser.add_argument('--no-title', action='store_true',
            help=_('Removes title'))
    parser.add_argument('--xlabel', type=str,
            default=_("Performance ratio"),
            help=_('Set the x label of the performance profile'))
    parser.add_argument('--ylabel', type=str,
            default=_("Percentage of problems solved"),
            help=_('Set the y label of the performance profile'))

    parser.add_argument('-c', '--cache', action='store_true',
            help=_('Enable cache.'))
    parser.add_argument('-s', '--subset',
            help=_('Name of a file with a subset of problems to compare'))
    parser.add_argument('--tau', type=float,
            help=_('Limit the x-axis based this value'))
    parser.add_argument('-f', '--force', action='store_true',
            help=_('Force overwrite the output file'))
    parser.add_argument('-o', '--output',
            help=_('Name of the file to use as output '
                    '(the correct extension will be add)'))

    parser.add_argument('--demo', action='store_true',
            help=_('Use examples files as input'))
    parser.add_argument('file_name', nargs='*',
            help=_('The name of the files to be used for '
                    'the performance profiling (for demo use `--demo`)'))
    parser.add_argument('--problem-sizes', default='',
            help=_('The sizes of each problem. Required only for data profile'))

    parsed_args = parser.parse_args(args)

    # Set input files for demo
    if parsed_args.demo:
        if parsed_args.file_name:
            warnings.warn(_("Using demo mode. Ignoring input files."),
                    UserWarning)
        if parsed_args.type == 'perf':
            parsed_args.file_name = [
                    os.path.join(THIS_DIR, 'examples/alpha.table'),
                    os.path.join(THIS_DIR, 'examples/beta.table'),
                    os.path.join(THIS_DIR, 'examples/gamma.table')]
        elif parsed_args.type == 'data':
            parsed_args.file_name = [
                    os.path.join(THIS_DIR, 'examples/df-alpha'),
                    os.path.join(THIS_DIR, 'examples/df-beta')]
            parsed_args.problem_sizes = os.path.join(THIS_DIR, 'examples/df.sizes')
        else:
            raise ValueError("Profile type {} not implemented".format(parsed_args.type))
    elif len(parsed_args.file_name) <= 1:
        raise ValueError(_("You must provide at least two input files."))
    elif not parsed_args.type in ['perf', 'data']:
        raise ValueError("Profile type {} not implemented".format(parsed_args.type))
    elif parsed_args.type == 'data' and not os.path.isfile(parsed_args.problem_sizes):
        if parsed_args.problem_sizes == '':
            raise ValueError("Data profile needs problems sizes. (--problem-sizes FILE)")
        else:
            raise ValueError("File {} passed for problem sizes not found.".format(parsed_args.problem_sizes))

    return parsed_args

def main():
    """This is the entry point when calling perprof."""

    try:
        args = set_arguments(sys.argv[1:])

        options = process_arguments(args)

        if args.type == 'perf':
            from .import perfprof
            profile = perfprof.PerfProfile(options)
        else:
            raise NotImplementedError(_("Profile type {} not implemented".format(options.type)))

        x, y = profile.get_plot_data()

        if args.bokeh:
            # bokeh
            from . import bokeh

            bokeh.plot(x, y, options)
        elif args.mp:
            # matplotlib
            from . import matplotlib
            matplotlib.plot(x, y, options)
        elif args.tikz:
            if options['output_format'] == 'pdf' and args.output is None:
                print(_("ERROR: When using PDF output, you need to provide "
                        "the name of the output file."))
            else:
                # tikz
                from . import tikz
                tikz.plot(x, y, options)
        elif args.raw:
            # raw
            from . import perfprof
            print('raw')

            print(perfprof.PerfProfile(options))
        elif args.table:
            raise NotImplementedError("Currently broken")
            # table
            #from . import prof
            #data = prof.Pdata(options)
            #data.print_rob_eff_table()
    except ValueError as error:
        print(error)
    except NotImplementedError as error:
        print(error)
