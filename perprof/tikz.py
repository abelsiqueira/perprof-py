"""
This handle the plot using tikz.
"""

import math
from . import prof

class Profiler(prof.Pdata):
    def __init__(self, setup, tikz_header):
        self.tikz_header = tikz_header
        prof.Pdata.__init__(self, setup)

    def scale(self):
        self.already_scaled = True
        super().scale()

    def generate_perf_functions(self):
        self.perf_functions = {}
        for s in self.solvers:
            self.perf_functions[s] = []
        for t in self.times:
            for s in self.solvers:
                self.perf_functions[s].append(len(
                    [x for x in self.data[s].values() if x <= t]))

    def plot(self):
        try:
            self.already_scaled
        except:
            self.scale()

        try:
            self.perf_functions
        except:
            self.generate_perf_functions()

        colors = ['red','blue','green']
        maxt = max(self.times)

        if self.semilog:
            for i in range(len(self.times)):
                self.times[i] = math.log(self.times[i])/math.log(maxt)
        else:
            for i in range(len(self.times)):
                self.times[i] = self.times[i]/maxt

        if self.tikz_header:
            print('\\documentclass{article}')
            print('\\usepackage[utf8]{inputenc}')
            print('\\usepackage[T1]{fontenc}')
            print('\\usepackage{tikz}')
            print('\\usepackage{pgfplots}')
            print()
            print('\\usepackage{geometry}')
            print()
            print('\\geometry{top=2cm,bottom=2cm,left=2cm,right=2cm}')
            print()
            print('\\begin{document}')

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
            if self.semilog:
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

        if self.tikz_header:
            print('\\end{document}')
