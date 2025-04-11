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

from typing import Dict, List, Tuple
from pathlib import Path

import os
import numpy as np

#from odatse.solver.template import Template
from .template import Template

class Input:
    """Class for handling LEED input file generation.

    This class manages the creation of input files for the LEED calculation
    by using templates and parameter substitution.
    """

    def __init__(self, info):
        """Initialize input file generator.

        Parameters
        ----------
        info : SolverInfo
            Configuration information containing parameters and paths

        Notes
        -----
        Sets up Fortran format specifications for different parameter types:
        - IP: Inner potential parameters (F7.2 format)
        - opt: Optimization parameters (F7.4 format) 
        - debye: Debye temperature parameters (F9.4 format)
        """
        # Define Fortran format specifications for different parameter types
        format_list = {
            "IP": "F7.2",    # Format for inner potential parameters
            "opt": "F7.4",   # Format for optimization parameters
            "debye": "F9.4", # Format for Debye temperature parameters
        }

        # Get list of parameter strings and base directory from config
        string_list = info.param.string_list
        base_dir = info.reference.path_to_base_dir

        # Initialize template objects for both LEED calculation steps
        self.tmpl4 = Template(file=os.path.join(base_dir, "tleed4.i"), keywords=string_list, format=format_list, style="fortran")
        self.tmpl5 = Template(file=os.path.join(base_dir, "tleed5.i"), keywords=string_list, format=format_list, style="fortran")

    def generate(self, xs: np.ndarray):
        """Generate input files by substituting parameters.

        Creates tleed4.i and tleed5.i input files by substituting the provided
        parameter values into the templates.

        Parameters
        ----------
        xs : np.ndarray
            Array of parameter values to substitute into templates
        """
        # Generate input files for both LEED calculation steps
        self.tmpl4.generate(xs, output="tleed4.i")
        self.tmpl5.generate(xs, output="tleed5.i")

