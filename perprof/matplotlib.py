"""
This handle the plot using matplotlib.
"""

from . import prof
import matplotlib.pyplot as plt

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
                print('ERROR: File {} exists'.format(self.output))
                print('Use `-f` to overwrite')
                exit(1)
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
            plt.plot(self.times, self.ppsbt[s])

        if self.semilog:
            plt.gca().set_xscale('log')

        plt.savefig(self.output)
