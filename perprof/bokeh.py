"""
This handle the plot using bokeh.
"""

import os.path
import gettext
import bokeh.models.formatters
import bokeh.plotting as plt

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

# TODO: Add more colors to list and compatible with others backend
BOKEH_COLOR_LIST = ["blue",
                    "green",
                    "red",
                    "cyan",
                    "magenta",
                    "yellow"]

def plot(x, y, options):
    """
    Create the profile using matplotlib.
    """
    if options['output'] is None:
        output = 'performance-profile.{}'.format(options['output_format'])
    else:
        output = '{}.{}'.format(options['output'], options['output_format'])

    # Language for the plot
    translation = gettext.translation('perprof',
            os.path.join(THIS_DIR, 'locale'), [options['lang']])
    plot_lang = translation.gettext

    solvers = y.keys()
    tau = options['tau']

    if not options['force']:
        try:
            file_ = open(output, 'r')
            file_.close()
            raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite').format(output))
        except FileNotFoundError:
            pass

    plt.output_file(output, title=plot_lang(options['title']))

    # Axis
    try:
        maxt = min(max(x), tau)
    except (AttributeError, TypeError):
        maxt = max(x)

    boken_plot_options = {"x_range":[1,maxt], "y_range":[0,1]}

    # Change the xscale to log scale
    if options['semilog']:
        boken_plot_options["x_axis_type"] = "log"

    p = plt.figure(title=plot_lang(options['title']),
            x_axis_label=plot_lang(options['ylabel']),
            y_axis_label=plot_lang(options['xlabel']),
            **boken_plot_options)

    for idx, solver in enumerate(solvers):
        p.line(x, y[solver],
                legend=solver,
                line_width=2,
                line_color=BOKEH_COLOR_LIST[idx % len(BOKEH_COLOR_LIST)])

    # Legend
    p.legend.orientation = "horizontal"

    # Help lines
    p.grid.grid_line_color = "black"
    p.grid.grid_line_alpha = 0.5

    # Save the plot
    plt.save(p)
