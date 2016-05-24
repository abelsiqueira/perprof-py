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

        # Language for the plot
        translation = gettext.translation('perprof',
                os.path.join(THIS_DIR, 'locale'), [profiler_options['lang']])
        self.plot_lang = translation.gettext

        prof.Pdata.__init__(self, parser_options, profiler_options)

    def plot(self):
        """
        Create the performance profile using TikZ/PgfPlots.
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

        if self.black_and_white and len(self.solvers) > 13:
            raise ValueError(_("ERROR: Maximum numbers of solvers in black" \
                " and white plot is 13."))
        if not self.black_and_white and len(self.solvers) > 30:
            raise ValueError(_("ERROR: Maximum numbers of solvers in color" \
                " plot is 30."))

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
                str2output.append('\\definecolor{{pagebg}}{{RGB}}{{' \
                        '{0},{1},{2}}}'.format(
                                self.page_background[0],
                                self.page_background[1],
                                self.page_background[2]))
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
            lines = ["dashed", "dotted", "dashdotted", "dashdotdotted"]
            types = ["", "loosely ", "densely "]
            str2output.append('  cycle list={')
            aux = ["solid"]
            for k in range(0,len(self.solvers)):
                i = k % len(lines)
                j = k // len(lines)
                aux.append('  {{{}{}}}'.format(types[j], lines[i]))
            str2output.append(',\n'.join(aux) + '},')
        else:
            colors = ["blue", "red", "black", "brown", "green!80!black",
                    "magenta!80!black"]
            lines = ["solid", "dashed", "dotted", "dashdotted", "dashdotdotted"]
            str2output.append('  cycle list={')
            aux = []
            for k in range(0,len(self.solvers)):
                i = k % len(colors)
                j = k // len(colors)
                aux.append('  {{{},{}}}'.format(colors[i], lines[j]))
            str2output.append(',\n'.join(aux) + '},')
        if self.background:
            str2output.append("axis background/.style=" \
                    "{{fill={{rgb,255:red,{0};green,{1};blue,{2}}}}},".format(
                            self.background[0],
                            self.background[1],
                            self.background[2]))
        if len(self.solvers) > 5:
            legend_pos = 'outer north east'
        else:
            legend_pos = 'south east'
        str2output.append('    xmin=1, xmax={:.2f},\n' \
        '    ymin=-0.003, ymax=1.003,\n' \
        '    ymajorgrids,\n' \
        '    ytick={{0,0.2,0.4,0.6,0.8,1.0}},\n' \
        '    xlabel={{{xlabel}}},\n' \
        '    ylabel={{{ylabel}}},\n' \
        '    title={{{title}}},\n' \
        '    legend pos={{{legend_pos}}},\n' \
        '    width=\\textwidth\n' \
        '    ]'.format(maxt,
                xlabel=self.plot_lang(self.xlabel),
                ylabel=self.plot_lang(self.ylabel),
                legend_pos=legend_pos,
                title=self.plot_lang(self.title)))

        for solver in self.solvers:
            this_ppsbt = self.ppsbt[solver]
            str2output.append('  \\addplot+[mark=none, thick] coordinates {')
            str2output.append('    ({:.4f},{:.4f})'.format(self.times[0],
                this_ppsbt[0]))
            last_t = round(self.times[0], 4)
            last_p = round(self.ppsbt[solver][0], 4)
            for i in range(1,len(self.times)-1):
                dx = round(self.times[i], 4) - last_t
                dx2 = round(self.times[i+1], 4) - last_t
                dy = round(this_ppsbt[i], 4) - last_p
                dy2 = round(this_ppsbt[i+1], 4) - last_p
                if dx*dy2 == dy*dx2:
                    continue
                if self.times[i] <= self.tau:
                    time = round(self.times[i], 4)
                    ppsbt = round(self.ppsbt[solver][i], 4)
                    str2output.append('    ({:.4f},{:.4f})'.format(time, ppsbt))
                    last_t = time
                    last_p = ppsbt
                else:
                    break
            j = len(self.times)-1
            str2output.append('    ({:.4f},{:.4f})'.format(self.times[j],
                this_ppsbt[j]))
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
