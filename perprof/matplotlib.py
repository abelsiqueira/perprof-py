"""
This handle the plot using matplotlib.
"""

from . import prof
import matplotlib.pyplot as plt

class Profiler(prof.Pdata):
    def __init__(self, setup, tikz_header):
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
                raise PermissionError('Use the `-f` flag')
            except FileNotFoundError():
                pass

        try:
            self.already_scaled
        except:
            self.scale()

        plt.hold(True)
        for s in self.solvers:
            p_solved = []
            for t in self.times:
                aux = 0
                for p in self.problems:
                    if t > self.data[s][p]:
                        aux += 1
                p_solved.append(aux / self.number_problems)
            plt.plot(self.times, p_solved)

        if self.semilog:
            plt.gca().set_xscale('log')

        plt.savefig(self.output)
