"""
The functions related with the perform (not the output).
"""

import pprint
import math
from . import parse

def load_data(setup):
    """
    Load the data.

    :param setup: the setup configurations
    :type setup: main.PerProfSetup
    """
    try:
        with open(setup.get_subset(), 'r') as subset_file:
            subset = [l.strip() for l in subset_file]
    except:
        subset = []
    data = {}
    for f in setup.get_files():
        data_tmp, solver_name = parse.parse_file(f, subset,
                setup.using_free_format())
        data[solver_name] = data_tmp
    return data

class Pdata:
    def __init__(self, setup):
        self.data = load_data(setup)
        self.cache = setup.using_cache()
        self.force = setup.using_force()
        self.semilog = setup.using_semilog()
        self.bw = setup.using_black_and_white()
        self.output_format = setup.get_output_format()
        self.pgfplot_version = setup.get_pgfplot_version()
        self.tau = setup.get_tau()

    def __repr__(self):
        try:
            self.solvers
        except:
            self.get_set_solvers()
        try:
            self.problems
        except:
            self.get_set_problems()

        str2output = ' ' * 18

        for s in self.solvers:
            if len(s) > 16:
                str2output += '{:>16}  '.format(s[-16:])
            else:
                str2output += '{space}{:>16}  '.format(s,
                        space = ' ' * (len(s) - 16))
        str2output += '\n'

        for p in self.problems:
            str2output += '{:>16}  '.format(p)
            for s in self.solvers:
                try:
                    str2output += '{space}{:8.4}  '.format(self.data[s][p],
                            space = ' ' * 8)
                except:
                    str2output += '{}inf  '.format(13 * ' ')
            str2output += '\n'

        return str2output[:-2]

    def get_set_solvers(self):
        try:
            self.solvers
        except:
            self.solvers = sorted(list(self.data.keys()))
        return self.solvers

    def get_set_problems(self):
        try:
            self.problems
            self.number_problems
        except:
            p = set()
            for i in self.data:
                for j in self.data[i]:
                    p.add(j)
            self.problems = p
            self.number_problems = len(p)
        return self.problems

    def scale(self):
        """
        Scale time.
        """
        try:
            self.solvers
        except:
            self.get_set_solvers()
        try:
            self.problems
        except:
            self.get_set_problems()

        self.times = set()
        for p in self.problems:
            min_time = float('inf')
            for s in self.solvers:
                try:
                    if self.data[s][p] < min_time:
                        min_time = self.data[s][p]
                except:
                    pass
            for s in self.solvers:
                try:
                    self.data[s][p] = self.data[s][p] / min_time
                except:
                    self.data[s][p] = float('inf')
                if (self.data[s][p] < float('inf')):
                    self.times.add(self.data[s][p])
        if len(self.times) == 0:
            raise ValueError("ERROR: problem set is empty")
        self.times = [x for x in self.times]
        self.times.sort()

    def set_percent_problems_solved_by_time(self):
        # ppsbt = Percent Problems Solved By Time
        self.ppsbt = {}
        for s in self.solvers:
            self.ppsbt[s] = []
            for t in self.times:
                aux = 0
                for p in self.problems:
                    if t >= self.data[s][p]:
                        aux += 1
                self.ppsbt[s].append(aux / self.number_problems)

    def plot(self):
        """
        This should be implemented by a child of this class.
        """
        raise NotImplementedError()
