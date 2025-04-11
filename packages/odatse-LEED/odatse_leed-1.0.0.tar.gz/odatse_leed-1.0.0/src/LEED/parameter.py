# odatse-LEED -- Low Energy Electron Diffraction solver module for ODAT-SE
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

from typing import Tuple, List, Dict, Union, Optional, Annotated
from annotated_types import Len
from pydantic import BaseModel, PositiveInt, ValidationError, Field, field_validator
from numbers import Number

class SolverConfig(BaseModel):
    """
    Configuration for the solver

    Attributes
    ----------
    path_to_first_solver : str
        Path to the first solver executable (phase shift calculation)
    path_to_second_solver : str
        Path to the second solver executable (LEED intensity calculation)  
    sigma_file_path : str
        Path to the experimental data file containing error bars
    remove_work_dir : bool
        Whether to remove working directories after calculation
    use_tmpdir : bool
        Whether to use system temp directory for calculations
    """
    path_to_first_solver: str = "satl1.exe"  # Default path to first solver
    path_to_second_solver: str = "satl2.exe"  # Default path to second solver
    sigma_file_path: str = "exp.d"  # Default path to experimental data
    remove_work_dir: Optional[bool] = False  # Keep work directories by default
    use_tmpdir: Optional[bool] = False  # Use local directory by default

class SolverParam(BaseModel):
    """
    Configuration for the solver

    Attributes
    ----------
    string_list : List[str]
        List of strings to be replaced in the input template files
    """
    string_list: List[str]  # List of parameter strings for template substitution

class SolverReference(BaseModel):
    """
    Reference data for the solver

    Attributes
    ----------
    path_to_base_dir : str
        Path to the directory containing reference data and input templates
    rfactor : Union[str,Dict], optional
        R-factor type specification ("rpe", "rsq", etc.) or dictionary of settings
    rescale : bool, optional
        Whether to rescale intensities during R-factor calculation
    smoothing_factor : float, optional
        Factor for smoothing I-V curves (0.0 means no smoothing)
    vi_value : float, optional
        Imaginary potential parameter for Pendry R-factor calculation
    """
    path_to_base_dir: str = "base"  # Default reference data directory
    rfactor: Optional[Union[str,Dict]] = "rpe"  # Default to Pendry R-factor
    rescale: Optional[bool] = False  # Default to no intensity rescaling
    smoothing_factor: Optional[float] = 0.0  # Default to no smoothing
    vi_value: Optional[float] = None  # Imaginary potential parameter

class SolverInfo(BaseModel):
    """
    Parameters for the LEED solver

    Attributes
    ----------
    name : str
        Name of the solver (default: "leed")
    dimension : int
        Number of optimization parameters
    config : SolverConfig
        Configuration settings for solver executables
    param : SolverParam
        Parameters for input file generation
    reference : SolverReference
        Reference data and R-factor settings
    """
    name: Optional[str] = "leed"  # Default solver name
    dimension: Optional[int] = None  # Number of parameters to optimize
    config: SolverConfig  # Solver executable configuration
    param: SolverParam  # Input parameter configuration  
    reference: SolverReference  # Reference data configuration

def parse_solver_info(**kwargs):
    try:
        info = SolverInfo(**kwargs)
    except ValidationError as e:
        print("----------------")
        print(str(e))
        print("----------------")
        raise ValueError("failed in parsing solver parameters") from e
    return info


if __name__ == "__main__":
    import tomli

    # Example configuration in TOML format
    input_data = """
    [solver]
    [solver.config]
    path_to_solver = "satl2.exe"
    [solver.reference]
    path_to_base_dir = "base"
    """

    # Parse TOML and create SolverInfo instance
    params = tomli.loads(input_data)
    si = SolverInfo(**params["solver"])

    print(si)
