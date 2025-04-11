# odatse-XAFS -- X-ray Absorption Fine Structure solver module for ODAT-SE
# Copyright (C) 2024- The University of Tokyo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
# 

from typing import List
import itertools
import os
import sys
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
import time

import numpy as np

import odatse
from .input import Input
from .output import Output
from .parameter import SolverInfo

from pydantic import ValidationError

class Solver(odatse.solver.SolverBase):
    """
    Solver class for handling the execution of the FEFF solver for XAFS data analysis.
    """

    path_to_solver: Path

    def __init__(self, info: odatse.Info):
        """
        Initialize the Solver instance.

        Parameters
        ----------
        info : odatse.Info
            Information required to configure the solver.
        """
        super().__init__(info)
        self._name = "feff"

        try:
            info_solver = SolverInfo(**info.solver)
        except ValidationError as e:
            print("ERROR: {}".format(e))
            sys.exit(1)

        p2solver = info_solver.config.feff_exec_file
        if os.path.dirname(p2solver) != "":
            # ignore ENV[PATH]
            self.path_to_solver = self.root_dir / Path(p2solver).expanduser()
        else:
            for P in itertools.chain([self.root_dir], os.environ["PATH"].split(":")):
                self.path_to_solver = Path(P) / p2solver
                if os.access(self.path_to_solver, mode=os.X_OK):
                    break
        if not os.access(self.path_to_solver, mode=os.X_OK):
            raise RuntimeError("ERROR: solver {} is not found".format(p2solver))

        self.use_tmpdir = info_solver.config.use_tmpdir

        self.input = Input(info.base, info_solver)
        self.output = Output(info.base, info_solver)
        self.result = None

    def evaluate(self, x: np.ndarray, args=(), nprocs: int = 1, nthreads: int = 1) -> float:
        """
        Evaluate the solver with the given parameters.

        Parameters
        ----------
        x : np.ndarray
            Input array for the solver.
        args : tuple, optional
            Additional arguments for the solver. Defaults to ().
        nprocs : int, optional
            Number of processes to use. Defaults to 1.
        nthreads : int, optional
            Number of threads to use. Defaults to 1.

        Returns
        -------
        float
            Result of the evaluation.
        """
        # assume current directory is self.proc_dir
        if self.use_tmpdir:
            owd = os.getcwd()
            tmpdir = TemporaryDirectory()
            os.chdir(tmpdir.name)
            print("use_tmpdir: {}".format(tmpdir.name))

        fitted_x_list, workdir, subdirs = self.input.prepare(x, args)

        cwd = os.getcwd()
        for subdir in subdirs:
            os.chdir(subdir)
            self._run(nprocs, nthreads)
            # time.sleep(3)
            os.chdir(cwd)

        result = self.output.get_results(fitted_x_list, subdirs)

        self.input.post(workdir)

        if self.use_tmpdir:
            os.chdir(owd)
            tmpdir.cleanup()

        return result

    def _run(self, nprocs: int = 1, nthreads: int = 1) -> None:
        """
        Run the solver.

        Parameters
        ----------
        nprocs : int, optional
            Number of processes to use. Defaults to 1.
        nthreads : int, optional
            Number of threads to use. Defaults to 1.
        """
        try:
            self._run_by_subprocess([str(self.path_to_solver)])
        except subprocess.CalledProcessError as e:
            print("WARNING: NO ATOMS CLOSE ENOUGH TO OVERLAP ATOM    1,  UNIQUE POT    0!!  Rmt set to Rnorman.  May be error in input file. {}".format(e))

    def _run_by_subprocess(self, command: List[str]) -> None:
        """
        Run the solver using a subprocess.

        Parameters
        ----------
        command : List[str]
            Command to execute the solver.
        """
        with open("stdout", "w") as fi:
            subprocess.run(
                command,
                stdout=fi,
                stderr=subprocess.STDOUT,
                check=True,
            )
