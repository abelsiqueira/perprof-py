"""Class and functions related to storing the solver's results."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import TypedDict, Union

import numpy as np
import pandas as pd

from .parse import _parse_yaml


class _ParseOptions(TypedDict):
    """Type definition for parse options dictionary."""

    algname: str | None
    success: str
    free_format: bool
    col_name: int
    col_exit: int
    col_time: int
    col_fval: int
    col_primal: int
    col_dual: int


class SolverData:
    """Store performance data from a single solver/algorithm.

    Contains performance metrics and metadata for one solver across multiple test problems.

    Attributes:
        algname (str):
            Name of the algorithm/solver being analyzed.
        data (pandas.DataFrame):
            DataFrame containing performance results with required columns:

            - "name": The problem name (string identifier).
            - "exit": Exit flag to determine successful termination.
            - "time": Elapsed time for the algorithm (float, seconds).
            - "fval": Function value at the solution (optional).
            - "primal": Primal residual at the solution (optional).
            - "dual": Dual residual at the solution (optional).
        success (list[str]):
            List of exit flag values considered successful termination.
            Default: ["c", "converged", "solved", "success"]

    Example:
        >>> import pandas as pd
        >>> from perprof.solver_data import SolverData
        >>>
        >>> # Create from DataFrame
        >>> data = pd.DataFrame({
        ...     "name": ["prob1", "prob2", "prob3"],
        ...     "exit": ["converged", "converged", "failed"],
        ...     "time": [1.2, 3.4, 10.0]
        ... })
        >>> solver = SolverData("Newton", data)
        >>>
        >>> # Access data
        >>> solver.algname
        'Newton'
        >>> len(solver.data)
        3
        >>> successful = solver.data[solver.data.exit.isin(solver.success)]
        >>> len(successful) / len(solver.data) > 0.5
        True
    """

    def __init__(
        self,
        algname: str,
        data: Union[str, Path, pd.DataFrame],
        success: list[str] | None = None,
        read_csv_args: dict | None = None,
    ) -> None:
        """Initialize SolverData from file or DataFrame.

        Args:
            algname (str):
                Name of the algorithm/solver for identification.
            data (Union[str, Path, pd.DataFrame]):
                Source of performance data. Can be:
                - File path (str/Path) to CSV file with solver results
                - Pre-loaded pandas DataFrame with required columns
            success (list[str], optional):
                Exit flag values considered successful termination.
                If None, defaults to ["c", "converged", "solved", "success"].
            read_csv_args (dict, optional):
                Additional arguments passed to pandas.read_csv when loading files.
                Useful for custom separators, encoding, etc.

        Raises:
            TypeError: If data is not a supported type (str, Path, or DataFrame).
            ValueError: If required columns ("name", "exit", "time") are missing.

        Example:
            >>> # From DataFrame
            >>> import pandas as pd
            >>> from perprof.solver_data import SolverData
            >>> df = pd.DataFrame({
            ...     "name": ["prob1", "prob2"],
            ...     "exit": ["converged", "failed"],
            ...     "time": [1.0, 5.0]
            ... })
            >>> solver = SolverData("MyAlgorithm", df)
            >>> solver.algname
            'MyAlgorithm'
            >>>
            >>> # Custom success flags
            >>> solver2 = SolverData("Algorithm2", df, success=["optimal", "feasible"])
            >>> solver2.success
            ['optimal', 'feasible']
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


def read_table(filename: Union[str, Path]) -> SolverData:
    """Read solver data from YAML-formatted table file.

    Parses files with YAML front matter and tabular data. Standard format for
    perprof solver data files.

    File format:
        ```
        ---
        Solver Name: MyAlgorithm
        Success: converged,optimal
        ---
        problem1 converged 1.23 0.001
        problem2 failed 5.67 0.1
        problem3 converged 2.45 0.01
        ```

    Args:
        filename (Union[str, Path]):
            Path to the table file with YAML header and data rows.

    Returns:
        SolverData: Parsed solver data ready for profile analysis.

    Example:
        The file format combines YAML metadata with tabular data:

        >>> # File content example (not actual doctest):
        >>> # ---
        >>> # Solver Name: MyAlgorithm
        >>> # Success: converged,optimal
        >>> # ---
        >>> # problem1 converged 1.23 0.001
        >>> # problem2 failed 5.67 0.1
        >>> pass  # Placeholder since file operations can't be tested in doctest
    """
    options: _ParseOptions = {
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
    success_list = options["success"].split(",")
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
        options["algname"] or "Unknown",
        data,
        success=success_list,
    )
