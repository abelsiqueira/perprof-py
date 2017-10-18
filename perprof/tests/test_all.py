import unittest
import perprof
from perprof.main import process_arguments
from perprof.main import set_arguments
from perprof import bokeh
from perprof import tikz
from perprof import matplotlib
from perprof import perfprof

class TestPerprof(unittest.TestCase):

    fileargs = {
            "perf": 'perprof/examples/perf.example',
            "perf-mf": ' '.join(['perprof/examples/' + s + '.table' for s in ['alpha', 'beta', 'gamma']])
            }
    backends = ['bokeh', 'tikz', 'mp', 'raw']
    backend_plots = {
            "bokeh": bokeh.plot,
            "tikz": tikz.plot,
            "mp": matplotlib.plot
            }
    profiles = {
            "perf": perfprof.PerfProfile,
            "perf-mf": perfprof.PerfProfile
            }
    profile_args = {
            "perf": "--performance-profile",
            "perf-mf": "--performance-profile-multiple-files"
            }

    def test_backends(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo'
            isTrue = {'bokeh': False, 'tikz': False, 'mp': False, 'raw': False }
            isTrue[backend] = True
            args = set_arguments(args.split())
            self.assertEqual(args.bokeh, isTrue['bokeh'])
            self.assertEqual(args.tikz, isTrue['tikz'])
            self.assertEqual(args.mp,   isTrue['mp'])
            self.assertEqual(args.raw,  isTrue['raw'])

    def test_output_formats(self):
        outputs = {
                "bokeh": ["html"],
                "tikz": ["pdf", "tex"],
                "mp": ["png", "eps", "pdf", "ps", "svg"],
                "raw": [] }
        backends = self.backends
        x = [1.0, 2.0, 3.0, 4.0]
        y = { "s1": [0.0, 0.25, 0.25, 0.75], "s2": [0.25, 0.50, 1.00, 1.00] }
        for backend in backends:
            for output in outputs[backend]:
                args = '--' + backend + ' --' + output + ' --demo -f'
                args = set_arguments(args.split())
                options = process_arguments(args)
                self.assertEqual(options['output_format'], output)
                self.backend_plots[backend](x, y, options)

    def test_profiles(self):
        for p in self.profiles:
            args = self.profile_args[p] + ' --tikz -o tmp -f ' + self.fileargs[p]
            args = set_arguments(args.split())
            options = process_arguments(args)
            prof = self.profiles[p](options)

    # Performance profile tests
    def test_only_name(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/only-name.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_columns(self):
        baseargs = self.profile_args["perf-mf"] + ' --tikz ' + self.fileargs["perf-mf"]
        #Default comparison needs 3 columns
        args = baseargs + ' perprof/tests/2-col.sample '
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)
        #Default values should fail with 5 or less columns.
        #Unconstrained Default values should fail with 5 or less columns
        #(because dual default column is 5).
        baseargs = '--compare optimalvalues ' + baseargs
        for xtra in ['', '--unconstrained ']:
            baseargs = xtra + baseargs
            for n in [2,3,4,5]:
                args = baseargs + ' perprof/tests/{}-col.sample '.format(n)
                args = set_arguments(args.split())
                options = process_arguments(args)
                self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_without_time(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/without-time.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_without_c_or_d(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/c-or-d.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_zero_time(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/zero-time.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_empty_file(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/empty.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_empty_subset(self):
        args = self.profile_args["perf-mf"] + ' --tikz --demo --subset perprof/tests/empty.subset'
        args = set_arguments(args.split())
        self.assertRaises(AttributeError, process_arguments, args)

    def test_empty_intersection(self):
        args = self.profile_args["perf-mf"] + ' --tikz --demo --subset perprof/tests/fantasy.subset'
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_no_success(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/no-success.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        prof = self.profiles["perf-mf"](options)
        self.assertRaises(ValueError, prof.compute_profile)

    def test_repeated_problem(self):
        args = self.profile_args["perf-mf"] + ' --tikz perprof/tests/repeat.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, self.profiles["perf-mf"], options)

    def test_yaml_fail(self):
        args = '--tikz perprof/tests/yaml-fail.sample ' + self.fileargs["perf-mf"]
        args = set_arguments(args.split())
        options = process_arguments(args)
        self.assertRaises(ValueError, perfprof.PerfProfile, options)

if __name__ == '__main__':
    unittest.main()
