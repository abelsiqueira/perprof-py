"""Class and functions related to storing the solver's results."""

from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

from .parse import _parse_yaml


class SolverData:
    """Store data from one solver.

    Attributes:
        algname (str):
            Name of the algorithm
        data (pandas.DataFrame):
            DataFrame with columns

            - "name": The problem name.
            - "exit": Exit flag to determine successful termination.
            - "time": Elapsed time for the algorithm.
            - "fval": Function value at the solution.
            - "primal": Primal residual at the solution.
            - "dual": Dual residual at the solution.
        success (list[str]):
            List of strings used to define what is a successful termination.
    """

    def __init__(
        self,
        algname,
        data,
        success=None,
        read_csv_args=None,
    ):
        """Initializes the SolverData from files or DataFrames.

        Args:
            algname (str):
                Name of the algorithm.
            data (Union[str, Path, pandas.DataFrame]):
                File name of csv to read or DataFrame.
            success (list[str]):
                Vector of flags considered as success.
            read_csv_args (dict):
                Arguments to be passed to `pandas.read_csv` if `data` is a file name.

        Raises:
            TypeError: If the data is not a str, Path, or pandas.DataFrame.
        """
        self.algname = algname
        if not success:
            success = ["c", "converged", "solved", "success"]
        self.success = success
        if isinstance(data, (str, Path)):
            if not read_csv_args:
                read_csv_args = {}
            self.data = pd.read_csv(data, **read_csv_args)
        elif isinstance(data, pd.DataFrame):
            self.data = data
        else:
            raise TypeError("Unexpected type for data input")

        # Make sure that a columns name, time and exit exist
        for col in ["name", "exit", "time"]:
            if col not in self.data.columns:
                raise ValueError(f"Missing column {col}")
        for col in ["fval", "primal", "dual"]:
            if col not in self.data:
                self.data[col] = np.nan


def read_table(filename):
    """
    Read a table file as described in the documentation section [File Format](file-format).

    Args:
        filename (str):
            Name of the table file.

    Returns:
        solver (SolverData): Parsed data
    """
    options = {
        "algname": None,
        "success": "c,converged,solved,success",
        "free_format": True,
        "col_name": 1,
        "col_exit": 2,
        "col_time": 3,
        "col_fval": 4,
        "col_primal": 5,
        "col_dual": 6,
    }

    with open(filename, encoding="utf-8") as file_:
        lines = file_.readlines()

        in_yaml = False
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if in_yaml:
                    yaml_header = lines[0:i]
                    data_lines = lines[i + 1 :]
                    break
                in_yaml = True

    _parse_yaml(options, "".join(yaml_header))
    options["success"] = options["success"].split(",")
    data_header = ["name", "exit", "time", "fval", "primal", "dual"]
    header_order = [
        options["col_name"],
        options["col_exit"],
        options["col_time"],
        options["col_fval"],
        options["col_primal"],
        options["col_dual"],
    ]
    data_header = [data_header[i - 1] for i in header_order]
    data = pd.read_csv(
        StringIO("".join([" ".join(data_header) + "\n"] + data_lines)),
        delim_whitespace=True,
    )

    return SolverData(
        options["algname"],
        data,
        success=options["success"],
    )
