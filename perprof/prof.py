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
    def __init__(self, parser_options, profiler_options):
        """
        :param dict parser_options: parser configuration
        :param dict profiler_options: profiler configuration
        """
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
        self.subset = parser_options['subset']
        self.mintime = parser_options['mintime']
        self.maxtime = parser_options['maxtime']
        self.compare = parser_options['compare']
        self.unc = parser_options['unc']
        self.infeas_tol = parser_options['infeas_tol']
        self.success = parser_options['success']
        self.free_format = parser_options['free_format']
        self.files = parser_options['files']

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

    def compute_profile(self):
        """
        This should be implemented by the specific profilers.
        """
        raise NotImplementedError()
