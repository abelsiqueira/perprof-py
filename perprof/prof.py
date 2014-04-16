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
    def __init__(self, parser_options, profile_options):
        """
        :param dict parser_options: parser configuration
        :param dict profile_options: profiler configuration
        """
        self.data = load_data(parser_options)
        self.cache = profile_options['cache']
        self.force = profile_options['force']
        self.semilog = profile_options['semilog']
        self.black_and_white = profile_options['black_and_white']
        self.background = profile_options['background']
        self.page_background = profile_options['page_background']
        self.pdf_verbose = profile_options['pdf_verbose']
        self.output_format = profile_options['output_format']
        self.pgfplot_version = profile_options['pgfplot_version']
        self.tau = profile_options['tau']
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
                    if time >= self.data[solver][problem]:
                        aux += 1
                self.ppsbt[solver].append(aux / self.number_problems)
            if self.ppsbt[solver][-1] == 0:
                raise ValueError(_("ERROR: solver " + solver +
                    " has no solved problems. Verify the 'success' flag."))

    def plot(self):
        """
        This should be implemented by a child of this class.
        """
        raise NotImplementedError()
