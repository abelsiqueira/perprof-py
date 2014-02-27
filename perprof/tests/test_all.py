import unittest
import perprof
from perprof.main import PerProfSetup
from perprof.main import set_arguments
from perprof import tikz

class TestPerprof(unittest.TestCase):

    goodfiles = ' '.join(['perprof/examples/' + s + '.table' \
            for s in ['alpha', 'beta', 'gamma']])

    def test_backends(self):
        for backend in ['tikz', 'mp', 'raw']:
            args = '--' + backend + ' fakefile'
            isTrue = {'tikz': False, 'mp': False, 'raw': False }
            isTrue[backend] = True
            args = set_arguments(args.split())
            self.assertEqual(args.tikz, isTrue['tikz'])
            self.assertEqual(args.mp,   isTrue['mp'])
            self.assertEqual(args.raw,  isTrue['raw'])

    def test_output_formats(self):
        outputs = {
                "tikz": ["pdf", "tex"],
                "mp": ["png"] }
        backends = ['tikz', 'mp']
        for backend in backends:
            for output in outputs[backend]:
                args = '--' + backend + ' --' + output + ' fakefile'
                args = set_arguments(args.split())
                setup = PerProfSetup(args)
                self.assertEqual(setup.get_output_format(), output)

    def test_only_name(self):
        args = '--tikz perprof/tests/only-name.sample'
        args = set_arguments(args.split())
        setup = PerProfSetup(args)
        self.assertRaises(ValueError, tikz.Profiler, setup, args.standalone)

    def test_without_time(self):
        args = '--tikz perprof/tests/without-time.sample'
        args = set_arguments(args.split())
        setup = PerProfSetup(args)
        self.assertRaises(ValueError, tikz.Profiler, setup, args.standalone)

    def test_no_free_format(self):
        args = '--tikz ' + self.goodfiles
        args = set_arguments(args.split())
        setup = PerProfSetup(args)
        self.assertRaises(ValueError, tikz.Profiler, setup, args.standalone)

if __name__ == '__main__':
    unittest.main()
