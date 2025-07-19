"""Class to store the profile configuration and data."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd

from .solver_data import SolverData, read_table


class ProfileData:
    """Computes and stores performance profiles for algorithm comparison.

    Implements the Dolan and Moré performance profile methodology. Processes solver
    timing data and computes the fraction of problems solved by each solver within
    performance ratios relative to the best solver.

    Attributes:
        solvers (list[SolverData]):
            List of solver_data.SolverData objects associated with this performance profile.
        subset (list[str]):
            If not None, used to restrict the problems in which the profile is created.
        ratio (numpy.array):
            Ratio matrix computed using the best time for each problem.
            Shape: (n_problems, n_solvers). Entry [i,j] = time[i,j] / min_time[i]
        breakpoints (numpy.array):
            Array of unique ratio values sorted in ascending order.
            Used as x-axis values for profile visualization.
        cumulative (numpy.array):
            Matrix of cumulative distribution of problems solved.
            Shape: (len(breakpoints), n_solvers). Entry [i,j] = fraction of problems
            where solver j has ratio <= breakpoints[i].

    Example:
        >>> import pandas as pd
        >>> from perprof.profile_data import ProfileData
        >>> from perprof.solver_data import SolverData
        >>>
        >>> # Create solver data from DataFrames
        >>> data1 = pd.DataFrame({
        ...     "name": ["prob1", "prob2"],
        ...     "exit": ["converged", "converged"],
        ...     "time": [1.0, 2.0]
        ... })
        >>> data2 = pd.DataFrame({
        ...     "name": ["prob1", "prob2"],
        ...     "exit": ["converged", "converged"],
        ...     "time": [1.5, 1.5]
        ... })
        >>> solver1 = SolverData("Newton", data1, success=["converged"])
        >>> solver2 = SolverData("BFGS", data2, success=["converged"])
        >>>
        >>> # Create performance profile
        >>> profile = ProfileData(solver1, solver2)
        >>>
        >>> # Access computed data
        >>> print(f"Ratio matrix shape: {profile.ratio.shape}")
        Ratio matrix shape: (2, 2)
        >>> print(f"Number of breakpoints: {len(profile.breakpoints)}")
        Number of breakpoints: 3
    """

    def __init__(
        self, *solvers: Union[str, Path, SolverData], subset: list[str] | None = None
    ) -> None:
        """Initialize performance profile with solver data or file paths.

        Args:
            *solvers (Union[str, Path, SolverData]):
                Solver data sources. Can be:
                - File paths (str/Path) to YAML files with solver results
                - SolverData objects with pre-loaded data
                At least 2 solvers are required for comparison.
            subset (list[str], optional):
                If provided, restricts the analysis to only these problem names.
                Useful for focusing on specific problem subsets.

        Raises:
            ValueError: If solver input type is not supported or fewer than 2 solvers provided.

        Example:
            >>> import pandas as pd
            >>> from perprof.profile_data import ProfileData
            >>> from perprof.solver_data import SolverData
            >>>
            >>> # From SolverData objects with DataFrames
            >>> data1 = pd.DataFrame({"name": ["prob1", "prob2"], "exit": ["converged", "converged"], "time": [1.2, 3.4]})
            >>> data2 = pd.DataFrame({"name": ["prob1", "prob2"], "exit": ["converged", "converged"], "time": [1.5, 2.8]})
            >>> solver1 = SolverData("Method1", data1)
            >>> solver2 = SolverData("Method2", data2)
            >>> profile = ProfileData(solver1, solver2)
            >>>
            >>> # With problem subset
            >>> profile_subset = ProfileData(solver1, solver2, subset=["prob1"])
            >>> len(profile_subset._solvers_data)
            1
        """
        self.solvers = []
        for solver in solvers:
            if isinstance(solver, (str, Path)):
                self.solvers.append(read_table(solver))
            elif isinstance(solver, SolverData):
                self.solvers.append(solver)
            else:
                raise ValueError(f"Unexpected type for solver input: {type(solver)}")
        self.subset = subset

        # Variables that will be filled by self.process()
        self._solvers_data: pd.DataFrame | None = None
        self.ratio: np.ndarray | None = None
        self._best_times: np.ndarray | None = None
        self.breakpoints: np.ndarray | None = None
        self.cumulative: np.ndarray | None = None
        self.process()

    def process(self) -> None:
        """Process solver data to compute performance profile.

        Computes ratio matrix, breakpoints, and cumulative distribution:
        1. Merge solver data into unified DataFrame
        2. Set failed convergence times to infinity
        3. Compute ratio matrix: time[solver,problem] / min_time[problem]
        4. Generate breakpoints from unique ratio values
        5. Compute cumulative distribution

        Raises:
            ValueError: If fewer than 2 solvers are provided.

        Example:
            >>> import pandas as pd
            >>> from perprof.profile_data import ProfileData
            >>> from perprof.solver_data import SolverData
            >>>
            >>> # Create test data
            >>> data1 = pd.DataFrame({"name": ["prob1", "prob2"], "exit": ["converged", "converged"], "time": [1.0, 2.0]})
            >>> data2 = pd.DataFrame({"name": ["prob1", "prob2"], "exit": ["converged", "converged"], "time": [1.5, 1.5]})
            >>> solver1 = SolverData("Solver1", data1, success=["converged"])
            >>> solver2 = SolverData("Solver2", data2, success=["converged"])
            >>> profile = ProfileData(solver1, solver2)
            >>>
            >>> # Check computed ratios and cumulative distribution exist
            >>> profile.ratio is not None
            True
            >>> profile.cumulative is not None
            True
        """
        if len(self.solvers) <= 1:
            raise ValueError("A Profile needs two solvers, at least")

        # create the reduced dataset: |subset| x |solvers|
        cols = ["name", "time"]
        self._solvers_data = self.solvers[0].data[cols].copy()
        for solver in self.solvers[1:]:
            self._solvers_data = self._solvers_data.join(
                solver.data[cols].set_index("name"),
                on="name",
                rsuffix="_" + solver.algname,
            )
        self._solvers_data = self._solvers_data.rename(
            columns={"time": "time_" + self.solvers[0].algname}
        )

        # set to inf the ones that fail convergence
        for solver in self.solvers:
            mask = ~solver.data.exit.isin(solver.success)
            if np.any(mask):
                self._solvers_data.loc[mask, "time_" + solver.algname] = float("inf")

        self._solvers_data.fillna(float("inf"))
        if self.subset:
            self._solvers_data = self._solvers_data[
                self._solvers_data.name.isin(self.subset)
            ]

        # Compute the minimum time
        self._best_times = self._solvers_data.iloc[:, 1:].min(axis=1).values

        # Compute the cumulative distribution
        self.ratio = (
            self._solvers_data.iloc[:, 1:] / self._best_times[:, np.newaxis]
        ).values
        self.ratio[np.isnan(self.ratio)] = float("inf")
        self.breakpoints = np.sort(np.unique(self.ratio.reshape(-1)))
        # This removes inf and nan
        self.breakpoints = self.breakpoints[self.breakpoints < float("inf")]
        # self
        self.cumulative = (
            self.ratio[np.newaxis, :, :] <= self.breakpoints[:, np.newaxis, np.newaxis]
        )
        self.cumulative = self.cumulative.sum(axis=1) / self.ratio.shape[0]
