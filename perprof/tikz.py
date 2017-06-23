"""
This handle the plot using tikz.
"""

import sys
import os.path
import gettext
import subprocess

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

def plot(x, y, options):
    """
    Create the profile using TikZ/PgfPlots.
    """
    if options['output'] is None:
        output = sys.stdout
    else:
        output = '{}.tex'.format(options['output'])
        output = os.path.abspath(output)

    # Language for the plot
    translation = gettext.translation('perprof',
            os.path.join(THIS_DIR, 'locale'), [options['lang']])
    plot_lang = translation.gettext

    if not options['force']:
        try:
            file_ = open(output, 'r')
            file_.close()
            raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite.').format(output))
        except FileNotFoundError:
            pass
        except TypeError:
            # When using stdout
            pass

    solvers = y.keys()
    tau = options['tau']

    if options['black_and_white'] and len(solvers) > 13:
        raise ValueError(_("ERROR: Maximum numbers of solvers in black" \
            " and white plot is 13."))
    if not options['black_and_white'] and len(solvers) > 30:
        raise ValueError(_("ERROR: Maximum numbers of solvers in color" \
            " plot is 30."))

    maxt = max(x)
    try:
        maxt = min(maxt, tau)
    except (AttributeError, TypeError):
        tau = maxt

    str2output = []

    if options['standalone'] or options['output_format'] == 'pdf':
        str2output.append('\\documentclass{standalone}')
        str2output.append('\\usepackage[utf8]{inputenc}')
        str2output.append('\\usepackage[T1]{fontenc}')
        str2output.append('\\usepackage{tikz}')
        str2output.append('\\usepackage{pgfplots}')
        if options['pgfplot_version'] is not None:
            str2output.append('\\pgfplotsset{{compat={0}}}'.format(
                    options['pgfplot_version']))
        else:
            str2output.append('\\pgfplotsset{compat=newest,compat/show ' \
                    'suggested version=false}')
        if options['page_background']:
            str2output.append('\\definecolor{{pagebg}}{{RGB}}{{' \
                    '{0},{1},{2}}}'.format(
                            options['page_background'][0],
                            options['page_background'][1],
                            options['page_background'][2]))
            str2output.append('\\pagecolor{pagebg}')
        str2output.append('\\begin{document}')
    else:
        str2output.append('\\begin{center}')
    str2output.append('\\begin{tikzpicture}')

    if options['semilog']:
        str2output.append('  \\begin{semilogxaxis}[const plot,')
    else:
        str2output.append('  \\begin{axis}[const plot,')
    if options['black_and_white']:
        lines = ["dashed", "dotted", "dashdotted", "dashdotdotted"]
        types = ["", "loosely ", "densely "]
        str2output.append('  cycle list={')
        aux = ["solid"]
        for k in range(0,len(solvers)):
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
        for k in range(0,len(solvers)):
            i = k % len(colors)
            j = k // len(colors)
            aux.append('  {{{},{}}}'.format(colors[i], lines[j]))
        str2output.append(',\n'.join(aux) + '},')
    if options['background']:
        str2output.append("axis background/.style=" \
                "{{fill={{rgb,255:red,{0};green,{1};blue,{2}}}}},".format(
                        options['background'][0],
                        options['background'][1],
                        options['background'][2]))
    if len(solvers) > 5:
        legend_pos = 'outer north east'
    else:
        legend_pos = 'south east'
    if options['title'] is None:
        title = ''
    else:
        title = ',\n    title={{{}}},\n'.format(plot_lang(options['title']))

    str2output.append('    xmin=1, xmax={:.2f},\n' \
    '    ymin=-0.003, ymax=1.003,\n' \
    '    ymajorgrids,\n' \
    '    ytick={{0,0.2,0.4,0.6,0.8,1.0}},\n' \
    '    xlabel={{{xlabel}}},\n' \
    '    ylabel={{{ylabel}}},\n' \
    '{title}' \
    '    legend pos={{{legend_pos}}},\n' \
    '    width=\\textwidth\n' \
    '    ]'.format(maxt,
            xlabel=plot_lang(options['xlabel']),
            ylabel=plot_lang(options['ylabel']),
            title=title,
            legend_pos=legend_pos))

    for solver in solvers:
        this_prof = y[solver]
        str2output.append('  \\addplot+[mark=none, thick] coordinates {')
        str2output.append('    ({:.4f},{:.4f})'.format(x[0],
            this_prof[0]))
        last_t = round(x[0], 4)
        last_p = round(y[solver][0], 4)
        for i in range(1,len(x)-1):
            dx = round(x[i], 4) - last_t
            dx2 = round(x[i+1], 4) - last_t
            dy = round(this_prof[i], 4) - last_p
            dy2 = round(this_prof[i+1], 4) - last_p
            if dx*dy2 == dy*dx2:
                continue
            if x[i] <= tau:
                time = round(x[i], 4)
                prof = round(y[solver][i], 4)
                str2output.append('    ({:.4f},{:.4f})'.format(time, prof))
                last_t = time
                last_p = prof
            else:
                break
        j = len(x)-1
        str2output.append('    ({:.4f},{:.4f})'.format(x[j],
            this_prof[j]))
        str2output.append('  };')
        str2output.append('  \\addlegendentry{{{0}}}'.format(solver))

    if options['semilog']:
        str2output.append('  \\end{semilogxaxis}')
    else:
        str2output.append('  \\end{axis}')
    str2output.append('\\end{tikzpicture}')
    if options['standalone'] or options['output_format'] == 'pdf':
        str2output.append('\\end{document}')
    else:
        str2output.append('\\end{center}\n')

    try:
        with open(output, 'w') as file_:
            file_.write('\n'.join(str2output))

        if options['output_format'] == 'pdf':
            if options['pdf_verbose']:
                mode = 'nonstopmode'
            else:
                mode = 'batchmode'
            subprocess.check_call(['pdflatex', '-interaction', mode,
                '-output-directory', os.path.dirname(output),
                output])
    except TypeError:
        # When using stdout
        print(str2output, file=output)
