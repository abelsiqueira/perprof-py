"""Plot using bokeh."""

import gettext
import os.path

import bokeh.plotting as plt

from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation("perprof", os.path.join(THIS_DIR, "locale"))
_ = THIS_TRANSLATION.gettext

# TODO: Add more colors to list and compatible with others backend
BOKEH_COLOR_LIST = ["blue", "green", "red", "cyan", "magenta", "yellow"]


class Profiler(prof.Pdata):
    """Interactive performance profile generator using Bokeh backend.

    This class creates interactive HTML performance profile plots using Bokeh.
    The resulting plots are fully interactive with zooming, panning, hover tooltips,
    and responsive design suitable for web deployment or standalone viewing.

    Bokeh profiles offer advantages over static plots for data exploration:
    - Interactive zoom and pan for detailed analysis
    - Hover tooltips showing exact values
    - Legend-based line toggling for visual comparison
    - Responsive layout adapting to different screen sizes
    - Self-contained HTML files requiring no server

    The profiler generates line plots showing the cumulative distribution of solver
    performance ratios with smooth curves instead of traditional step plots.

    Attributes:
        output (str): Output HTML filename including extension.
        output_format (str): File format, always "html" for Bokeh.
        plot_lang (function): Localization function for plot text.

    Example:
        Creating an interactive Bokeh profiler:

        ```python
        from perprof.bokeh import Profiler

        parser_opts = {
            "files": ["solver1.txt", "solver2.txt"],
            "success": ["converged"],
            "free_format": True
        }
        profiler_opts = {
            "output": "interactive_comparison",
            "output_format": "html",
            "semilog": True,
            "title": "Interactive Performance Profile",
            "lang": "en"
        }
        profiler = Profiler(parser_opts, profiler_opts)
        profiler.plot()  # Creates interactive_comparison.html
        ```
    """

    def __init__(self, parser_options, profiler_options):
        """Initialize Bokeh-based interactive performance profiler.

        Args:
            parser_options (dict): Data parsing configuration including:
                - files: List of solver data files to process
                - success: Success criteria for solver convergence
                - maxtime/mintime: Time filtering bounds
                - compare: Performance metric to compare (default: "time")
                - subset: Optional problem subset restriction
            profiler_options (dict): Visualization configuration including:
                - output: Output filename prefix (extension auto-added)
                - output_format: Must be "html" for Bokeh backend
                - semilog: Use logarithmic x-axis scaling
                - lang: Language for plot labels
                - title/xlabel/ylabel: Plot text customization

        Note:
            Color customization and black_and_white options are not supported
            in the current Bokeh implementation. The profiler uses a fixed
            color palette defined in BOKEH_COLOR_LIST.

        Example:
            ```python
            parser_opts = {"files": ["data1.txt"], "success": ["converged"]}
            profiler_opts = {"output": "plot", "output_format": "html", "lang": "en"}
            profiler = Profiler(parser_opts, profiler_opts)
            ```
        """
        if profiler_options["output"] is None:
            self.output = f"performance-profile.{profiler_options['output_format']}"
        else:
            self.output = (
                f"{profiler_options['output']}.{profiler_options['output_format']}"
            )
        self.output_format = profiler_options["output_format"]

        # Language for the plot
        translation = gettext.translation(
            "perprof", os.path.join(THIS_DIR, "locale"), [profiler_options["lang"]]
        )
        self.plot_lang = translation.gettext

        prof.Pdata.__init__(self, parser_options, profiler_options)

    def plot(self):
        """Generate and save the interactive performance profile plot.

        Creates an interactive HTML plot using Bokeh showing the cumulative distribution
        of performance ratios for each solver. The plot includes smooth line curves
        representing solver performance with interactive features for data exploration.

        Interactive features:
        - Zoom and pan controls for detailed analysis
        - Hover tooltips (planned feature, not yet implemented)
        - Legend entries for toggling solver visibility
        - Responsive layout for different screen sizes
        - Grid lines with customizable transparency

        Plot characteristics:
        - Line plots instead of step plots (smoother appearance)
        - Logarithmic x-axis scaling (if semilog=True)
        - Fixed color palette cycling through BOKEH_COLOR_LIST
        - Automatic axis scaling and range setting
        - Bottom-right legend positioning

        The plot is saved as a self-contained HTML file that can be opened
        in any web browser without requiring a Bokeh server.

        Note:
            The plot currently shows axis labels with x/y swapped in the figure
            initialization. This appears to be a bug in the current implementation.

        Example:
            ```python
            # After creating profiler instance (see __init__ example)
            profiler.plot()  # Creates interactive HTML file
            ```
        """
        self.pre_plot()

        plt.output_file(self.output, title=self.plot_lang(self.title))

        # Axis
        try:
            maxt = min(max(self.times), self.tau)
        except (AttributeError, TypeError):
            maxt = max(self.times)

        boken_plot_options = {"x_range": [1, maxt], "y_range": [0, 1]}

        # Change the xscale to log scale
        if self.semilog:
            boken_plot_options["x_axis_type"] = "log"

        p = plt.figure(
            title=self.plot_lang(self.title),
            x_axis_label=self.plot_lang(self.ylabel),
            y_axis_label=self.plot_lang(self.xlabel),
            **boken_plot_options,
        )

        for idx, solver in enumerate(self.solvers):
            p.line(
                self.times,
                self.ppsbt[solver],
                legend=solver,
                line_width=2,
                line_color=BOKEH_COLOR_LIST[idx % len(BOKEH_COLOR_LIST)],
            )

        # Legend
        p.legend.orientation = "bottom_right"

        # Help lines
        p.grid.grid_line_color = "black"
        p.grid.grid_line_alpha = 0.5

        # Save the plot
        plt.save(p)
