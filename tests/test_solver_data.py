from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from perprof.solver_data import SolverData, read_table

DATA_DIR = Path(__file__).resolve().parent / "test_data/"


@pytest.fixture(name="auxiliary_data")
def fixture_auxiliary_data():
    """DataFrame for simple_solver_a."""
    return pd.DataFrame(
        {
            "name": ["p1", "p2", "p3", "p4"],
            "exit": ["c", "c", "c", "d"],
            "time": [3.0, 5.0, 8.0, 60.0],
            "fval": [np.nan, np.nan, np.nan, np.nan],
            "primal": [np.nan, np.nan, np.nan, np.nan],
            "dual": [np.nan, np.nan, np.nan, np.nan],
        }
    )


def test_constructor(auxiliary_data):
    """Test the constructor of SolverData."""
    solver = SolverData("A", DATA_DIR / "simple_solver_a.csv")
    assert solver.algname == "A"
    assert solver.data.equals(auxiliary_data)
    assert solver.success == ["c", "converged", "solved", "success"]

    solver = SolverData("A", DATA_DIR / "simple_solver_a.csv", success=["a", "b", "c"])
    assert solver.success == ["a", "b", "c"]

    solver = SolverData("A", auxiliary_data)
    assert solver.data is auxiliary_data

    with pytest.raises(TypeError):
        SolverData("A", 1)

    for col in ["name", "exit", "time"]:
        input_data = auxiliary_data.rename(columns={col: col + "_"})
        with pytest.raises(ValueError):
            solver = SolverData("A", input_data)


def test_read_table(auxiliary_data):
    """Test function read_table."""
    solver = read_table(DATA_DIR / "simple_solver_a.table")
    assert solver.data.equals(auxiliary_data)
