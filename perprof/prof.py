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
    data = {}
    for f in setup.get_files():
        data[f] = parse.parse_file(f)
    return data

class Pdata:
    def __init__(self, setup):
        self.data = load_data(setup)

    def __repr__(self):
        try:
            self.solvers
        except:
            self.get_set_solvers()
        try:
            self.problems
        except:
            self.get_set_problems()

        for s in self.solvers:
            print('{:>8}'.format(s), end='  ')
        print()

        for p in self.problems:
            print('{:>8}'.format(p), end='  ')
            for s in self.solvers:
                print('{:8.4}'.format(self.data[s][p]), end='  ')
            print()

        print('times = ', end=' ')
        for t in self.times:
            print('{:.4}'.format(t), end=' ')
        print()

        print('perf_functions:')
        pprint.pprint(self.perf_functions)

        return ''

    def get_set_solvers(self):
        try:
            self.solvers
        except:
            self.solvers = self.data.keys()
        return self.solvers

    def get_set_problems(self):
        try:
            self.problems
        except:
            p = set()
            for i in self.data.keys():
                for j in self.data[i].keys():
                    p.add(j)
            self.problems = p
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
        self.times = [x for x in self.times]
        self.times.sort()

    def generate_perf_functions(self):
        self.perf_functions = {}
        for s in self.solvers:
            self.perf_functions[s] = []
        for t in self.times:
            for s in self.solvers:
                self.perf_functions[s].append(len(
                    [x for x in self.data[s].values() if x <= t]))
            
    def print_tikz(self, use_log = False):
        colors = ['red','blue','green']
        maxt = max(self.times)

        if use_log:
            for i in range(len(self.times)):
                self.times[i] = math.log(self.times[i])/math.log(maxt)
        else:
            for i in range(len(self.times)):
                self.times[i] = self.times[i]/maxt


        print('\\begin{center}')
        print('\\begin{tikzpicture}[yscale=10,xscale=15]')
        print('  \draw[->] (-0.01,0) -- (1.01,0);')
        print('  \draw[->] (0,-0.01) -- (0,1.05);')

        print('  \\foreach \\y in {0.2,0.4,0.6,0.8,1.0} {')
        print('    \draw (-0.01,\\y)node[left]{\\y} -- (0.01,\\y);')
        print('    \draw[dashed,gray,thin] (0,\\y) -- (1,\\y);')
        print('    \draw (1.01,\\y)node[right]{\\y} -- (0.99,\\y);')
        print('  }')

        
        N = math.floor(math.log10(maxt));
        V = 10**N/maxt

        for i in range(1,N+1):
            print('  \draw ({:.2f},-0.01)'.format(i*V), end='')
            print('node[below]', end='')
            if use_log:
                print('{$10^{'+'{}'.format(i)+'}$}', end='')
            else:
                print('{$'+'{}'.format(i), end='')
                print('\\times10^{'+'{}'.format(N)+'}$}', end='')
            print(' -- ({:.2f},0.01);'.format(i*V))

        print('  \draw (1,-0.01)node[below]{', end='')
        print('{:.2f}'.format(maxt), end='')
        print('} -- (1,1.05);')

        count = 0
        for s in self.solvers:
            N = len(self.problems)
            p = self.perf_functions[s][0]/N
            for i in range(len(self.times)-1):
                t = self.times[i]
                tp = self.times[i+1]
                print('  \draw[{},thick] '.format(colors[count]), end='')
                print('({:.4f},{:.4f})'.format(t,p), end='')
                print(' -- ({:.4f},{:.4f})'.format(tp,p), end='')
                p = self.perf_functions[s][i+1]/N;
                print(' -- ({:.4f},{:.4f})'.format(tp,p), end='')
                print(';')
            count = count + 1

        print('\end{tikzpicture}')
        print('\end{center}')
