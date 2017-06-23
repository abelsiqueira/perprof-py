"""
The functions related with the perform (not the output).
"""

import os.path
import gettext

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

#pylint: disable=R0921
class Pdata(object):
    """
    Store data for performance profile.
    """
    def __init__(self, options):
        """
        :param dict options: configuration
        """
        self.background = options['background']
        self.black_and_white = options['black_and_white']
        self.cache = options['cache']
        self.compare = options['compare']
        self.files = options['files']
        self.force = options['force']
        self.free_format = options['free_format']
        self.infeas_tol = options['infeas_tol']
        self.maxtime = options['maxtime']
        self.mintime = options['mintime']
        self.output_format = options['output_format']
        self.page_background = options['page_background']
        self.pdf_verbose = options['pdf_verbose']
        self.pgfplot_version = options['pgfplot_version']
        self.semilog = options['semilog']
        self.subset = options['subset']
        self.success = options['success']
        self.tablename = options['output']
        self.tau = options['tau']
        self.title = options['title']
        self.unc = options['unc']
        self.xlabel = options['xlabel']
        self.ylabel = options['ylabel']

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

    def compute_profile(self):
        """
        This should be implemented by the specific profilers.
        """
        raise NotImplementedError()
