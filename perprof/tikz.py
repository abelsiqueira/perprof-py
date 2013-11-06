"""
This handle the plot using tikz.
"""

import sys
import math
from . import prof

class Profiler(prof.Pdata):
    def __init__(self, setup, tikz_header):
        if setup.get_output() is None:
            self.output = sys.stdin
        else:
            self.output = '{}.tex'.format(setup.get_output())
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

        try:
            self.perf_functions
        except:
            self.generate_perf_functions()

        maxt = max(self.times)

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
        print('\\begin{tikzpicture}')

        if self.semilog:
            print('  \\begin{semilogxaxis}[const plot, ')
        else:
            print('  \\begin{axis}[const plot, ')
        print('    xmin=1, xmax={:.2f},'.format(maxt))
        print('    ymin=0, ymax=1,')
        print('    ymajorgrids,')
        print('    ytick={0,0.2,0.4,0.6,0.8,1.0},')
        print('    legend pos= south east,')
        print('    width=\\textwidth')
        print('    ]')

        for s in self.solvers:
            N = len(self.problems)
            print('  \\addplot+[mark=none, thick] coordinates {')
            for i in range(len(self.times)):
                t = self.times[i]
                p = self.perf_functions[s][i]/N
                print('    ({:.4f},{:.4f})'.format(t,p))
            print('  };')
        if self.semilog:
            print('  \\end{semilogxaxis}')
        else:
            print('  \\end{axis}')
        print('\end{tikzpicture}')
        print('\end{center}')

        if self.tikz_header:
            print('\\end{document}')
