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

def load_data(setup):
    """
    Load the data.

    :param setup: the setup configurations
    :type setup: main.PerProfSetup
    """
    if setup.get_subset():
        with open(setup.get_subset(), 'r') as subset_file:
            subset = [l.strip() for l in subset_file]
        if len(subset) == 0:
            raise AttributeError(_("ERROR: Subset is empty"))
    else:
        subset = []

    data = {}
    for file_ in setup.get_files():
        data_tmp, solver_name = parse.parse_file(file_, subset,
                setup.get_success(), setup.get_maxtime(), setup.using_free_format())
        data[solver_name] = data_tmp
    return data

#pylint: disable=R0921
class Pdata(object):
    def __init__(self, setup):
        self.data = load_data(setup)
        self.cache = setup.using_cache()
        self.force = setup.using_force()
        self.semilog = setup.using_semilog()
        self.black_and_white = setup.using_black_and_white()
        self.background = setup.get_background()
        self.page_background = setup.get_page_background()
        self.pdf_verbose = setup.get_pdf_verbose()
        self.output_format = setup.get_output_format()
        self.pgfplot_version = setup.get_pgfplot_version()
        self.tau = setup.get_tau()
        self.already_scaled = False

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
                            self.data[solver][problem], space=' ' * 8)
                except KeyError:
                    str2output += '{}inf  '.format(13 * ' ')
            str2output += '\n'

        return str2output[:-2]

    def get_set_solvers(self):
        try:
            self.solvers
        except AttributeError:
            self.solvers = sorted(list(self.data.keys()))
        return self.solvers

    def get_set_problems(self):
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
            min_time = float('inf')
            for solver in self.solvers:
                try:
                    if self.data[solver][problem] < min_time:
                        min_time = self.data[solver][problem]
                except KeyError:
                    pass
            for solver in self.solvers:
                try:
                    self.data[solver][problem] = self.data[solver][problem] / min_time
                except (KeyError, ZeroDivisionError):
                    self.data[solver][problem] = float('inf')
                if self.data[solver][problem] < float('inf'):
                    times_set.add(self.data[solver][problem])
        if not times_set:
            raise ValueError(_("ERROR: problem set is empty"))

        self.times = [x for x in times_set]
        self.times.sort()

        self.already_scaled = True

    def set_percent_problems_solved_by_time(self):
        # ppsbt = Percent Problems Solved By Time
        self.ppsbt = {}
        for solver in self.solvers:
            self.ppsbt[solver] = []
            for time in self.times:
                aux = 0
                for problem in self.problems:
                    if time >= self.data[solver][problem]:
                        aux += 1
                self.ppsbt[solver].append(aux / self.number_problems)

    def plot(self):
        """
        This should be implemented by a child of this class.
        """
        raise NotImplementedError()
