"""
This handle the plot using tikz.
"""

import sys
import os.path
import gettext
import subprocess
from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class Profiler(prof.Pdata):
    def __init__(self, setup, standalone):
        if setup.get_output() is None:
            self.output = sys.stdout
        else:
            self.output = '{}.tex'.format(setup.get_output())
            self.output = os.path.abspath(self.output)
        self.standalone = standalone
        prof.Pdata.__init__(self, setup)
        self.output_format = setup.get_output_format()

        # Language for the axis label
        translation = gettext.translation('perprof',
                os.path.join(THIS_DIR, 'locale'), [setup.lang])
        self.axis_lang = translation.gettext

    def plot(self):
        if not self.force:
            try:
                file_ = open(self.output, 'r')
                file_.close()
                raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite.').format(self.output))
            except FileNotFoundError:
                pass
            except TypeError:
                # When using stdout
                pass

        if not self.already_scaled:
            self.scale()

        try:
            self.ppsbt
        except AttributeError:
            self.set_percent_problems_solved_by_time()

        maxt = max(self.times)
        try:
            maxt = min(maxt, self.tau)
        except (AttributeError, TypeError):
            self.tau = maxt

        str2output = ''

        if self.standalone or self.output_format == 'pdf':
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
        if self.black_and_white:
            str2output += 'cycle list name=linestyles*,\n'
        if self.background:
            str2output += "axis background/.style=" \
                    "{{fill={{rgb,255:red,{0};green,{1};blue,{2}}}}}, \n".format(
                            self.background[0],
                            self.background[1],
                            self.background[2])
        str2output += '    xmin=1, xmax={:.2f},' \
        '    ymin=0, ymax=1,\n' \
        '    ymajorgrids,\n' \
        '    ytick={{0,0.2,0.4,0.6,0.8,1.0}},\n' \
        '    xlabel={{{xlabel}}}, ylabel={{{ylabel}}},\n' \
        '    legend pos= south east,\n' \
        '    width=\\textwidth\n' \
        '    ]\n'.format(maxt,
                xlabel=self.axis_lang('Performance Ratio'),
                ylabel=self.axis_lang('Problems solved'))

        for solver in self.solvers:
            str2output += '  \\addplot+[mark=none, thick] coordinates {\n'
            for i in range(len(self.times)):
                if self.times[i] <= self.tau:
                    time = self.times[i]
                    ppsbt = self.ppsbt[solver][i]
                    str2output += '    ({:.4f},{:.4f})\n'.format(time, ppsbt)
                else:
                    break
            str2output += '  };\n'
            str2output += '  \\addlegendentry{' + solver + '}\n'
        if self.semilog:
            str2output += '  \\end{semilogxaxis}\n'
        else:
            str2output += '  \\end{axis}\n'
        str2output += '\\end{tikzpicture}\n'
        if self.standalone or self.output_format == 'pdf':
            str2output += '\\end{document}'
        else:
            str2output += '\\end{center}\n'

        try:
            with open(self.output, 'w') as file_:
                file_.write(str2output)

            if self.output_format == 'pdf':
                if self.pdf_verbose:
                    mode = 'nonstopmode'
                else:
                    mode = 'batchmode'
                subprocess.check_call(['pdflatex', '-interaction', mode,
                    '-output-directory', os.path.dirname(self.output),
                    self.output])
        except TypeError:
            # When using stdout
            print(str2output, file=self.output)
