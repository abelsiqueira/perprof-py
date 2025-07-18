"""Main file for perprof."""

from __future__ import annotations

import argparse
import gettext
import os.path
import sys
import warnings
from typing import TypedDict

# pylint: disable=import-outside-toplevel


SUPPORT_BOKEH = ["html"]
SUPPORT_MP = ["eps", "pdf", "png", "ps", "svg"]
SUPPORT_TIKZ = ["tex", "pdf"]


THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation("perprof", os.path.join(THIS_DIR, "locale"))
_ = THIS_TRANSLATION.gettext


class ParserOptions(TypedDict):
    """Type definition for parser options dictionary."""

    free_format: bool
    files: list[str]
    success: list[str]
    maxtime: float
    mintime: float
    compare: str
    unc: bool
    infeas_tol: float
    subset: list[str]


class ProfilerOptions(TypedDict):
    """Type definition for profiler options dictionary."""

    lang: str
    cache: bool
    files: list[str]
    force: bool
    standalone: bool
    semilog: bool
    black_and_white: bool
    output: str | None
    pgfplot_version: float | None
    tau: float | None
    pdf_verbose: bool
    title: str | None
    xlabel: str
    ylabel: str
    background: tuple[int, int, int] | None
    page_background: tuple[int, int, int] | None
    output_format: str | None


# pylint: disable=too-many-statements,too-many-branches
def process_arguments(
    args: argparse.Namespace,
) -> tuple[ParserOptions, ProfilerOptions]:
    """Generate the dictionaries with options."""
    parser_options: ParserOptions = {
        "free_format": args.free_format,
        "files": args.file_name,
        "success": args.success.split(","),
        "maxtime": args.maxtime,
        "mintime": args.mintime,
        "compare": args.compare,
        "unc": args.unconstrained,
        "infeas_tol": args.infeasibility_tolerance,
        "subset": [],  # Will be set below if args.subset exists
    }

    profiler_options: ProfilerOptions = {
        "lang": args.lang,
        "cache": args.cache,
        "files": args.file_name,
        "force": args.force,
        "standalone": args.standalone,
        "semilog": args.semilog,
        "black_and_white": args.black_and_white,
        "output": args.output,
        "pgfplot_version": args.pgfplotcompat,
        "tau": args.tau,
        "pdf_verbose": args.pdf_verbose,
        "title": args.title,
        "xlabel": args.xlabel,
        "ylabel": args.ylabel,
        "background": None,  # Will be set below if args.background exists
        "page_background": None,  # Will be set below if args.page_background exists
        "output_format": None,  # Will be set below based on args
    }

    if args.no_title:
        profiler_options["title"] = None

    if args.background is None:
        profiler_options["background"] = None
    else:
        # Set a tuple of integer
        background_tuple = tuple(int(i) for i in args.background.split(","))
        assert len(background_tuple) == 3, _("RGB for background must have 3 integers")
        profiler_options["background"] = background_tuple
    if args.page_background is None:
        profiler_options["page_background"] = None
    else:
        page_background_tuple = tuple(int(i) for i in args.page_background.split(","))
        assert len(page_background_tuple) == 3, _(
            "RGB for page background must have 3 integers"
        )
        profiler_options["page_background"] = page_background_tuple

    if args.html:
        profiler_options["output_format"] = "html"
    elif args.eps:
        profiler_options["output_format"] = "eps"
    elif args.pdf:
        profiler_options["output_format"] = "pdf"
    elif args.png:
        profiler_options["output_format"] = "png"
    elif args.ps:
        profiler_options["output_format"] = "ps"
    elif args.svg:
        profiler_options["output_format"] = "svg"
    elif args.tex:
        profiler_options["output_format"] = "tex"
    elif args.bokeh:
        profiler_options["output_format"] = "html"
    elif args.mp:
        profiler_options["output_format"] = "png"
    elif args.tikz:
        profiler_options["output_format"] = "pdf"
    else:
        profiler_options["output_format"] = None

    output_format = profiler_options["output_format"]
    if args.bokeh and output_format not in SUPPORT_BOKEH:
        raise NotImplementedError(
            _("Output option {} not supported by bokeh").format(
                output_format.upper() if output_format else "None"
            )
        )
    if args.mp and output_format not in SUPPORT_MP:
        raise NotImplementedError(
            _("Output option {} not supported by matplotlib").format(
                output_format.upper() if output_format else "None"
            )
        )
    if args.tikz and output_format not in SUPPORT_TIKZ:
        raise NotImplementedError(
            _("Output option {} not supported by TikZ").format(
                output_format.upper() if output_format else "None"
            )
        )
    if args.raw and output_format:
        raise NotImplementedError(
            _("--raw does not support output except standard output")
        )
    if args.table and output_format:
        raise NotImplementedError(_("--table only write to .tex or to standard output"))

    if args.subset:
        with open(args.subset, encoding="utf-8") as subset_file:
            parser_options["subset"] = [line.strip() for line in subset_file]
        if len(parser_options["subset"]) == 0:
            raise AttributeError(_("ERROR: Subset is empty"))

    return parser_options, profiler_options


def set_arguments(args: list[str]) -> argparse.Namespace:
    """Set all the arguments of perprof."""

    parser = argparse.ArgumentParser(
        description=_(
            "A python module for performance profiling "
            "(as described by Dolan and Moré)."
        ),
        fromfile_prefix_chars="@",
    )

    backend_args = parser.add_argument_group(_("Backend options"))
    backend = backend_args.add_mutually_exclusive_group(required=True)
    backend.add_argument(
        "--bokeh",
        action="store_true",
        help=_("Use bokeh as backend for the plot. Default output: HTML"),
    )
    backend.add_argument(
        "--mp",
        action="store_true",
        help=_("Use matplotlib as backend for the plot. Default output: PNG"),
    )
    backend.add_argument(
        "--tikz",
        action="store_true",
        help=_("Use LaTex/TikZ/pgfplots as backend for the plot. Default output: PDF"),
    )
    backend.add_argument(
        "--raw",
        action="store_true",
        help=_("Print raw data. Default output: standard output"),
    )
    backend.add_argument(
        "--table",
        action="store_true",
        help=_("Print table of robustness and efficiency"),
    )

    output_format_args = parser.add_argument_group(_("Output formats"))
    output_format = output_format_args.add_mutually_exclusive_group()
    output_format.add_argument(
        "--html", action="store_true", help=_("The output file will be a HTML file")
    )
    output_format.add_argument(
        "--eps", action="store_true", help=_("The output file will be a EPS file")
    )
    output_format.add_argument(
        "--pdf", action="store_true", help=_("The output file will be a PDF file")
    )
    output_format.add_argument(
        "--png", action="store_true", help=_("The output file will be a PNG file")
    )
    output_format.add_argument(
        "--ps", action="store_true", help=_("The output file will be a PS file")
    )
    output_format.add_argument(
        "--svg", action="store_true", help=_("The output file will be a SVG file")
    )
    output_format.add_argument(
        "--tex", action="store_true", help=_("The output file will be a (La)TeX file")
    )

    tikz_options = parser.add_argument_group(_("TikZ options"))
    tikz_options.add_argument(
        "--standalone",
        action="store_true",
        help=_(
            "Create the header as a standalone to the tex file, "
            "enabling compilation of the result"
        ),
    )
    tikz_options.add_argument(
        "--pgfplotcompat",
        type=float,
        default=None,
        help=_("Set pgfplots backwards compatibility mode to given version"),
    )

    parser.add_argument(
        "--lang",
        "-l",
        choices=["en", "pt_BR"],
        default="en",
        help=_("Set language for plot"),
    )
    parser.add_argument(
        "--free-format",
        action="store_true",
        help=_("When parsing file handle all non `c` character as `d`"),
    )
    parser.add_argument(
        "--pdf-verbose", action="store_true", help=_("Print output of pdflatex")
    )
    parser.add_argument(
        "--black-and-white", action="store_true", help=_("Use only black color.")
    )
    parser.add_argument(
        "--background",
        help=_(
            "RGB values separated by commas for the background color "
            "of the plot. (Values in the 0,255 range)"
        ),
    )
    parser.add_argument(
        "--page-background",
        help=_(
            "RGB values separated by commas for the background color "
            "of the page. (Values in the 0,255 range)"
        ),
    )
    parser.add_argument(
        "--semilog",
        action="store_true",
        help=_("Use logarithmic scale for the x axis of the plot"),
    )
    parser.add_argument(
        "--success",
        type=str,
        default="c",
        help=_(
            "Flags that are interpreted as success, separated by commas.  Default: `c`"
        ),
    )
    parser.add_argument(
        "--maxtime",
        type=float,
        default=float("inf"),
        help=_(
            "Sets a maximum time for a solved problem. Any problem with a "
            "time greater than this will be considered failed."
        ),
    )
    parser.add_argument(
        "--mintime",
        type=float,
        default=0,
        help=_(
            "Sets a minimum time for a solved problem. Any problem with a "
            "time smaller than this will have the time set to this."
        ),
    )
    parser.add_argument(
        "--compare",
        choices=["exitflag", "optimalvalues"],
        default="exitflag",
        help=_("Choose the type of comparison to be made."),
    )
    parser.add_argument(
        "--unconstrained",
        action="store_true",
        help=_(
            "Set the problems to unconstrained, which implies that there "
            "is no primal feasibility to check."
        ),
    )
    parser.add_argument(
        "--infeasibility-tolerance",
        type=float,
        default=1e-4,
        help=_("Tolerance for the primal and dual infeasibilities"),
    )
    parser.add_argument(
        "--title",
        type=str,
        default=_("Performance Profile"),
        help=_("Set the title to be show on top of the performance profile"),
    )
    parser.add_argument("--no-title", action="store_true", help=_("Removes title"))
    parser.add_argument(
        "--xlabel",
        type=str,
        default=_("Performance ratio"),
        help=_("Set the x label of the performance profile"),
    )
    parser.add_argument(
        "--ylabel",
        type=str,
        default=_("Percentage of problems solved"),
        help=_("Set the y label of the performance profile"),
    )

    parser.add_argument("-c", "--cache", action="store_true", help=_("Enable cache."))
    parser.add_argument(
        "-s", "--subset", help=_("Name of a file with a subset of problems to compare")
    )
    parser.add_argument(
        "--tau", type=float, help=_("Limit the x-axis based this value")
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help=_("Force overwrite the output file")
    )
    parser.add_argument(
        "-o",
        "--output",
        help=_("Name of the file to use as output (the correct extension will be add)"),
    )

    parser.add_argument(
        "--demo", action="store_true", help=_("Use examples files as input")
    )
    parser.add_argument(
        "file_name",
        nargs="*",
        help=_(
            "The name of the files to be used for "
            "the performance profiling (for demo use `--demo`)"
        ),
    )

    parsed_args = parser.parse_args(args)

    # Set input files for demo
    if parsed_args.demo:
        if parsed_args.file_name:
            warnings.warn(_("Using demo mode. Ignoring input files."), UserWarning)
        parsed_args.file_name = [
            os.path.join(THIS_DIR, "examples/alpha.table"),
            os.path.join(THIS_DIR, "examples/beta.table"),
            os.path.join(THIS_DIR, "examples/gamma.table"),
        ]
    elif len(parsed_args.file_name) <= 1:
        raise ValueError(_("You must provide at least two input files."))

    return parsed_args


def main() -> None:
    """Entry point when calling perprof."""
    try:
        args = set_arguments(sys.argv[1:])

        parser_options, profiler_options = process_arguments(args)

        if args.bokeh:
            # bokeh
            from . import bokeh

            bokeh_profiler = bokeh.Profiler(parser_options, profiler_options)
            bokeh_profiler.plot()
        elif args.mp:
            # matplotlib
            from . import matplotlib

            mp_profiler = matplotlib.Profiler(parser_options, profiler_options)
            mp_profiler.plot()
        elif args.tikz:
            if profiler_options["output_format"] == "pdf" and args.output is None:
                print(
                    _(
                        "ERROR: When using PDF output, you need to provide "
                        "the name of the output file."
                    )
                )
            else:
                # tikz
                from . import tikz

                tikz_profiler = tikz.Profiler(parser_options, profiler_options)
                tikz_profiler.plot()
        elif args.raw:
            # raw
            from . import prof

            print("raw")

            print(prof.Pdata(parser_options, profiler_options))
        elif args.table:
            # table
            from . import prof

            pdata = prof.Pdata(parser_options, profiler_options)
            pdata.print_rob_eff_table()
    except ValueError as error:
        print(error)
    except NotImplementedError as error:
        print(error)
