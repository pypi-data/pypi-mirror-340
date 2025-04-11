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

import os
import numpy as np

from pathlib import Path
from typing import List, Dict, Tuple, Optional, TYPE_CHECKING


class Output(object):
    """
    Output manager for handling the results of the FEFF solver.
    """

    dimension: int
    string_list: List[str]
    feff_output_file: str
    calculated_first_k: float
    calculated_last_k: float
    k_range: Tuple[float]
    remove_work_dir: bool
    polarization: List[List[float]]

    def __init__(self, info_base, info_solver):
        """
        Initialize the Output class with the given base and solver information.

        Parameters
        ----------
        info_base
            Object containing base information.
        info_solver
            Object containing solver information.
        """
        if info_solver.dimension:
            self.dimension = info_solver.dimension
        else:
            self.dimension = info_base["dimension"]

        # solver.config
        self.feff_output_file = info_solver.config.feff_output_file
        self.remove_work_dir = info_solver.config.remove_work_dir

        # solver.param
        self.string_list = info_solver.param.string_list
        self.polarization = info_solver.param.polarization
        self.k_range = info_solver.param.k_range

        # solver.reference
        reference_epsilon_path = info_solver.reference.path_epsilon
        self._read_reference(reference_epsilon_path, self.k_range)

    def _read_reference(self, file_path, k_range, skiprows=2):
        """
        Read the reference data from the given file.

        Parameters
        ----------
        file_path : str
            Path to the reference file.
        k_range : tuple
            Tuple containing the minimum and maximum k values.
        skiprows : int, optional
            Number of rows to skip at the beginning of the file. Defaults to 2.
        """
        data = np.loadtxt(file_path, skiprows=skiprows, unpack=True)

        k = data[0]
        kmin, kmax = k_range
        mask = (k >= kmin) & (k <= kmax)

        self.k = k[mask]
        self.exp_data = []
        for i in range(1, len(data), 2):
            chi = data[i][mask]
            eps = data[i+1][mask]
            self.exp_data.append((chi, eps))

    def get_results(self, fitted_x_list, subdirs) -> float:
        """
        Get Rfactor obtained by the solver program.

        Parameters
        ----------
        fitted_x_list : list
            List of fitted x values.
        subdirs : list
            List of subdirectories containing the output files.

        Returns
        -------
        float
            The average R-factor value.
        """
        dimension = self.dimension
        string_list = self.string_list
        polar_values = self.polarization

        rfactors = []
        for idx in range(len(subdirs)):
            output_file = Path(subdirs[idx], self.feff_output_file)
            calc = self._read_calc_result(output_file, self.k_range)
            if calc:
                rfac = self._calc_Rfactor(*calc, self.exp_data[idx])
            else:
                rfac = float("inf")
            rfactors.append(rfac)

        Rfactor = np.average(rfactors)

        #if Rfactor <= 2:
        if True:
            # print("The R-factor value is less than 2.")
            for idx in range(dimension):
                print("{} = {}".format(string_list[idx], fitted_x_list[idx]))
            message = "R-factor = {}".format(Rfactor)
            for idx in range(len(subdirs)):
                message += " Polarization {} R-factor{} = {} ".format(str(polar_values[idx]), idx+1, rfactors[idx])
            print(message)

        return Rfactor

    def _read_calc_result(self, file_path, k_range):
        """
        Read the calculated result from the given file.

        Parameters
        ----------
        file_path : str
            Path to the calculation result file.
        k_range : tuple
            Tuple containing the minimum and maximum k values.

        Returns
        -------
        tuple
            A tuple containing the masked k values and the corresponding calculated values.
        """
        if not Path(file_path).exists():
            print("WARNING: file not found: {}".format(file_path))
            return None

        data = np.loadtxt(file_path, unpack=True)

        k = data[0]
        kmin, kmax = k_range
        mask = (k >= kmin) & (k <= kmax)

        return data[0][mask], data[1][mask]

    def _calc_Rfactor(self, k, calc, ref):
        """
        Calculate the R-factor for the given calculated and reference data.

        Parameters
        ----------
        k : numpy.ndarray
            Array of k values.
        calc : numpy.ndarray
            Array of calculated values.
        ref : tuple
            Tuple containing the reference chi and epsilon values.

        Returns
        -------
        float
            The calculated R-factor.
        """
        if calc is None:
            return float("inf")

        chi, eps = ref
        N = len(k)
        R = (1/N) * np.sum((np.square(np.subtract(chi, calc))) / (np.square(eps)))
        return R
