"""
The functions related with the perform (not the output).
"""

import os.path
import gettext
from . import parse

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

def load_data(parser_options):
    """
    Load the data.

    :param dict parser_options: the configuration dicionary
    """
    data = {}
    for file_ in parser_options['files']:
        data_tmp, solver_name = parse.parse_file(file_, parser_options)
        data[solver_name] = data_tmp
    return data

#pylint: disable=R0921
class Pdata(object):
    """
    Store data for performance profile.
    """
    def __init__(self, parser_options, profiler_options):
        """
        :param dict parser_options: parser configuration
        :param dict profiler_options: profiler configuration
        """
        self.data = load_data(parser_options)
        self.cache = profiler_options['cache']
        self.force = profiler_options['force']
        self.semilog = profiler_options['semilog']
        self.black_and_white = profiler_options['black_and_white']
        self.background = profiler_options['background']
        self.page_background = profiler_options['page_background']
        self.pdf_verbose = profiler_options['pdf_verbose']
        self.output_format = profiler_options['output_format']
        self.pgfplot_version = profiler_options['pgfplot_version']
        self.tau = profiler_options['tau']
        self.title = profiler_options['title']
        self.xlabel = profiler_options['xlabel']
        self.ylabel = profiler_options['ylabel']
        self.already_scaled = False

        self.tablename = profiler_options['output']

    def __repr__(self):
        try:
            self.solvers
        except AttributeError:
            self.get_set_solvers()
        try:
            self.problems
        except AttributeError:
            self.get_set_problems()

        str2output = ' ' * 18

        for solver in self.solvers:
            if len(solver) > 16:
                str2output += '{:>16}  '.format(solver[-16:])
            else:
                str2output += '{space}{:>16}  '.format(solver,
                        space=' ' * (len(solver) - 16))
        str2output += '\n'

        for problem in self.problems:
            str2output += '{:>16}  '.format(problem)
            for solver in self.solvers:
                try:
                    str2output += '{space}{:8.4} '.format(
                            self.data[solver][problem]["time"], space=' ' * 8)
                except KeyError:
                    str2output += '{}inf  '.format(13 * ' ')
            str2output += '\n'

        return str2output[:-2]

    def get_set_solvers(self):
        """
        Get the set of solvers to use.

        :return: list of solvers
        """
        try:
            self.solvers
        except AttributeError:
            self.solvers = sorted(list(self.data.keys()))
        return self.solvers

    def get_set_problems(self):
        """
        Get the set of problems to use.

        :return: list of problems
        """
        try:
            self.problems
            self.number_problems
        except AttributeError:
            problems = set()
            for i in self.data:
                for j in self.data[i]:
                    problems.add(j)
            self.problems = problems
            self.number_problems = len(problems)
        return self.problems

    def scale(self):
        """
        Scale time.
        """
        try:
            self.solvers
        except AttributeError:
            self.get_set_solvers()
        try:
            self.problems
        except AttributeError:
            self.get_set_problems()

        times_set = set()
        for problem in self.problems:
            for solver in self.solvers:
                try:
                    self.data[solver][problem]["time"]
                except (KeyError, TypeError):
                    self.data[solver][problem] = {
                            "time": float('inf'),
                            "fval": float('inf') }

            min_fval = min([self.data[s][problem]["fval"]
                    for s in self.data.keys()])
            if min_fval < float('inf'):
                min_time = min([self.data[s][problem]["time"]
                    for s in self.data.keys()
                        if self.data[s][problem]["fval"] < min_fval +
                        abs(min_fval)*1e-3 + 1e-6])
            else:
                min_time = min([self.data[s][problem]["time"]
                    for s in self.data.keys()])

            for solver in self.solvers:
                try:
                    self.data[solver][problem]["time"] = \
                            self.data[solver][problem]["time"] / min_time
                except ZeroDivisionError:
                    self.data[solver][problem] = {"time": float('inf')}
                if self.data[solver][problem]["time"] < float('inf'):
                    times_set.add(self.data[solver][problem]["time"])
        if not times_set:
            raise ValueError(_("ERROR: problem set is empty"))

        self.times = [x for x in times_set]
        self.times.sort()

        self.already_scaled = True

    def set_percent_problems_solved_by_time(self):
        """
        Set the percent of problems solved by time.
        """
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
                raise ValueError(_("ERROR:") + solver +
                    _(" has no solved problems. Verify the 'success' flag."))

    def plot(self):
        """
        This should be implemented by a child of this class.
        """
        raise NotImplementedError()

    def print_rob_eff_table(self):
        if not self.already_scaled:
            self.scale()

        try:
            self.ppsbt
        except AttributeError:
            self.set_percent_problems_solved_by_time()

        import sys
        if self.tablename is None:
            output = sys.stdout
            print("Solvers    | Robust  | Effic")
            for solver in self.solvers:
                print('{:10s} | {:6.3f}% | {:6.3f}%'.format(solver,
                    round(100*self.ppsbt[solver][-1],3),
                    round(100*self.ppsbt[solver][0],3)))
        else:
            output = '{}.tex'.format(self.tablename)
            output = os.path.abspath(output)

            str2output = ['\\begin{tabular}{|c|r|r|} \\hline',
                    'Solver & Robustness & Efficiency \\\\ \\hline']
            for solver in self.solvers:
                str2output.append('{} & {} \% & {} \% \\\\ \\hline'.format(solver,
                    round(100*self.ppsbt[solver][-1],3),
                    round(100*self.ppsbt[solver][0],3)))
            str2output.append('\\end{tabular}')

            with open(output, 'w') as file_:
                file_.write('\n'.join(str2output))
