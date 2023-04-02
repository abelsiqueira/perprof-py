from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from perprof.profile_data import ProfileData
from perprof.solver_data import SolverData, read_table

DATA_DIR = Path(__file__).resolve().parent / "test_data/"


@pytest.fixture(name="auxiliary_data")
def fixture_auxiliary_data():
    """DataFrame for simple_solver_a."""
    return {
        "A": pd.DataFrame(
            {
                "name": ["p1", "p2", "p3", "p4", "p5"],
                "exit": ["c", "c", "c", "d", "d"],
                "time": [3.0, 5.0, 8.0, 60.0, 60.0],
                "fval": [np.nan, np.nan, np.nan, np.nan, np.nan],
                "primal": [np.nan, np.nan, np.nan, np.nan, np.nan],
                "dual": [np.nan, np.nan, np.nan, np.nan, np.nan],
            }
        ),
        "B": pd.DataFrame(
            {
                "name": ["p1", "p2", "p3", "p4", "p5"],
                "exit": ["c", "c", "c", "c", "d"],
                "time": [12.0, 2.5, 4.0, 0.1, 60.0],
                "fval": [np.nan, np.nan, np.nan, np.nan, np.nan],
                "primal": [np.nan, np.nan, np.nan, np.nan, np.nan],
                "dual": [np.nan, np.nan, np.nan, np.nan, np.nan],
            }
        ),
        "C": pd.DataFrame(
            {
                "name": ["p1", "p2", "p3", "p4", "p5"],
                "exit": ["c", "c", "c", "c", "d"],
                "time": [12.0, 2.5, 4.0, 0.1, 60.0],
                "fval": [np.nan, np.nan, np.nan, np.nan, np.nan],
                "primal": [np.nan, np.nan, np.nan, np.nan, np.nan],
                "dual": [np.nan, np.nan, np.nan, np.nan, np.nan],
            }
        ),
        "ratio": np.array(
            [
                [1.0, 4.0],
                [2.0, 1.0],
                [2.0, 1.0],
                [float("inf"), 1.0],
                [float("inf"), float("inf")],
            ]
        ),
        "breakpoints": np.array([1.0, 2.0, 4.0]),
        "cumulative": np.array(
            [
                [0.2, 0.6],
                [0.6, 0.6],
                [0.6, 0.8],
            ]
        ),
        "subset": ["p2", "p3"],
        "ratio_subset": np.array(
            [
                [2.0, 1.0],
                [2.0, 1.0],
            ]
        ),
        "breakpoints_subset": np.array([1.0, 2.0]),
        "cumulative_subset": np.array(
            [
                [0.0, 1.0],
                [1.0, 1.0],
            ]
        ),
    }


def test_constructor(auxiliary_data):
    """Test constructor of ProfileData."""
    solver_a = SolverData("A", auxiliary_data["A"])
    profile_data = ProfileData(solver_a, DATA_DIR / "simple_solver_b.table")
    assert np.all(profile_data.ratio == auxiliary_data["ratio"])
    assert np.all(profile_data.breakpoints == auxiliary_data["breakpoints"])
    assert np.all(profile_data.cumulative == auxiliary_data["cumulative"])

    # Fails for invalid input
    with pytest.raises(ValueError):
        ProfileData(1)


def test_process(auxiliary_data):
    """Test ProfileData.process()."""
    solvers = [SolverData(algname, auxiliary_data[algname]) for algname in ["A", "B"]]

    # Fails for single (valid) input
    profile_data = ProfileData(*solvers)
    with pytest.raises(ValueError):
        profile_data.solvers = solvers[0:1]
        profile_data.process()

    # Subset
    profile_data = ProfileData(*solvers, subset=auxiliary_data["subset"])
    assert np.all(profile_data.subset == auxiliary_data["subset"])
    assert np.all(profile_data.ratio == auxiliary_data["ratio_subset"])
    assert np.all(profile_data.breakpoints == auxiliary_data["breakpoints_subset"])
    assert np.all(profile_data.cumulative == auxiliary_data["cumulative_subset"])
