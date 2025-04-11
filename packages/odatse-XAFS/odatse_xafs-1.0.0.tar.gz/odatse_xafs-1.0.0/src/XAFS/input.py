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
import shutil

from pathlib import Path
from typing import List, Dict, Optional, TYPE_CHECKING


class Input(object):
    """
    Class for handling input preparation for the FEFF solver.
    """

    root_dir: Path
    output_dir: Path
    dimension: int
    string_list: List[str]
    polarization_list: List[str]
    feff_input_file: Path
    feff_template_file: Path
    fitted_x_list: List[str]

    def __init__(self, info_base, info_solver):
        """
        Initialize the Input class with the given base and solver information.

        Parameters
        ----------
        info_base : dict
            Object containing base information.
        info_solver : object
            Object containing solver information.
        """
        self.root_dir = info_base["root_dir"]
        self.output_dir = info_base["output_dir"]

        if info_solver.dimension:
            self.dimension = info_solver.dimension
        else:
            self.dimension = info_base["dimension"]

        # solver.param
        self.string_list = info_solver.param.string_list
        self.polarization_list = info_solver.param.polarization_list
        self.polarization = info_solver.param.polarization

        self.call_dir = ["call_{:02d}".format(k+1) for k in range(len(self.polarization))]

        # solver.config
        self.feff_input_file = Path(info_solver.config.feff_input_file)
        self.remove_work_dir = info_solver.config.remove_work_dir
        self.use_tmpdir = info_solver.config.use_tmpdir

        filename = Path(info_solver.config.feff_template_file).expanduser().resolve()
        self.feff_template_file = self.root_dir / filename
        if not self.feff_template_file.exists():
            raise RuntimeError(
                f"ERROR: feff_template_file ({self.feff_template_file}) does not exist"
            )

        self._check_template()

        feff_template_data=[]
        with open(self.feff_template_file, 'r') as file_input:
            for line in file_input:
                feff_template_data.append(line.strip())
        self.feff_template_data_origin = feff_template_data

    def prepare(self, x: np.ndarray, args):
        """
        Prepare the input files and working directory.

        Parameters
        ----------
        x : np.ndarray
            Numpy array of input values.
        args : tuple
            Tuple containing step and iset values.

        Returns
        -------
        tuple
            Tuple containing fitted_x_list, workdir, and subdirs.
        """
        x_list = x
        step, iset = args

        fitted_x_list = ["{:.8f}".format(v) for v in x_list]
        workdir, subdirs = self._create_workdir(step , iset)
        self._generate_input_file(fitted_x_list, workdir)

        return fitted_x_list, workdir, subdirs

    def post(self, work_dir):
        """
        Perform post-processing tasks such as removing the working directory.

        Parameters
        ----------
        work_dir : Path
            Path to the working directory.
        """
        if (not self.use_tmpdir) and self.remove_work_dir:
            def rmtree_error_handler(function, path, excinfo):
                print(f"WARNING: Failed to remove a working directory, {path}")
            print("remove directory: {}".format(work_dir))
            shutil.rmtree(work_dir, onerror=rmtree_error_handler)

    def _generate_input_file(self, fitted_x_list, folder_name):
        """
        Generate the input file based on the template and fitted values.

        Parameters
        ----------
        fitted_x_list : list
            List of fitted values as strings.
        folder_name : str
            Name of the folder to save the input file.
        """
        polarization_list = self.polarization_list
        polar_values = self.polarization
        call_dir = self.call_dir

        for index in range(len(call_dir)):
            polar_value = polar_values[index]
            call_dir_path = os.path.join(folder_name, call_dir[index])

            input_file_path = os.path.join(call_dir_path, self.feff_input_file)

            replaced_lines = []
            for line in self.feff_template_data_origin:
                for i in range(self.dimension):
                    if self.string_list[i] in line:
                        line = line.replace(self.string_list[i], fitted_x_list[i])
                for j in range(len(polarization_list)):
                    if polarization_list[j] in line:
                        line = line.replace(polarization_list[j], str(polar_value[j]), 1)  # Replace only once
                replaced_lines.append(line)

            with open(input_file_path, "w") as file_output:
                for line in replaced_lines:
                    file_output.write(line + "\n")

    def _check_template(self) -> None:
        """
        Check if all required labels appear in the template file.

        Raises
        ------
        ValueError
            If any label is missing in the template file.
        """
        found = [False] * self.dimension
        with open(self.feff_template_file, "r") as file_input:
            for line in file_input:
                for index, keyword in enumerate(self.string_list):
                    if keyword in line:
                        found[index] = True
        if not all(found):
            msg = "ERROR: the following labels do not appear in the template file: "
            msg += ", ".join([v for i, v in enumerate(self.string_list) if not found[i]])
            raise ValueError(msg)

    def _create_workdir(self, Log_number , iset):
        """
        Create the working directory and subdirectories.

        Parameters
        ----------
        Log_number : int
            Log number for the directory name.
        iset : int
            Set number for the directory name.

        Returns
        -------
        tuple
            Tuple containing the workdir and list of subdirs.
        """
        workdir = "Log{:08d}_{:08d}".format(Log_number, iset)
        os.makedirs(workdir, exist_ok=True)

        subdirs = []
        for dir_name in self.call_dir:
            subdir = os.path.join(workdir, dir_name)
            os.makedirs(subdir, exist_ok=True)
            subdirs.append(subdir)

        return workdir, subdirs

