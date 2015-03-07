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
    """
    The profiler using TikZ.
    """
    def __init__(self, parser_options, profiler_options):
        """
        :param dict parser_options: parser options
        :param dict profiler_options: profiler options
        """
        if profiler_options['output'] is None:
            self.output = sys.stdout
        else:
            self.output = '{}.tex'.format(profiler_options['output'])
            self.output = os.path.abspath(self.output)
        self.standalone = profiler_options['standalone']
        self.output_format = profiler_options['output_format']

        # Language for the axis label
        translation = gettext.translation('perprof',
                os.path.join(THIS_DIR, 'locale'), [profiler_options['lang']])
        self.axis_lang = translation.gettext

        prof.Pdata.__init__(self, parser_options, profiler_options)

    def plot(self):
        """
        Create the performance profile using matplotlib.
        """
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

        str2output = []

        if self.standalone or self.output_format == 'pdf':
            str2output.append('\\documentclass{standalone}')
            str2output.append('\\usepackage[utf8]{inputenc}')
            str2output.append('\\usepackage[T1]{fontenc}')
            str2output.append('\\usepackage{tikz}')
            str2output.append('\\usepackage{pgfplots}')
            if self.pgfplot_version is not None:
                str2output.append('\\pgfplotsset{{compat={0}}}'.format(
                        self.pgfplot_version))
            else:
                str2output.append('\\pgfplotsset{compat=newest,compat/show ' \
                        'suggested version=false}')
            if self.page_background:
                str = '\\definecolor{pagebg}{RGB}{'
                str += '{},{},{}'.format(
                                self.page_background[0],
                                self.page_background[1],
                                self.page_background[2])
                str += '}'
                str2output.append(str)
                str2output.append('\\pagecolor{pagebg}')
            str2output.append('\\begin{document}')
        else:
            str2output.append('\\begin{center}')
        str2output.append('\\begin{tikzpicture}')

        if self.semilog:
            str2output.append('  \\begin{semilogxaxis}[const plot,')
        else:
            str2output.append('  \\begin{axis}[const plot,')
        if self.black_and_white:
            str2output.append('cycle list name=linestyles*,')
        if self.background:
            str2output.append("axis background/.style=" \
                    "{{fill={{rgb,255:red,{0};green,{1};blue,{2}}}}},".format(
                            self.background[0],
                            self.background[1],
                            self.background[2]))
        str2output.append('    xmin=1, xmax={:.2f},\n' \
        '    ymin=0, ymax=1,\n' \
        '    ymajorgrids,\n' \
        '    ytick={{0,0.2,0.4,0.6,0.8,1.0}},\n' \
        '    xlabel={{{xlabel}}}, ylabel={{{ylabel}}},\n' \
        '    legend pos= south east,\n' \
        '    width=\\textwidth\n' \
        '    ]'.format(maxt,
                xlabel=self.axis_lang('Performance Ratio'),
                ylabel=self.axis_lang('Problems solved')))

        for solver in self.solvers:
            str2output.append('  \\addplot+[mark=none, thick] coordinates {')
            for i in range(len(self.times)):
                if self.times[i] <= self.tau:
                    time = self.times[i]
                    ppsbt = self.ppsbt[solver][i]
                    str2output.append('    ({:.4f},{:.4f})'.format(time,
                        ppsbt))
                else:
                    break
            str2output.append('  };')
            str2output.append('  \\addlegendentry{{{0}}}'.format(solver))
        if self.semilog:
            str2output.append('  \\end{semilogxaxis}')
        else:
            str2output.append('  \\end{axis}')
        str2output.append('\\end{tikzpicture}')
        if self.standalone or self.output_format == 'pdf':
            str2output.append('\\end{document}')
        else:
            str2output.append('\\end{center}\n')

        try:
            with open(self.output, 'w') as file_:
                file_.write('\n'.join(str2output))

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
