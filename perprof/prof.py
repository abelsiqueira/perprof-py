"""The functions related with the perform (not the output)."""

import gettext
import os.path
import sys

from . import parse

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation("perprof", os.path.join(THIS_DIR, "locale"))
_ = THIS_TRANSLATION.gettext


def load_data(parser_options):
    """
    Load the data.

    Args:
        parser_options (dict): the configuration dicionary
    """
    data = {}
    for file_ in parser_options["files"]:
        data_tmp, solver_name = parse.parse_file(file_, parser_options)
        data[solver_name] = data_tmp
    return data


class Pdata:
    """Store data for performance profile."""

    def __init__(self, parser_options, profiler_options):
        """Initialize Pdata.

        Args:
            parser_options (dict): parser configuration.
            profiler_options (dict): profiler configuration
        """
        self.data = load_data(parser_options)
        self.cache = profiler_options["cache"]
        self.force = profiler_options["force"]
        self.semilog = profiler_options["semilog"]
        self.black_and_white = profiler_options["black_and_white"]
        self.background = profiler_options["background"]
        self.page_background = profiler_options["page_background"]
        self.pdf_verbose = profiler_options["pdf_verbose"]
        self.output_format = profiler_options["output_format"]
        self.pgfplot_version = profiler_options["pgfplot_version"]
        self.tau = profiler_options["tau"]
        self.title = profiler_options["title"]
        self.xlabel = profiler_options["xlabel"]
        self.ylabel = profiler_options["ylabel"]
        self.already_scaled = False
        self.tablename = profiler_options["output"]

        self.solvers = sorted(list(self.data.keys()))
        self.problems = {x for v in self.data.values() for x in v}
        self.number_problems = len(self.problems)

    def __repr__(self):
        """Return a representation of the Pdata object."""
        str2output = " " * 18

        for solver in self.solvers:
            str2output += f"{solver[-16:]:>16}  "
        str2output += "\n"

        for problem in self.problems:
            str2output += f"{problem:>16}  "
            for solver in self.solvers:
                try:
                    str2output += " " * 8 + f'{self.data[solver][problem]["time"]:8.4} '
                except KeyError:
                    str2output += " " * 13 + "inf  "
            str2output += "\n"

        return str2output[:-2]

    def get_set_solvers(self):
        """
        Get the set of solvers to use.

        Returns:
            solvers (list[dict]): list of solvers
        """
        return self.solvers

    def get_set_problems(self):
        """
        Get the set of problems to use.

        Returns:
            problems (list[str]): list of problems
        """
        return self.problems

    def scale(self):
        """Scale time."""
        times_set = set()
        for problem in self.problems:
            for solver in self.solvers:
                try:
                    self.data[solver][problem]["time"]
                except (KeyError, TypeError):
                    self.data[solver][problem] = {
                        "time": float("inf"),
                        "fval": float("inf"),
                    }

            min_fval = min(v[problem]["fval"] for v in self.data.values())
            if min_fval < float("inf"):
                min_time = min(
                    v[problem]["time"]
                    for v in self.data.values()
                    if v[problem]["fval"] < min_fval + abs(min_fval) * 1e-3 + 1e-6
                )
            else:
                min_time = min(v[problem]["time"] for v in self.data.values())

            for solver in self.solvers:
                try:
                    self.data[solver][problem]["time"] = (
                        self.data[solver][problem]["time"] / min_time
                    )
                except ZeroDivisionError:
                    self.data[solver][problem] = {"time": float("inf")}
                if self.data[solver][problem]["time"] < float("inf"):
                    times_set.add(self.data[solver][problem]["time"])
        if not times_set:
            raise ValueError(_("ERROR: problem set is empty"))

        self.times = sorted(times_set)
        maxt = self.times[-1]
        self.times.append(maxt * 1.05)

        self.already_scaled = True

    def set_percent_problems_solved_by_time(self):
        """Set the percent of problems solved by time."""
        # ppsbt = Percent Problems Solved By Time
        self.ppsbt = {}
        for solver in self.solvers:
            self.ppsbt[solver] = []
            for time in self.times:
                aux = 0
                for problem in self.problems:
                    if time >= self.data[solver][problem]["time"]:
                        aux += 1
                self.ppsbt[solver].append(aux / self.number_problems)
            if self.ppsbt[solver][-1] == 0:
                raise ValueError(
                    _("ERROR:")
                    + solver
                    + _(" has no solved problems. Verify the 'success' flag.")
                )

    def pre_plot(self):
        """Run plot-related checks and processing."""
        if self.force and self.output != sys.stdout and os.path.exists(self.output):
            raise ValueError(
                _("ERROR: File {} exists.\nUse `-f` to overwrite").format(self.output)
            )

        if not self.already_scaled:
            self.scale()

        try:
            self.ppsbt
        except AttributeError:
            self.set_percent_problems_solved_by_time()

    def plot(self):
        """Generate the plot."""
        raise NotImplementedError()

    def print_rob_eff_table(self):
        """Print table of robustness and efficiency."""
        if not self.already_scaled:
            self.scale()

        try:
            self.ppsbt
        except AttributeError:
            self.set_percent_problems_solved_by_time()

        if self.tablename is None:
            output = sys.stdout
            print("Solvers    | Robust  | Effic")
            for solver in self.solvers:
                robustness = round(100 * self.ppsbt[solver][-1], 3)
                efficiency = round(100 * self.ppsbt[solver][0], 3)
                print(f"{solver:10} | {robustness:6.3f}% | {efficiency:6.3f}%")
        else:
            output = f"{self.tablename}.tex"
            output = os.path.abspath(output)

            str2output = [
                "\\begin{tabular}{|c|r|r|} \\hline",
                "Solver & Robustness & Efficiency \\\\ \\hline",
            ]
            for solver in self.solvers:
                robustness = round(100 * self.ppsbt[solver][-1], 3)
                efficiency = round(100 * self.ppsbt[solver][0], 3)
                str2output.append(
                    f"{solver} & {robustness} \\% & {efficiency} \\% \\\\ \\hline"
                )
            str2output.append("\\end{tabular}")

            with open(output, "w", encoding="utf-8") as file_:
                file_.write("\n".join(str2output))
