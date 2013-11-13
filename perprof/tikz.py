"""
This handle the plot using tikz.
"""

import sys
import math
from . import prof

class Profiler(prof.Pdata):
    def __init__(self, setup, tikz_header):
        if setup.get_output() is None:
            self.output = sys.stdout
        else:
            self.output = '{}.tex'.format(setup.get_output())
        self.tikz_header = tikz_header
        prof.Pdata.__init__(self, setup)

    def scale(self):
        self.already_scaled = True
        super().scale()

    def plot(self):
        if not self.force:
            try:
                f = open(self.output, 'r')
                f.close()
                raise ValueError('ERROR: File {} exists. '.format(self.output) + 'Use `-f` to overwrite')
            except FileNotFoundError:
                pass
            except TypeError:
                # When using stdout
                pass

        try:
            self.already_scaled
        except:
            self.scale()

        try:
            self.ppsbt
        except:
            self.set_percent_problems_solved_by_time()

        maxt = max(self.times)

        str2output = ''

        if self.tikz_header:
            str2output += '\\documentclass{article}\n'
            str2output += '\\usepackage[utf8]{inputenc}\n'
            str2output += '\\usepackage[T1]{fontenc}\n'
            str2output += '\\usepackage{tikz}\n'
            str2output += '\\usepackage{pgfplots}\n'
            str2output += '\\usepackage{geometry}\n'
            str2output += '\\geometry{top=2cm,bottom=2cm,left=2cm,right=2cm}\n\n'
            str2output += '\\begin{document}\n'

        str2output += '\\begin{center}\n'
        str2output += '\\begin{tikzpicture}\n'

        if self.semilog:
            str2output += '  \\begin{semilogxaxis}[const plot, \n'
        else:
            str2output += '  \\begin{axis}[const plot, \n'
        str2output += '    xmin=1, xmax={:.2f},'.format(maxt)
        str2output += '    ymin=0, ymax=1,\n'
        str2output += '    ymajorgrids,\n'
        str2output += '    ytick={0,0.2,0.4,0.6,0.8,1.0},\n'
        str2output += '    legend pos= south east,\n'
        str2output += '    width=\\textwidth\n'
        str2output += '    ]\n'

        for s in self.solvers:
            str2output += '  \\addplot+[mark=none, thick] coordinates {\n'
            for i in range(len(self.times)):
                t = self.times[i]
                p = self.ppsbt[s][i]
                str2output += '    ({:.4f},{:.4f})\n'.format(t,p)
            str2output += '  };\n'
            str2output += '  \\addlegendentry{' + s + '}\n'
        if self.semilog:
            str2output += '  \\end{semilogxaxis}\n'
        else:
            str2output += '  \\end{axis}\n'
        str2output += '\\end{tikzpicture}\n'
        str2output += '\\end{center}\n'

        if self.tikz_header:
            str2output += '\\end{document}'

        try:
            with open(self.output, 'w') as f:
                f.write(str2output)
        except TypeError:
            # When using stdout
            print(str2output, file=self.output)
