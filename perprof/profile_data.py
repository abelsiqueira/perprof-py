"""Class to store the profile configuration and data."""

from pathlib import Path

import numpy as np

from .solver_data import SolverData, read_table


class ProfileData:
    """Computes and stores the performance profile.

    This class will store and compute the performance profile of given solvers.
    This is only the most basic profile choice, it only uses the time and the convergence status.

    Attributes:
        solvers (list[SolverData]):
            List of solver_data.SolverData objects associated with this performance profile.
        subset (list[str]):
            If not None, used to restrict the problems in which the profile is created.
        ratio (numpy.array):
            Ratio matrix computed using the best time for each problem.
        breakpoints (numpy.array):
            Array of breakpoints obtained from the ratio matrix.
        cumulative (numpy.array):
            Matrix of the cumulative distribution of problems. Dimensions and len(breakpoints) by len(solvers).
    """

    def __init__(self, *solvers, subset=None):
        """Initialize the profile structure with solver_data.SolverData or files.

        Args:
            *solvers (Union[str, Path, SolverData]):
                Arguments of type str/Path to be read through solver_data.read_table or of type solver_data.SolverData. At least 2 arguments are required
            subset (list[str]):
                If not None, restricts the solvers data to only these problems.
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
        self._solvers_data = None
        self.ratio = None
        self._best_times = None
        self.breakpoints = None
        self.cumulative = None
        self.process()

    def process(self):
        """
        Process the solver data.

        If the solvers argument is updated, this should be called again.
        This returns the internal values and returns nothing.
        """
        if len(self.solvers) <= 1:
            raise ValueError("A Profile needs two solvers, at least")

        problems = set(self.solvers[0].data["name"].values)
        for solver in self.solvers[1:]:
            problems = problems.union(set(solver.data["name"].values))
        problems = sorted(list(problems))

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
