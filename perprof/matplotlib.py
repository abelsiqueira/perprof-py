"""
This handle the plot using matplotlib.
"""

import os.path
import gettext
import matplotlib.pyplot as plt
from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class Profiler(prof.Pdata):
    def __init__(self, setup):
        self.already_scaled = False

        if setup.get_output() is None:
            self.output = 'performance-profile.png'
        else:
            self.output = '{}.png'.format(setup.get_output())
        prof.Pdata.__init__(self, setup)

    def plot(self):
        if not self.force:
            try:
                file_ = open(self.output, 'r')
                file_.close()
                raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite').format(self.output))
            except FileNotFoundError:
                pass

        if not self.already_scaled:
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
