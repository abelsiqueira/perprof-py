"""Plot using tikz."""

import gettext
import os.path
import subprocess
import sys

from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation("perprof", os.path.join(THIS_DIR, "locale"))
_ = THIS_TRANSLATION.gettext


class Profiler(prof.Pdata):
    """Publication-quality performance profile generator using TikZ/PGFPlots.

    This class creates high-quality LaTeX-based performance profile plots using
    TikZ and PGFPlots. The output is ideal for academic publications, technical
    reports, and presentations requiring vector graphics with consistent typography.

    TikZ/PGFPlots advantages:
    - True vector graphics with infinite scalability
    - Consistent fonts matching LaTeX document typography
    - Professional mathematical notation and symbols
    - Fine-grained control over plot appearance
    - Direct integration with LaTeX documents
    - Support for both standalone and embedded figures

    The profiler generates either standalone LaTeX documents or TikZ code that
    can be embedded into larger documents. It supports both color and black-and-white
    output with extensive line style and color customization.

    Attributes:
        output (str|TextIO): Output filename or file handle (stdout for None).
        standalone (bool): Whether to generate standalone LaTeX document.
        output_format (str): Target format ("tex" or "pdf").
        plot_lang (function): Localization function for plot text.

    Example:
        Creating a TikZ profiler for publication-quality output:

        ```python
        from perprof.tikz import Profiler

        parser_opts = {
            "files": ["solver1.txt", "solver2.txt"],
            "success": ["converged"],
            "free_format": True
        }
        profiler_opts = {
            "output": "publication_figure",
            "output_format": "pdf",
            "standalone": True,
            "black_and_white": False,
            "title": "Performance Profile Comparison",
            "lang": "en"
        }
        profiler = Profiler(parser_opts, profiler_opts)
        profiler.plot()  # Creates publication_figure.tex and compiles to PDF
        ```
    """

    def __init__(self, parser_options, profiler_options):
        """Initialize TikZ/PGFPlots-based performance profiler.

        Args:
            parser_options (dict): Data parsing configuration including:
                - files: List of solver data files to process
                - success: Success criteria for solver convergence
                - maxtime/mintime: Time filtering bounds
                - compare: Performance metric to compare (default: "time")
                - subset: Optional problem subset restriction
            profiler_options (dict): Visualization configuration including:
                - output: Output filename prefix (None for stdout)
                - output_format: Target format ("tex" or "pdf")
                - standalone: Generate standalone LaTeX document
                - black_and_white: Use monochrome line styles
                - semilog: Use logarithmic x-axis scaling
                - lang: Language for plot labels
                - title/xlabel/ylabel: Plot text customization
                - pgfplot_version: PGFPlots compatibility version
                - background/page_background: Color customization

        Note:
            TikZ backend has solver limits: 13 for black-and-white plots,
            30 for color plots. This is due to the finite number of
            predefined line styles and colors in the TikZ implementation.

        Example:
            ```python
            parser_opts = {"files": ["data1.txt"], "success": ["converged"]}
            profiler_opts = {"output": "plot", "output_format": "pdf",
                           "standalone": True, "lang": "en"}
            profiler = Profiler(parser_opts, profiler_opts)
            ```
        """
        if profiler_options["output"] is None:
            self.output = sys.stdout
        else:
            self.output = f"{profiler_options['output']}.tex"
            self.output = os.path.abspath(self.output)
        self.standalone = profiler_options["standalone"]
        self.output_format = profiler_options["output_format"]

        # Language for the plot
        translation = gettext.translation(
            "perprof", os.path.join(THIS_DIR, "locale"), [profiler_options["lang"]]
        )
        self.plot_lang = translation.gettext

        prof.Pdata.__init__(self, parser_options, profiler_options)

    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    def plot(self):
        """Generate and save the TikZ/PGFPlots performance profile.

        Creates publication-quality LaTeX code for performance profiles using TikZ
        and PGFPlots packages. The output can be either a standalone LaTeX document
        or TikZ code for embedding in larger documents.

        LaTeX generation process:
        1. Document structure (if standalone): documentclass, packages, setup
        2. Color and line style definitions based on solver count and B&W setting
        3. PGFPlots axis environment with scaling, labels, and grid
        4. Data plots using step functions with appropriate styling
        5. Legend and plot finalization
        6. Optional PDF compilation via pdflatex

        Key features:
        - Step plots using PGFPlots \\addplot commands
        - Logarithmic x-axis scaling (if semilog=True)
        - Extensive color and line style combinations
        - Professional typography matching document fonts
        - Automatic PDF compilation for output_format="pdf"
        - Background color support with RGB definitions
        - Grid lines and legend positioning

        The method validates solver count limits (13 for B&W, 30 for color)
        and generates appropriate error messages for violations.

        Raises:
            ValueError: If too many solvers for the chosen style (B&W vs color).
            subprocess-related exceptions: If PDF compilation fails.

        Example:
            ```python
            # After creating profiler instance (see __init__ example)
            profiler.plot()  # Creates .tex file and optionally compiles to PDF
            ```
        """
        self.pre_plot()

        if self.black_and_white and len(self.solvers) > 13:
            raise ValueError(
                _("ERROR: Maximum numbers of solvers in black and white plot is 13.")
            )
        if not self.black_and_white and len(self.solvers) > 30:
            raise ValueError(
                _("ERROR: Maximum numbers of solvers in color plot is 30.")
            )

        maxt = max(self.times)
        try:
            maxt = min(maxt, self.tau)
        except (AttributeError, TypeError):
            self.tau = maxt

        str2output = []

        if self.standalone or self.output_format == "pdf":
            str2output.append("\\documentclass{standalone}")
            str2output.append("\\usepackage[utf8]{inputenc}")
            str2output.append("\\usepackage[T1]{fontenc}")
            str2output.append("\\usepackage{tikz}")
            str2output.append("\\usepackage{pgfplots}")
            if self.pgfplot_version is not None:
                str2output.append(f"\\pgfplotsset{{compat={self.pgfplot_version}}}")
            else:
                str2output.append(
                    "\\pgfplotsset{compat=newest,compat/show suggested version=false}"
                )
            if self.page_background:
                str2output.append(
                    "\\definecolor{pagebg}{RGB}{"
                    + ",".join(str(x) for x in self.page_background)
                    + "}"
                )
                str2output.append("\\pagecolor{pagebg}")
            str2output.append("\\begin{document}")
        else:
            str2output.append("\\begin{center}")
        str2output.append("\\begin{tikzpicture}")

        if self.semilog:
            str2output.append("  \\begin{semilogxaxis}[const plot,")
        else:
            str2output.append("  \\begin{axis}[const plot,")
        if self.black_and_white:
            lines = ["dashed", "dotted", "dashdotted", "dashdotdotted"]
            types = ["", "loosely ", "densely "]
            str2output.append("  cycle list={")
            aux = ["solid"]
            for k in range(0, len(self.solvers)):
                i = k % len(lines)
                j = k // len(lines)
                aux.append(f"  {{{types[j]}{lines[i]}}}")
            str2output.append(",\n".join(aux) + "},")
        else:
            colors = [
                "blue",
                "red",
                "black",
                "brown",
                "green!80!black",
                "magenta!80!black",
            ]
            lines = ["solid", "dashed", "dotted", "dashdotted", "dashdotdotted"]
            str2output.append("  cycle list={")
            aux = []
            for k in range(0, len(self.solvers)):
                i = k % len(colors)
                j = k // len(colors)
                aux.append(f"  {{{colors[i]},{lines[j]}}}")
            str2output.append(",\n".join(aux) + "},")
        if self.background:
            red, green, blue = self.background
            str2output.append(
                "axis background/.style="
                f"{{fill={{rgb,255:red,{red};green,{green};blue,{blue}}}}},"
            )
        if len(self.solvers) > 5:
            legend_pos = "outer north east"
        else:
            legend_pos = "south east"
        if self.title is None:
            title = ""
        else:
            title = f"title={{{self.plot_lang(self.title)}}},"

        xlabel = self.plot_lang(self.xlabel)
        ylabel = self.plot_lang(self.ylabel)

        str2output.append(
            f"""xmin=1, xmax={maxt:.2f},
                ymin=-0.003, ymax=1.003,
                ymajorgrids,
                ytick={{0,0.2,0.4,0.6,0.8,1.0}},
                xlabel={{{xlabel}}},
                ylabel={{{ylabel}}},{title}
                legend pos={{{legend_pos}}},
                width=\\textwidth
            ]"""
        )

        for solver in self.solvers:
            this_ppsbt = self.ppsbt[solver]
            str2output.append("  \\addplot+[mark=none, thick] coordinates {")
            str2output.append(f"    ({self.times[0]:.4f},{this_ppsbt[0]:.4f})")
            last_t = round(self.times[0], 4)
            last_p = round(self.ppsbt[solver][0], 4)
            for i in range(1, len(self.times) - 1):
                dx = round(self.times[i], 4) - last_t
                dx2 = round(self.times[i + 1], 4) - last_t
                dy = round(this_ppsbt[i], 4) - last_p
                dy2 = round(this_ppsbt[i + 1], 4) - last_p
                if dx * dy2 == dy * dx2:
                    continue
                if self.times[i] <= self.tau:
                    time = round(self.times[i], 4)
                    ppsbt = round(self.ppsbt[solver][i], 4)
                    str2output.append(f"    ({time:.4f},{ppsbt:.4f})")
                    last_t = time
                    last_p = ppsbt
                else:
                    break
            j = len(self.times) - 1
            str2output.append(f"    ({self.times[j]:.4f},{this_ppsbt[j]:.4f})")
            str2output.append("  };")
            str2output.append(f"  \\addlegendentry{{{solver}}}")

        if self.semilog:
            str2output.append("  \\end{semilogxaxis}")
        else:
            str2output.append("  \\end{axis}")
        str2output.append("\\end{tikzpicture}")
        if self.standalone or self.output_format == "pdf":
            str2output.append("\\end{document}")
        else:
            str2output.append("\\end{center}\n")

        try:
            with open(self.output, "w", encoding="utf-8") as file_:
                file_.write("\n".join(str2output))

            if self.output_format == "pdf":
                if self.pdf_verbose:
                    mode = "nonstopmode"
                else:
                    mode = "batchmode"
                subprocess.check_call(
                    [
                        "pdflatex",
                        "-interaction",
                        mode,
                        "-output-directory",
                        os.path.dirname(self.output),
                        self.output,
                    ]
                )
        except TypeError:
            # When using stdout
            print(str2output, file=self.output)
