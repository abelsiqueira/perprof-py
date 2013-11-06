"""
This handle the plot using matplotlib.
"""

from . import prof
import matplotlib.pyplot as plt

class Profiler(prof.Pdata):
    def scale(self):
        self.already_scale = True
        super().scale()

    def plot(self):
        try:
            self.already_scale
        except:
            self.scale()

        if self.log:
            raise NotImplementedError()
        else:
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
        plt.savefig('performe-profile.png')
