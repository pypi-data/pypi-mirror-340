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

import sys
import odatse

from .leed import Solver


def main():
    """
    Main function to run the data-analysis software for quantum beam diffraction experiments
    on material surface structures. It parses command-line arguments, loads the input file,
    selects the appropriate algorithm and solver, and executes the analysis.
    """

    info, run_mode = odatse.initialize()

    alg_module = odatse.algorithm.choose_algorithm(info.algorithm["name"])

    solver = Solver(info)
    runner = odatse.Runner(solver, info)
    alg = alg_module.Algorithm(info, runner, run_mode=run_mode)

    result = alg.main()
