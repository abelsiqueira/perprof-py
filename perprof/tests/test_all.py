import unittest
import perprof
from perprof.main import PerProfSetup
from perprof.main import set_arguments
from perprof import tikz
from perprof import matplotlib
from perprof import prof

class TestPerprof(unittest.TestCase):

    goodfiles = ' '.join(['perprof/examples/' + s + '.table' \
            for s in ['alpha', 'beta', 'gamma']])
    backends = ['tikz', 'mp', 'raw']
    back_profilers = {
            "tikz": tikz.Profiler,
            "mp": matplotlib.Profiler,
            "raw": prof.Pdata }

    def test_backends(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo'
            isTrue = {'tikz': False, 'mp': False, 'raw': False }
            isTrue[backend] = True
            args = set_arguments(args.split())
            self.assertEqual(args.tikz, isTrue['tikz'])
            self.assertEqual(args.mp,   isTrue['mp'])
            self.assertEqual(args.raw,  isTrue['raw'])

    def test_output_formats(self):
        outputs = {
                "tikz": ["pdf", "tex"],
                "mp": ["png", "eps", "pdf", "ps", "svg"],
                "raw": [] }
        backends = self.backends
        for backend in backends:
            for output in outputs[backend]:
                args = '--' + backend + ' --' + output + ' --demo'
                args = set_arguments(args.split())
                setup = PerProfSetup(args)
                self.assertEqual(setup.get_output_format(), output)
                data = self.back_profilers[backend](setup)
                if backend != "tikz":
                    self.assertEqual(data.output, 'performance-profile.{}'.format(output))

    def test_only_name(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/only-name.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_without_time(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/without-time.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_without_c_or_d(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/c-or-d.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_zero_time(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/zero-time.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_yaml_fail(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/yaml-fail.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_empty_file(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/empty.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_empty_subset(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo --subset perprof/tests/empty.subset'
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(AttributeError, self.back_profilers[backend], setup)

    def test_empty_intersection(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo --subset perprof/tests/fantasy.subset'
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

    def test_no_success(self):
        for backend in self.backends:
            if backend == "raw":
                continue
            args = '--' + backend + ' perprof/tests/no-success.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            data = self.back_profilers[backend](setup)
            self.assertRaises(ValueError, data.plot)

    def test_repeated_problem(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/repeat.sample ' + self.goodfiles
            args = set_arguments(args.split())
            setup = PerProfSetup(args)
            self.assertRaises(ValueError, self.back_profilers[backend], setup)

if __name__ == '__main__':
    unittest.main()
