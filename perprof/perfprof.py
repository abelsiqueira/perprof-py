"""
Performance profile class, and related functions.

A performance profile requires information about the solution for each problem.
At least whether the problem converged or not, and how long it took/how much it
cost.

The input are files, one for each solver, with the following format::

    ---
    <Metadata 01>: <Value 01>
    <Metadata 02>: <Value 02>
    ---
    <Problem Name 01> <Exit Flag 01> <Cost 01>
    <Problem Name 02> <Exit Flag 02> <Cost 02>
    <Problem Name 03> <Exit Flag 03> <Cost 03>
    ...
"""

import os.path
import gettext
from . import aux
from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class PerfProfile(prof.Pdata):
    """
    Store data for performance profile.
    """
    def __init__(self, parser_options, profiler_options):
        """
        :param dict parser_options: parser configuration
        :param dict profiler_options: profiler configuration
        """
        prof.Pdata.__init__(self, parser_options, profiler_options)
        self.data = {}
        for file_ in parser_options['files']:
            data_tmp, solver_name = self.parse_file(file_)
            self.data[solver_name] = data_tmp

    def compute_profile(self, frtol=1e-3, fatol=1e-6):
        """
        Compute the performance function
        """
        try:
            self.solvers
        except AttributeError:
            self.get_set_solvers()
        try:
            self.problems
        except AttributeError:
            self.get_set_problems()

        ratio_set = set()
        for problem in self.problems:
            for solver in self.solvers:
                try:
                    self.data[solver][problem]["time"]
                except (KeyError, TypeError):
                    self.data[solver][problem] = {
                            "time": float('inf'),
                            "fval": float('inf') }
            min_fval = min([self.data[s][problem]["fval"]
                    for s in self.data.keys()])
            if min_fval < float('inf'):
                # Use function value to consider convergence
                min_time = min([self.data[s][problem]["time"]
                    for s in self.data.keys()
                        if self.data[s][problem]["fval"] < min_fval +
                        abs(min_fval)*frtol + fatol])
            else:
                min_time = min([self.data[s][problem]["time"]
                    for s in self.data.keys()])

            for solver in self.solvers:
                try:
                    self.data[solver][problem]["ratio"] = \
                            self.data[solver][problem]["time"] / min_time
                except ZeroDivisionError:
                    self.data[solver][problem] = {"ratio": float('inf')}
                if self.data[solver][problem]["ratio"] < float('inf'):
                    ratio_set.add(self.data[solver][problem]["ratio"])
        if not ratio_set:
            raise ValueError(_("ERROR: problem set is empty"))

        ratios = [x for x in ratio_set]
        ratios.sort()
        maxt = ratios[-1]
        ratios.append(maxt * 1.05)

        # prof = Percentage of Problems Solved By Ratio
        self.prof = {}
        for solver in self.solvers:
            self.prof[solver] = []
            for r in ratios:
                Ps = sum([self.data[solver][p]["ratio"] <= r for p in self.problems]) / self.number_problems
                self.prof[solver].append(Ps)
            if self.prof[solver][-1] == 0:
                raise ValueError(_("ERROR:") + solver +
                    _(" has no solved problems. Verify the 'success' flag."))
        self.profx = ratios

    def print_rob_eff_table(self):
        try:
            self.prof
        except AttributeError:
            self.compute_profile()

        import sys
        if self.tablename is None:
            output = sys.stdout
            print("Solvers    | Robust  | Effic")
            for solver in self.solvers:
                print('{:10s} | {:6.3f}% | {:6.3f}%'.format(solver,
                    round(100*self.prof[solver][-1],3),
                    round(100*self.prof[solver][0],3)))
        else:
            output = '{}.tex'.format(self.tablename)
            output = os.path.abspath(output)

            str2output = ['\\begin{tabular}{|c|r|r|} \\hline',
                    'Solver & Robustness & Efficiency \\\\ \\hline']
            for solver in self.solvers:
                str2output.append('{} & {} \% & {} \% \\\\ \\hline'.format(solver,
                    round(100*self.prof[solver][-1],3),
                    round(100*self.prof[solver][0],3)))
            str2output.append('\\end{tabular}')

            with open(output, 'w') as file_:
                file_.write('\n'.join(str2output))

    def parse_file(self, filename):
        """
        Parse one performance profile file.

        :param str filename: name of the file to be parser
        :param dict options: dictionary with the options:
            list subset: list with the name of the problems to use
            list success: list with strings to mark sucess
            int mintime: minimum time running the solver
            int maxtime: maximum time running the solver
            bool free_format: if False request that fail be mark with ``d``
        :return: performance profile data and name of the solver
        """
        solver_info = {
                'algname': aux._str_sanitize(filename),
                'success': self.success,
                'free_format': self.free_format
                }
        colopts = ['name', 'exit', 'time', 'fval', 'primal', 'dual']
        col = {}
        for colopt in colopts:
            # Columns starts at 1 but indexing at 0
            solver_info['col_'+colopt] = colopts.index(colopt)+1
            col[colopt] = colopts.index(colopt)
        data = {}
        with open(filename) as file_:
            line_number = 0
            in_yaml = False
            yaml_header = ''
            for line in file_:
                line_number += 1
                ldata = line.split()
                if len(ldata) == 0:
                    continue # Empty line
                # This is for backward compatibility
                elif ldata[0] == '#Name' and len(ldata) >= 2:
                    solver_info['algname'] = aux._str_sanitize(ldata[1])
                    # Handle YAML
                elif ldata[0] == '---':
                    if in_yaml:
                        aux._parse_yaml(solver_info, yaml_header)
                        for colopt in colopts:
                            # Columns starts at 1 but indexing at 0
                            col[colopt] = solver_info['col_'+colopt]-1
                        in_yaml = False
                    else:
                        in_yaml = True
                elif in_yaml:
                    yaml_header += line
                    # Parse data
                elif len(ldata) < 2:
                    raise ValueError(aux._error_message(filename, line_number,
                        _('This line must have at least 2 elements.')))
                else:
                    # Execution data
                    ldata[col["name"]] = aux._str_sanitize(ldata[col["name"]])
                    pname = ldata[col["name"]]
                    if self.subset and pname not in self.subset:
                        continue
                    if pname in data:
                        raise ValueError(aux._error_message(filename, line_number,
                            _('Duplicated problem: ') + pname + "."))
                    try:
                        time = float(ldata[col["time"]])
                    except:
                        raise ValueError(aux._error_message(filename, line_number,
                            _('Problem has no time/cost: ') + pname + "."))
                    if time < self.mintime:
                        time = self.mintime
                    if time >= self.maxtime:
                        continue
                    if self.compare == 'optimalvalues':
                        try:
                            if self.unc:
                                primal = 0.0
                            else:
                                primal = float(ldata[col["primal"]])
                            dual = float(ldata[col["dual"]])
                        except:
                            raise ValueError(aux._error_message(filename,
                                line_number, _("Column for primal or dual is out of bounds")))
                        if max(primal, dual) > self.infeas_tol:
                            continue
                        data[pname] = {
                                "time": time,
                                "fval": float('inf')}
                        try:
                            data[pname]["fval"] = float(ldata[col["fval"]])
                        except:
                            raise ValueError(aux._error_message(filename,
                                line_number, _("Column for fval is out of bounds")))
                    elif self.compare == 'exitflag':
                        if time == 0:
                            raise ValueError(aux._error_message(filename, line_number,
                                _("Time spending can't be zero.")))
                        if ldata[col["exit"]] in solver_info['success']:
                            if len(ldata) < 3:
                                raise ValueError(aux._error_message(filename, line_number,
                                    _('This line must have at least 3 elements.')))
                            data[pname] = {
                                    "time": time,
                                    "fval": float('inf')}
                        elif solver_info['free_format'] or ldata[col["exit"]] == 'd':
                            data[pname] = {
                                    "time": float('inf'),
                                    "fval": float('inf')}
                        else:
                            raise ValueError(aux._error_message(filename, line_number,
                                _('The second element in this lime must be {} or d.').format(
                                    ', '.join(solver_info['success']))))
                    else:
                        raise KeyError(_("The parser option 'compare' should be "
                            "'exitflag' or 'optimalvalues'"))

        if not data:
            raise ValueError(
                    _("ERROR: List of problems (intersected with subset, if any) is empty"))
        return data, solver_info['algname']
