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

from typing import Tuple, List, Dict, Union, Optional, Annotated, Literal, Set
from typing_extensions import Self
from annotated_types import Len
from pydantic import BaseModel, PositiveInt, ValidationError, Field, field_validator, model_validator, FilePath, conlist, PositiveFloat, NonNegativeInt
from numbers import Number

from pathlib import Path


class SolverConfig(BaseModel):
    """
    Configuration for the FEFF solver.

    Attributes
    ----------
    feff_exec_file : str
        Path to the FEFF executable file.
    feff_input_file : str
        Name of the FEFF input file.
    feff_output_file : str
        Name of the FEFF output file.
    feff_template_file : str
        Name of the FEFF template file.
    remove_work_dir : bool
        Flag to remove the working directory after execution.
    use_tmpdir : bool
        Flag to use a temporary directory for execution.
    """
    feff_exec_file: str = "feff85L"
    feff_input_file: str = "feff.inp"
    feff_output_file: str = "chi.dat"
    feff_template_file: str = "template.txt"
    remove_work_dir: bool = False
    use_tmpdir: bool = False
class SolverParam(BaseModel):
    """
    Parameters for the FEFF solver.

    Attributes
    ----------
    string_list : List[str]
        List of strings to be replaced in the template.
    polarization_list : List[str]
        List of polarization labels.
    polarization : List[List[float]]
        List of polarization vectors.
    calculated_first_k : Union[float, int]
        First k value for calculation.
    calculated_last_k : Union[float, int]
        Last k value for calculation.
    k_range : List[float]
        Range of k values for calculation.
    """
    string_list: List[str]
    polarization_list: List[str] = ["@Ex", "@Ey", "@Ez"]
    polarization: List[List[float]]
    calculated_first_k: Optional[Union[float,int]] = None
    calculated_last_k: Optional[Union[float,int]] = None
    k_range: Optional[List[float]] = None

    @model_validator(mode="after")
    def check_k_range(self) -> Self:
        """
        Validate the k range parameters.

        Raises
        ------
        ValueError
            If the k range parameters are not correctly defined.
        """
        if ((self.calculated_first_k is not None and self.calculated_last_k is None)
            or (self.calculated_first_k is None and self.calculated_last_k is not None)):
            raise ValueError("either calculated_first_k or calculated_last_k is not defined")
        if ((self.calculated_first_k is None and self.calculated_last_k is None)
            and self.k_range is None):
            raise ValueError("either calculated_first/last_k or k_range must be defined")
        if ((self.calculated_first_k is not None and self.calculated_last_k is not None)
            and self.k_range is not None):
            raise ValueError("either calculated_first/last_k or k_range and not both should be defined")
        if (self.k_range is not None and len(self.k_range) != 2):
            raise ValueError("k_range should be [kmin, kmax]")

        if self.k_range is None:
            self.k_range = [self.calculated_first_k, self.calculated_last_k]
        else:
            self.calculated_first_k = self.k_range[0]
            self.calculated_last_k = self.k_range[1]

        return self
        return self

class SolverReference(BaseModel):
    """
    Reference data for the FEFF solver.

    Attributes
    ----------
    path_epsilon : Path
        Path to the epsilon reference file.
    """
    path_epsilon: Path

class SolverInfo(BaseModel):
    """
    Information for the FEFF solver.

    Attributes
    ----------
    name : str
        Name of the solver.
    dimension : int
        Dimension of the solver.
    config : SolverConfig
        Configuration for the solver.
    param : SolverParam
        Parameters for the solver.
    reference : SolverReference
        Reference data for the solver.
    """
    name: Optional[str] = "xafs"
    dimension: Optional[int] = None
    config: SolverConfig
    param: SolverParam
    reference: SolverReference

    @model_validator(mode="after")
    def check_field_lengths(self) -> Self:
        """
        Validate the lengths of the fields.

        Raises
        ------
        ValueError
            If the lengths of the fields do not match the expected values.
        """
        if self.dimension is not None and self.dimension != len(self.param.string_list):
            raise ValueError("length of string_list does not match dimension")
        if len(self.param.polarization_list) != 3:
            raise ValueError("length of polarization_list is not 3")
        if not all([len(v) == len(self.param.polarization_list) for v in self.param.polarization]):
            raise ValueError("lengths of polarization elements are not 3")
        return self


if __name__ == "__main__":
    import tomli
    from devtools import pprint

    input_data = """
[solver]
name = "xafs"
dimension = 3

[solver.config]
#feff_exec_file  = "../bin/feff85L"
feff_output_file = "./chi.dat"
remove_work_dir = false
use_tmpdir = false

[solver.param]
string_list = ["value_01", "value_02","value_03"]
polarization_list = ["polarization_01", "polarization_02", "polarization_03"]
polarization = [ [0,1,0], [1,0,0], [0,0,1] ]
#calculated_first_k = 3.6
#calculated_last_k = 10
k_range = [3.6, 10]

[solver.reference]
path_epsilon = "mock_data.txt"

"""

    params = tomli.loads(input_data)
    si = SolverInfo(**params["solver"])

    pprint(si)
