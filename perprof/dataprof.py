"""
Data profile class, and related functions.

A data profile requires information about the best solution per iteration for
each problem.
Giving a few iterations is enough, as the function will compute the lowest so
far.

The inputs are folders, one for each solver, with files containing the iteration
and function values, one for each problem. In addition, the problem sizes are
necessary as well.
The file structure should be simple::

    <Iteration> <Function value>

The iterations are expected to be in order.
"""

import os.path
import gettext
from . import aux
from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class DataProfile(prof.Pdata):
    """
    Store data for data profile.
    """
    def __init__(self, options):
        """
        :param dict options: configuration
        """
        prof.Pdata.__init__(self, options)
        self.data = {}
        for file_ in options['files']:
            data_tmp, solver_name = self.parse_file(file_)
            self.data[solver_name] = data_tmp
        self.read_sizes_file(options['problem_sizes'])

    def compute_profile(self, rtol = 0.3):
        """
        Compute the data function
        """
        try:
            self.solvers
        except AttributeError:
            self.get_set_solvers()
        try:
            self.problems
        except AttributeError:
            self.get_set_problems()

        profx = set()
        for s in self.solvers:
            for p in self.data[s].keys():
                for k in self.data[s][p]:
                    profx.add( k/(self.sizes[p]+1) )
        self.profx = [x for x in profx]
        self.profx.sort()
        maxr = self.profx[-1]
        self.profx.append(maxr * 1.01)

        self.prof = {}
        for s in self.solvers:
            self.prof[s] = [0] * len(self.profx)

        I = set([0])

        for p in self.problems:
            fmax = self.data[self.solvers[0]][p][0]
            fmin = max([self.data[s][p][-1] for s in self.solvers])
            ftol = fmin + rtol * (fmax - fmin)
            splx = self.sizes[p] + 1
            for s in self.solvers:
                try:
                    # Find index in which fi <= ftol
                    k = next(i for (i,f) in enumerate(self.data[s][p]) if f <= ftol)
                    first_change = True
                    for (j,x) in enumerate(self.profx):
                        if k/splx <= x:
                            self.prof[s][j] += 1
                            if first_change:
                                I.add(j)
                                first_change = False
                except:
                    pass

        I = sorted(list(I))
        Np = len(self.problems)
        self.profx = [self.profx[i] for i in I]
        self.profx.append(self.profx[-1] * 1.05)
        for s in self.solvers:
            self.prof[s] = [self.prof[s][i]/Np for i in I]
            self.prof[s].append(self.prof[s][-1])

    def parse_file(self, foldername):
        """
        Parse one data profile folder.
        """
        data = {}
        for fname in os.listdir(foldername):
            fname = os.path.join(foldername, fname)
            _, p = os.path.split(fname)
            p, _ = os.path.splitext(p)
            lastline = open(fname).readlines()[-1]
            N, _ = lastline.split()
            N = int(N)
            data[p] = [float('inf')] * N
            with open(fname) as _f:
                for line in _f:
                    i, F = line.split()
                    data[p][int(i)-1] = float(F)

            # Update the iterations to show the best so far (and fill gaps)
            for i in range(1, N):
                data[p][i] = min(data[p][i], data[p][i-1])

        if not data:
            raise ValueError(
                    _("ERROR: List of problems (intersected with subset, if any) is empty"))
        return data, os.path.split(os.path.abspath(foldername))[1]

    def read_sizes_file(self, fname):
        """
        Parse the sizes file.
        """
        self.sizes = {}
        with open(fname) as _f:
            for line in _f:
                sline = line.split()
                if sline[0][0] == '#':
                    continue
                self.sizes[sline[0]] = int(sline[1])
