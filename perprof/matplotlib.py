"""Plot using matplotlib."""

import gettext
import os

import matplotlib
import matplotlib.pyplot as plt

from . import prof

matplotlib.use("Agg")

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation("perprof", os.path.join(THIS_DIR, "locale"))
_ = THIS_TRANSLATION.gettext


class Profiler(prof.Pdata):
    """The profiler using matplotlib."""

    def __init__(self, parser_options, profiler_options):
        """Intialize Profiler with Matplotlib.

        Args:
            parser_options (dict): parser options.
            profiler_options (dict): profiler options
        """
        if profiler_options["output"] is None:
            self.output = f'performance-profile.{profiler_options["output_format"]}'
        else:
            self.output = (
                f'{profiler_options["output"]}.{profiler_options["output_format"]}'
            )
        self.output_format = profiler_options["output_format"]

        # Language for the plot
        translation = gettext.translation(
            "perprof", os.path.join(THIS_DIR, "locale"), [profiler_options["lang"]]
        )
        self.plot_lang = translation.gettext

        prof.Pdata.__init__(self, parser_options, profiler_options)

    # pylint: disable=too-many-branches
    def plot(self):
        """Create the performance profile using matplotlib."""
        self.pre_plot()

        # Hack need to background color
        figure_ = plt.figure()
        plot_ = figure_.add_subplot(111)

        # Set configurations handle when saving the plot
        save_configs = {
            "format": self.output_format,
        }

        if self.page_background:
            if not self.background:
                self.background = self.page_background
            # RGB tuples must be in the range [0,1]
            save_configs["facecolor"] = (
                self.page_background[0] / 255,
                self.page_background[1] / 255,
                self.page_background[2] / 255,
            )
        if self.background:
            plot_.set_facecolor(
                (
                    self.background[0] / 255,
                    self.background[1] / 255,
                    self.background[2] / 255,
                )
            )
            if not self.page_background:
                figure_.patch.set_alpha(0.0)
        if not self.background and not self.page_background:
            save_configs["transparent"] = True
            save_configs["facecolor"] = "none"

        # Define the linestyles
        if self.black_and_white:
            linestyles = ["k-", "k--", "k:", "k-."]
        else:
            linestyles = ["b", "g", "r", "c", "m", "y"]

        # Generate the plot for each solver
        for idx, solver in enumerate(self.solvers):
            plot_.step(
                self.times,
                self.ppsbt[solver],
                linestyles[idx],
                label=solver,
                where="post",
            )

        # Change the xscale to log scale
        if self.semilog:
            plt.gca().set_xscale("log")

        # Axis
        try:
            maxt = min(max(self.times), self.tau)
        except (AttributeError, TypeError):
            maxt = max(self.times)
        plt.gca().set_xlim(1, maxt)
        plt.gca().set_xlabel(self.plot_lang(self.xlabel))
        plt.gca().set_ylim(-0.002, 1.006)
        plt.gca().set_ylabel(self.plot_lang(self.ylabel))
        if self.title is not None:
            plt.gca().set_title(self.plot_lang(self.title))

        # Legend
        plt.gca().legend(loc=4)

        # Help lines
        plt.gca().grid(axis="y", color="0.5", linestyle="-")

        # Save the plot
        plt.savefig(self.output, bbox_inches="tight", pad_inches=0.05, **save_configs)
