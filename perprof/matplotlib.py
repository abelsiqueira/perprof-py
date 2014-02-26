"""
This handle the plot using matplotlib.
"""

import os.path
import matplotlib.pyplot as plt
from . import prof
from .i18n import *

class Profiler(prof.Pdata):
    def __init__(self, setup):
        self.already_scaled = False

        if setup.get_output() is None:
            self.output = 'performance-profile.png'
        else:
            self.output = '{}.png'.format(setup.get_output())
        prof.Pdata.__init__(self, setup)

    def scale(self):
        self.already_scaled = True
        super().scale()

    def plot(self):
        if not self.force:
            try:
                file_ = open(self.output, 'r')
                file_.close()
                raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite').format(self.output))
            except FileNotFoundError:
                pass

        try:
            self.already_scaled
        except AttributeError:
            self.scale()

        try:
            self.ppsbt
        except AttributeError:
            self.set_percent_problems_solved_by_time()

        plt.hold(True)
        for solver in self.solvers:
            plt.plot(self.times, self.ppsbt[solver], label=solver)

        if self.semilog:
            plt.gca().set_xscale('log')

        try:
            maxt = min(max(self.times), self.tau)
        except (AttributeError, TypeError):
            maxt = max(self.times)
        plt.gca().set_xlim(1, maxt)
        plt.gca().set_ylim(0, 1)
        plt.gca().legend(loc=4)
        plt.gca().grid(axis='y', color='0.5', linestyle='-')
        plt.gca().set_title('Performance profile')

        plt.savefig(self.output)
