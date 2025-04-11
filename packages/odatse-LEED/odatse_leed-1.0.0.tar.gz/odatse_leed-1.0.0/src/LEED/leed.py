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

from typing import List
from pathlib import Path
import os
from distutils.dir_util import copy_tree
import subprocess
import numpy as np

import odatse
from .parameter import parse_solver_info
from .input import Input
from .output import Output
#from odatse.solver.util import run_by_subprocess, Workdir
from .util import run_by_subprocess, Workdir

class Solver(odatse.solver.SolverBase):
    """LEED (Low Energy Electron Diffraction) solver implementation.
    
    This class implements the solver for LEED calculations, which requires two external
    executables to be run in sequence.
    """
    _name = "leed"

    def __init__(self, info: odatse.Info):
        """Initialize the LEED solver.
        
        Parameters
        ----------
        info : odatse.Info
            Configuration information for the solver
        """
        super().__init__(info)

        # Convert solver-specific configuration
        self.info = parse_solver_info(**info.solver)

        # Locate and validate the external solver executables
        self.path_to_first_solver = self.set_solver_path(self.info.config.path_to_first_solver)
        self.path_to_second_solver = self.set_solver_path(self.info.config.path_to_second_solver)

        # Directory containing reference data and input templates
        self.path_to_base_dir = self.info.reference.path_to_base_dir

        # Ensure all required input files are present
        self.check_files(["exp.d", "rfac.d", "tleed4.i", "tleed5.i"], self.path_to_base_dir)

        # Initialize input generator and output parser
        self.input = Input(self.info)
        self.output = Output(self.info)

    def evaluate(self, x: np.ndarray, args = (), nprocs: int = 1, nthreads: int = 1) -> float:
        """Evaluate the LEED calculation for given parameters.
        
        Parameters
        ----------
        x : np.ndarray
            Input parameters for the calculation
        args : tuple
            Additional arguments (used for work directory naming)
        nprocs : int
            Number of MPI processes (not used in current implementation)
        nthreads : int
            Number of OpenMP threads (not used in current implementation)
            
        Returns
        -------
        float
            Calculation result (typically R-factor)
        """
        # Create unique working directory for this evaluation
        work_dir = "Log{:08d}_{:08d}".format(*args)

        with Workdir(work_dir, remove=self.info.config.remove_work_dir, use_tmpdir=self.info.config.use_tmpdir):
            # Copy reference data and templates to working directory
            for dir in [self.path_to_base_dir]:
                copy_tree(os.path.join(self.root_dir, dir), ".")

            # Generate input files for current parameters
            self.input.generate(x)

            # Run the calculation
            self.run(nprocs, nthreads)

            # Parse and return results
            result = self.output.get_results()

        return result

    def run(self, nprocs: int = 1, nthreads: int = 1) -> None:
        """Execute the LEED calculation sequence.
        
        Runs two solvers in sequence. Catches and reports any execution errors.

        Parameters
        ----------
        nprocs : int
            Number of MPI processes (not used in current implementation)
        nthreads : int
            Number of OpenMP threads (not used in current implementation)

        Note
        ----
        raises RuntimeError when error occurs in either execution of solvers
        """
        # Run first solver (typically phase shift calculation)
        run_by_subprocess([self.path_to_first_solver])
        # Run second solver (typically LEED intensity calculation)
        run_by_subprocess([self.path_to_second_solver])

    def check_files(self, files, base_dir):
        """Check if all required files exist in the base directory.
        
        Parameters
        ----------
        files : list of str
            List of required file names
        base_dir : str
            Directory to check for files
            
        Raises
        ------
        RuntimeError
            If any required file is missing
        """
        for f in files:
            if not os.path.exists(os.path.join(base_dir, f)):
                raise RuntimeError(f"ERROR: input file \"{f}\" not found in \"{base_dir}\"")

    def set_solver_path(self, solver_name: str) -> Path:
        """Locate and validate the solver executable.
        
        Parameters
        ----------
        solver_name : str
            Name or path of the solver executable
            
        Returns
        -------
        Path
            Resolved path to the executable
            
        Raises
        ------
        RuntimeError
            If solver is not found or not executable
        """
        if os.path.dirname(solver_name) != "":
            # If path is provided, resolve relative to root directory
            solver_path = self.root_dir / Path(solver_name).expanduser()
        else:
            # If only name is provided, search in PATH and root directory
            for p in [self.root_dir] + os.environ["PATH"].split(":"):
                solver_path = os.path.join(p, solver_name)
                if os.access(solver_path, mode=os.X_OK):
                    break
        # Final check for executable permission
        if not os.access(solver_path, mode=os.X_OK):
            raise RuntimeError(f"ERROR: solver ({solver_name}) is not found")
        return solver_path

