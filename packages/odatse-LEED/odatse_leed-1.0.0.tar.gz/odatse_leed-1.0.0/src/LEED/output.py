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

from .rfactor import RFactor

class Output:
    """Output class for handling LEED calculation results and R-factor calculations.

    This class handles reading output files from LEED calculations and computing various
    types of R-factors to compare theoretical and experimental I-V curves.
    """
    def __init__(self, info):
        """Initialize the Output handler.

        Parameters
        ----------
        info : SolverInfo
            Configuration information containing R-factor settings and other parameters
        """
        # Set R-factor type based on configuration
        if isinstance(info.reference.rfactor, str):
            if info.reference.rfactor.lower() in ["rsq", "rsq_modified", "satleed"]:
                self.rfactor_type = info.reference.rfactor.lower()
            else:
                self.rfactor_type = None
        elif isinstance(info.reference.rfactor, dict):
            self.rfactor_type = None
        else:
            raise ValueError("unsupported rfactor type \"{}\"".format(type(info.reference.rfactor)))
        
        # Store configuration parameters
        self.rfactor = info.reference.rfactor
        self.rescale = info.reference.rescale
        self.smoothing = info.reference.smoothing_factor

        # vi_value is used for Pendry R-factor calculations
        self.vi_value = info.reference.vi_value

        # Check if RPE (Pendry) R-factor should be used
        self.use_rpe = False
        if isinstance(info.reference.rfactor, str):
            if info.reference.rfactor.lower() == "rpe":
                self.use_rpe = True
        elif "rpe" in [s.lower() for s in info.reference.rfactor.keys()]:
            self.use_rpe = True

    def get_results(self) -> float:
        """Calculate the R-factor based on residuals.

        Returns
        -------
        float
            Calculated R-factor value
        """

        # Use result of satleed
        if self.rfactor_type is not None and self.rfactor_type == "satleed":
            rfactor = self.read_from_search_s()
            return rfactor

        # Read the I-V curves from output files
        all_ee_data, all_exp_data, all_calc_data = self.read_iv_data()

        # Calculate appropriate R-factor based on configuration
        if self.rfactor_type is not None:
            if self.rfactor_type == "rsq":
                rfactor = self.calc_rfactor(all_ee_data, all_exp_data, all_calc_data)
            elif self.rfactor_type == "rsq_modified":
                rfactor = self.calc_rfactor_mod(all_ee_data, all_exp_data, all_calc_data)
            else:
                pass
        else:
            rfactor = self.calc_rfactor_class(all_ee_data, all_exp_data, all_calc_data)
        return rfactor

    def read_from_search_s(self):
        """Read R-factor result from search.s file.

        Returns
        -------
        float
            R-factor value from file

        Raises
        ------
        RuntimeError
            If R-factor value cannot be found in file
        """
        filename = "search.s"
        try:
            with open(filename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    if "R-FACTOR" in line:
                        rfactor = float(line.split("=")[1])
                        break
                else:
                    msg = f"R-FACTOR cannot be found in {filename}"
                    raise RuntimeError(msg)
        except FileNotFoundError as e:
            msg = "ERROR: search.s not found."
            raise RuntimeError(msg) from e

        return rfactor

    def calc_rfactor(self, all_ee_data, all_exp_data, all_calc_data):
        """Calculate standard R-factor (root mean square).

        Parameters
        ----------
        all_ee_data : list of ndarray
            Energy values for each I-V curve
        all_exp_data : list of ndarray
            Experimental intensity values
        all_calc_data : list of ndarray
            Calculated intensity values

        Returns
        -------
        float
            Calculated R-factor value
        """
        rss = 0.0  # Sum of squared residuals
        rex = 0.0  # Sum of squared experimental values
        for exp_data, calc_data in zip(all_exp_data, all_calc_data):
            res = exp_data - calc_data
            rs = np.sum(res**2)
            rss += rs
            rex += np.sum(exp_data**2)

        rfactor = np.sqrt(rss / rex)
        return rfactor

    def calc_rfactor_mod(self, all_ee_data, all_exp_data, all_calc_data):
        """Calculate modified R-factor weighted by energy range.

        Parameters
        ----------
        all_ee_data : list of ndarray
            Energy values for each I-V curve
        all_exp_data : list of ndarray
            Experimental intensity values
        all_calc_data : list of ndarray
            Calculated intensity values

        Returns
        -------
        float
            Calculated modified R-factor value
        """
        rval = 0.0
        erange = 0.0
        for ee, ex, th in zip(all_ee_data, all_exp_data, all_calc_data):
            res = ex - th
            rs = np.sum(res**2)
            rx = np.sum(ex**2)
            er = ee[-1] - ee[0]  # Energy range

            rval += rs / rx * er
            erange += er

        rfactor = np.sqrt(rval / erange)
        return rfactor

    def calc_rfactor_class(self, all_ee_data, all_exp_data, all_calc_data):
        """Calculate R-factor using RFactor class implementation.

        Parameters
        ----------
        all_ee_data : list of ndarray
            Energy values for each I-V curve
        all_exp_data : list of ndarray
            Experimental intensity values
        all_calc_data : list of ndarray
            Calculated intensity values

        Returns
        -------
        float
            Calculated R-factor value
        """
        if self.use_rpe:
            if self.vi_value is not None:
                vi_value = self.vi_value
            else:
                vi_value = self.read_vi_param()
        else:
            vi_value = None

        rf = RFactor(modes=self.rfactor, vi=vi_value, smoothing_factor=self.smoothing, rescale=self.rescale)

        rval = 0.0
        erange = 0.0
        for ee, ex, th in zip(all_ee_data, all_exp_data, all_calc_data):
            rv = rf.evaluate(ee, ex, th)
            er = ee[-1] - ee[0]

            rval += rv * er
            erange += er

        rfactor = rval / erange
        return rfactor

    def read_iv_data(self):
        """Read all I-V curve data files.

        Returns
        -------
        tuple
            Contains lists of energy values, experimental data, and theoretical data
        """
        ivfiles = sorted([f for f in os.listdir() if os.path.isfile(f) and f.startswith("iv")])

        ex_all = [[] for i in range(len(ivfiles))]
        th_all = [[] for i in range(len(ivfiles))]
        ee_all = [[] for i in range(len(ivfiles))]

        for f in ivfiles:
            idx = int(f.split("iv")[-1])
            eedata, exdata, thdata = self.read_iv_file(f)

            ex_all[idx-1] = np.array(exdata)
            th_all[idx-1] = np.array(thdata)
            ee_all[idx-1] = np.array(eedata)

        return ee_all, ex_all, th_all

    def read_iv_file(self, filename):
        """Read a single I-V curve data file.

        Parameters
        ----------
        filename : str
            Name of the I-V data file to read

        Returns
        -------
        tuple
            Contains energy values, experimental data, and theoretical data
        """
        exdata = []
        thdata = []
        eex = []
        eth = []

        try:
            with open(filename, "r") as fp:
                lines = fp.readlines()
        except FileNotFoundError as e:
            print(e)
            lines = []

        if len(lines) == 0:
            return eex, exdata, thdata

        # Parse file based on format
        if "TitleText" in lines[0]:
            # Original format
            e, d = None, None
            for line in lines[1:]:
                if line == "":
                    pass
                elif "IV exp" in line:
                    e, d = eex, exdata
                elif "IV theory" in line:
                    e, d = eth, thdata
                else:
                    parts = line.split()
                    if len(parts) >= 2:
                        d.append(float(parts[-1]))
                        e.append(float(parts[0]))
        else:
            # New CSV-like format
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) == 2:
                    exdata.append(float(parts[-1]))
                    eex.append(float(parts[0]))
                elif len(parts) == 3:
                    thdata.append(float(parts[-1]))
                    eth.append(float(parts[0]))
                else:
                    pass

        # Verify data consistency
        assert len(eex) == len(exdata)
        assert len(eth) == len(thdata)
        assert all([x == y for x, y in zip(eex, eth)])

        return eex, exdata, thdata

    def read_vi_param(self):
        """Read imaginary potential parameter from input file.

        Returns
        -------
        float or None
            Vi parameter value if found, None otherwise
        """
        from fortranformat import FortranRecordReader as reader
        filename = "tleed5.i"
        try:
            with open(filename, "r") as fp:
                # skip 6 lines
                for _ in range(6): fp.readline()
                vv, vi, _ = reader('(3F7.2)').read(fp.readline())

        except FileNotFoundError as e:
            print(e)
            return None

        return vi
