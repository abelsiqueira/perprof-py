import pytest

from perprof import bokeh, matplotlib, prof, tikz
from perprof.main import process_arguments, set_arguments

goodfiles = " ".join(
    ["perprof/examples/" + s + ".table" for s in ["alpha", "beta", "gamma"]]
)
backends = ["bokeh", "tikz", "mp", "raw"]
back_profilers = {
    "bokeh": bokeh.Profiler,
    "tikz": tikz.Profiler,
    "mp": matplotlib.Profiler,
    "raw": prof.Pdata,
}


def test_backends():
    for backend in backends:
        args = "--" + backend + " --demo"
        isTrue = {"bokeh": False, "tikz": False, "mp": False, "raw": False}
        isTrue[backend] = True
        args = set_arguments(args.split())
        assert args.bokeh == isTrue["bokeh"]
        assert args.tikz == isTrue["tikz"]
        assert args.mp == isTrue["mp"]
        assert args.raw == isTrue["raw"]


@pytest.mark.parametrize(
    "backend,outputs",
    [
        ("bokeh", ["html"]),
        ("tikz", ["pdf", "tex"]),
        ("mp", ["png", "eps", "pdf", "ps", "svg"]),
        ("raw", []),
    ],
)
def test_output_formats(backend, outputs):
    for output in outputs:
        args = "--" + backend + " --" + output + " --demo"
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        assert profiler_options["output_format"] == output
        data = back_profilers[backend](parser_options, profiler_options)
        if backend != "tikz":
            assert data.output == f"performance-profile.{output}"


def test_only_name():
    for backend in backends:
        args = "--" + backend + " tests/only-name.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_columns():
    for backend in backends:
        baseargs = "--" + backend + " " + goodfiles
        # Default comparison needs 3 columns
        args = baseargs + " tests/2-col.sample "
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)
        # Default values should fail with 5 or less columns.
        # Unconstrained Default values should fail with 5 or less columns
        # (because dual default column is 5).
        baseargs = "--compare optimalvalues " + baseargs
        for xtra in ["", "--unconstrained "]:
            baseargs = xtra + baseargs
            for n in [2, 3, 4, 5]:
                args = baseargs + f" tests/{n}-col.sample "
                args = set_arguments(args.split())
                parser_options, profiler_options = process_arguments(args)
                with pytest.raises(ValueError):
                    back_profilers[backend](parser_options, profiler_options)


def test_without_time():
    for backend in backends:
        args = "--" + backend + " tests/without-time.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_without_c_or_d():
    for backend in backends:
        args = "--" + backend + " tests/c-or-d.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_zero_time():
    for backend in backends:
        args = "--" + backend + " tests/zero-time.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_yaml_fail():
    for backend in backends:
        args = "--" + backend + " tests/yaml-fail.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_empty_file():
    for backend in backends:
        args = "--" + backend + " tests/empty.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_empty_subset():
    for backend in backends:
        args = "--" + backend + " --demo --subset tests/empty.subset"
        args = set_arguments(args.split())
        with pytest.raises(AttributeError):
            process_arguments(args)


def test_empty_intersection():
    for backend in backends:
        args = "--" + backend + " --demo --subset tests/fantasy.subset"
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)


def test_no_success():
    for backend in backends:
        if backend == "raw":
            continue
        args = "--" + backend + " tests/no-success.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        data = back_profilers[backend](parser_options, profiler_options)
        with pytest.raises(ValueError):
            data.plot()


def test_repeated_problem():
    for backend in backends:
        args = "--" + backend + " tests/repeat.sample " + goodfiles
        args = set_arguments(args.split())
        parser_options, profiler_options = process_arguments(args)
        with pytest.raises(ValueError):
            back_profilers[backend](parser_options, profiler_options)
