"""
This handle the plot using matplotlib.
"""

import os.path
from . import prof
import matplotlib.pyplot as plt

import gettext

this_dir, this_filename = os.path.split(__file__)
t = gettext.translation('perprof', os.path.join(this_dir, 'locale'))
_ = t.gettext

class Profiler(prof.Pdata):
    def __init__(self, setup):
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
                f = open(self.output, 'r')
                f.close()
                raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite').format(self.output))
            except FileNotFoundError:
                pass

        try:
            self.already_scaled
        except:
            self.scale()

        try:
            self.ppsbt
        except:
            self.set_percent_problems_solved_by_time()

        plt.hold(True)
        for s in self.solvers:
            plt.plot(self.times, self.ppsbt[s], label=s)

        if self.semilog:
            plt.gca().set_xscale('log')

        try:
            maxt = min(max(self.times),self.tau)
        except:
            maxt = max(self.times)
        plt.gca().set_xlim(1, maxt)
        plt.gca().set_ylim(0, 1)
        plt.gca().legend(loc=4)
        plt.gca().grid(axis='y',color='0.5',linestyle='-')
        plt.gca().set_title('Performance profile')

        plt.savefig(self.output)
