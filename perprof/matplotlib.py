"""
This handle the plot using matplotlib.
"""

import os.path
import gettext
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

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

    if not options['force']:
        try:
            file_ = open(output, 'r')
            file_.close()
            raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite').format(output))
        except FileNotFoundError:
            pass

    solvers = y.keys()
    tau = options['tau']

    # Hack need to background color
    figure_ = plt.figure()
    plot_ = figure_.add_subplot(111)

    # Set configurations handle when saving the plot
    save_configs = {}
    save_configs['format'] = options['output_format']

    pg_bg = options['page_background']
    bg = options['background']
    if pg_bg:
        if not bg:
            bg = options['page_background']
        # RGB tuples must be in the range [0,1]
        save_configs['facecolor'] = (pg_bg[0] / 255, pg_bg[1] / 255, pg_bg[2] / 255)
    if bg:
        plot_.set_axis_bgcolor((bg[0] / 255, bg[1] / 255, bg[2] / 255))
        if not pg_bg:
            figure_.patch.set_alpha(0.0)
    if not bg and not pg_bg:
        save_configs['transparent'] = True
        save_configs['frameon'] = False

    # We need to hold the plots
    plot_.hold(True)

    # Define the linestyles
    if options['black_and_white']:
        linestyles = ['k-', 'k--', 'k:', 'k-.']
    else:
        linestyles = ['b', 'g', 'r', 'c', 'm', 'y']

    # Generate the plot for each solver
    for idx, solver in enumerate(solvers):
        plot_.step(x, y[solver], linestyles[idx], label=solver, where='post')

    # Change the xscale to log scale
    if options['semilog']:
        plt.gca().set_xscale('log')

    # Axis
    try:
        maxt = min(max(x), tau)
    except (AttributeError, TypeError):
        maxt = max(x)
    plt.gca().set_xlim(1, maxt)
    plt.gca().set_xlabel(plot_lang(options['xlabel']))
    plt.gca().set_ylim(-0.002, 1.006)
    plt.gca().set_ylabel(plot_lang(options['ylabel']))
    if options['title'] is not None:
        plt.gca().set_title(plot_lang(options['title']))

    # Legend
    plt.gca().legend(loc=4)

    # Help lines
    plt.gca().grid(axis='y', color='0.5', linestyle='-')

    # Save the plot
    # pylint: disable-msg=W0142
    plt.savefig(output, bbox_inches='tight', pad_inches=0.05,
            **save_configs)
