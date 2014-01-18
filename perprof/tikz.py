"""
This handle the plot using tikz.
"""

import sys
import os.path
import subprocess
import math
from . import prof

class Profiler(prof.Pdata):
    def __init__(self, setup, tikz_header):
        if setup.get_output() is None:
            self.output = sys.stdout
        else:
            self.output = '{}.tex'.format(setup.get_output())
            self.output = os.path.abspath(self.output)
        self.tikz_header = tikz_header
        prof.Pdata.__init__(self, setup)
        self.output_format = setup.get_output_format()

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
        try:
            self.tau
            maxt = min(maxt, self.tau)
        except:
            self.tau = maxt

        str2output = ''

        if self.tikz_header or self.output_format == 'pdf':
            str2output += '\\documentclass{standalone}\n'
            str2output += '\\usepackage[utf8]{inputenc}\n'
            str2output += '\\usepackage[T1]{fontenc}\n'
            str2output += '\\usepackage{tikz}\n'
            str2output += '\\usepackage{pgfplots}\n'
            if self.pgfplot_version is not None:
                str2output += '\\pgfplotsset{{compat={0}}}\n'.format(
                        self.pgfplot_version)
            else:
                str2output += '\\pgfplotsset{compat=newest,compat/show ' \
                        'suggested version=false}\n'
            str2output += '\\begin{document}\n'
        else:
            str2output += '\\begin{center}\n'
        str2output += '\\begin{tikzpicture}\n'

        if self.semilog:
            str2output += '  \\begin{semilogxaxis}[const plot, \n'
        else:
            str2output += '  \\begin{axis}[const plot, \n'
        if self.bw:
            str2output += 'cycle list name=linestyles*,\n'
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
                if self.times[i] <= self.tau:
                    t = self.times[i]
                    p = self.ppsbt[s][i]
                    str2output += '    ({:.4f},{:.4f})\n'.format(t,p)
                else:
                    break
            str2output += '  };\n'
            str2output += '  \\addlegendentry{' + s + '}\n'
        if self.semilog:
            str2output += '  \\end{semilogxaxis}\n'
        else:
            str2output += '  \\end{axis}\n'
        str2output += '\\end{tikzpicture}\n'
        if self.tikz_header or self.output_format == 'pdf':
            str2output += '\\end{document}'
        else:
            str2output += '\\end{center}\n'

        try:
            with open(self.output, 'w') as f:
                f.write(str2output)

            if self.output_format == 'pdf':
                subprocess.check_call(['pdflatex',
                    '-interaction', 'nonstopmode',
                    '-output-directory', os.path.dirname(self.output),
                    self.output])
        except TypeError:
            # When using stdout
            print(str2output, file=self.output)
