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

import numpy as np

# This module implements various functions and classes for calculating R-factors
# between experimental and theoretical LEED I-V curves. R-factors are reliability
# factors that quantify the agreement between experiment and theory.

def calc_deriv_cubic_spline(x, f):
    """Calculate derivatives using cubic spline interpolation.

    Uses SciPy's CubicSpline with natural boundary conditions to compute smooth
    first and second derivatives of a function given by discrete points.

    Parameters
    ----------
    x : array_like
        x coordinates of data points
    f : array_like 
        y coordinates of data points

    Returns
    -------
    fp : ndarray
        First derivative at x points
    fpp : ndarray
        Second derivative at x points
    """
    from scipy.interpolate import CubicSpline
    spl = CubicSpline(x, f, bc_type="natural")
    fp = spl(x, nu=1)
    fpp = spl(x, nu=2)
    return fp, fpp

def calc_deriv_bspline(x, f, smoothing_factor):
    """Calculate derivatives using B-spline interpolation with smoothing.

    Uses SciPy's B-spline routines to fit a smoothing spline to the data and
    compute derivatives. The smoothing factor controls the trade-off between
    smoothness and accuracy of the fit.

    Parameters
    ----------
    x : array_like
        x coordinates of data points
    f : array_like
        y coordinates of data points
    smoothing_factor : float
        Smoothing factor for B-spline fitting. Larger values give smoother curves.

    Returns
    -------
    fx : ndarray
        Smoothed function values
    fp : ndarray
        First derivative at x points
    fpp : ndarray
        Second derivative at x points
    """
    from scipy.interpolate import BSpline, splrep, splev
    # Use 1/f as weights to give less weight to larger intensities
    tck = splrep(x, f, w=1/f, s=smoothing_factor)
    bspl = BSpline(*tck)

    fx = splev(x, bspl, der=0)
    fp = splev(x, bspl, der=1)
    fpp = splev(x, bspl, der=2)

    return fx, fp, fpp

def peak_average(x, y, yp):
    """Calculate average of peak values in y.

    Finds peaks in the data by looking for zero crossings in the derivative
    where the slope changes from positive to negative, and averages the peak
    values that exceed a threshold.

    Parameters
    ----------
    x : array_like
        x coordinates
    y : array_like
        y coordinates
    yp : array_like
        First derivative of y

    Returns
    -------
    float
        Average of peak values above threshold
    """
    # Set threshold at 2% of maximum y value
    threshold = np.max(y) / 50.0

    # Find peaks using derivative zero crossings
    m1 = yp * np.roll(yp, -1) < 0.0  # Zero crossing
    m2 = yp > 0.0                     # Positive to negative
    m3 = y > threshold                # Above threshold
    m = m1 & m2 & m3
    m[-1] = False                     # Exclude last point

    # Calculate average of peaks
    n = np.count_nonzero(m)
    avg = np.sum(y[m]) / n

    return avg

def calc_yfunc(x, y, yp, *, vi, persh=0.05):
    """Calculate Pendry Y-function.

    The Y-function transforms the I-V curves to emphasize peak positions rather
    than intensities. It is used in calculating the Pendry R-factor.

    Parameters
    ----------
    x : array_like
        x coordinates (energies)
    y : array_like
        y coordinates (intensities)
    yp : array_like
        First derivative of y
    vi : float
        Imaginary potential parameter
    persh : float, optional
        Shift parameter to avoid division by zero, by default 0.05

    Returns
    -------
    ndarray
        Y-function values
    """
    # Calculate average peak height
    eeave = peak_average(x, y, yp)
    
    # Add small shift to avoid division by zero
    af = y + persh * eeave
    apf = yp
    
    # Calculate logarithmic derivative
    ll = apf / af
    
    # Transform to Y-function
    y = ll / (1.0 + vi**2 * ll**2)
    return y

def varsum(xs):
    """Calculate sum with trapezoidal rule.

    Integrates array values using trapezoidal rule, giving half weight to
    endpoints.

    Parameters
    ----------
    xs : array_like
        Values to sum

    Returns
    -------
    float
        Trapezoidal sum
    """
    return np.sum(xs) - 0.5 * (xs[0] + xs[-1])

class RFactor:
    """Class for calculating various R-factors between experimental and theoretical I-V curves.

    This class implements multiple R-factor metrics used in LEED analysis:
    - r1, r2: Compare intensities
    - rp1, rp2: Compare first derivatives
    - rpp1, rpp2: Compare second derivatives  
    - rrzj, rmzj: Zanazzi-Jona R-factors
    - rpe: Pendry R-factor

    Attributes
    ----------
    modes : str or dict
        R-factor calculation modes. Can be single string or dict with weights.
    persh : float
        Shift parameter for Y-function calculation
    vi : float or None
        Imaginary potential for Pendry R-factor
    smoothing : float
        Smoothing factor for B-spline interpolation
    rescale : bool
        Whether to rescale theoretical intensities to match experimental ones
    """
    def __init__(self, modes="rpe", *, persh=0.05, vi=None, smoothing_factor=0.0, rescale=False):
        self.modes = modes
        self.persh = persh
        self.vi = vi  # imaginary part of inner potential.
        self.smoothing = smoothing_factor
        self.rescale = rescale

        if not (isinstance(modes, str) or isinstance(modes, dict)):
            raise ValueError("unsupported mode type {}".format(type(modes)))

    def evaluate(self, ee, ex, th):
        """Evaluate R-factor between experimental and theoretical curves.

        Main entry point for R-factor calculation. Handles both single mode
        and weighted combinations of multiple modes.

        Parameters
        ----------
        ee : array_like
            Energy values
        ex : array_like
            Experimental intensities
        th : array_like
            Theoretical intensities

        Returns
        -------
        float
            R-factor value
        """
        if isinstance(self.modes, str):
            return self._calc([self.modes], ee, ex, th)[0]

        elif isinstance(self.modes, dict):
            modes = self.modes.keys()
            results = self._calc(modes, ee, ex, th)
            # Calculate weighted average of R-factors
            r = 0.0
            w = 0.0
            for mode, value in zip(modes, results):
                r += self.modes[mode] * value
                w += self.modes[mode]
            return r / w

        else:
            return float("inf")

    def _calc(self, modes, ee, ex, th, output=None):
        """Internal method to calculate R-factors.

        Handles the actual computation of R-factors after preprocessing the
        input data (calculating derivatives, smoothing if requested).

        Parameters
        ----------
        modes : list
            List of R-factor modes to calculate
        ee : array_like
            Energy values
        ex : array_like
            Experimental intensities
        th : array_like
            Theoretical intensities
        output : str, optional
            Output file path for debug info

        Returns
        -------
        list
            List of calculated R-factor values
        """
        # Calculate derivatives using selected method
        if self.smoothing == 0.0:
            # Use cubic spline without smoothing
            exp, expp = calc_deriv_cubic_spline(ee, ex)
            thp, thpp = calc_deriv_cubic_spline(ee, th)
        else:
            # Use B-spline with smoothing
            ex, exp, expp = calc_deriv_bspline(ee, ex, self.smoothing)
            th, thp, thpp = calc_deriv_bspline(ee, th, self.smoothing)

        # Calculate Pendry Y-functions if needed
        if "rpe" in modes:
            assert self.vi is not None, "vi not set"
            ye = calc_yfunc(ee, ex, exp, vi=self.vi, persh=self.persh)
            yt = calc_yfunc(ee, th, thp, vi=self.vi, persh=self.persh)
        else:
            ye = np.zeros(len(ee), dtype=ex.dtype)
            yt = np.zeros(len(ee), dtype=th.dtype)

        # Write debug output if requested
        if output:
            with open(output, "w") as fp:
                for i in range(len(ee)):
                    fp.write("{:8.2f} {:20.12e} {:20.12e} {:20.12e} {:20.12e} {:20.12e} {:20.12e} {:20.12e} {:20.12e}\n".format(
                        ee[i],
                        ex[i], exp[i], expp[i], ye[i],
                        th[i], thp[i], thpp[i], yt[i]))
            return []

        # Calculate scaling factor if requested
        if self.rescale == True:
            print("DEBUG: rescale enabled")
            c = varsum(ex) / varsum(th)
        else:
            c = 1.0

        results = []

        # Calculate requested R-factors
        for mode in modes:
            if mode == "r1":
                # Mean absolute deviation of intensities
                r = varsum(np.abs(ex - c * th)) / varsum(ex)
            elif mode == "r2":
                # Mean squared deviation of intensities
                r = varsum((ex - c * th)**2) / varsum(ex**2)
            elif mode == "rp1":
                # Mean absolute deviation of first derivatives
                r = varsum(np.abs(exp - c * thp)) / varsum(np.abs(exp))
            elif mode == "rp2":
                # Mean squared deviation of first derivatives
                r = varsum((exp - c * thp)**2) / varsum(exp**2)
            elif mode == "rpp1":
                # Mean absolute deviation of second derivatives
                r = varsum(np.abs(expp - c * thpp)) / varsum(np.abs(expp))
            elif mode == "rpp2":
                # Mean squared deviation of second derivatives
                r = varsum((expp - c * thpp)**2) / varsum(expp**2)
            elif mode == "rrzj":
                # Zanazzi-Jona R-factor (original)
                eps = np.max(np.abs(exp))
                r = varsum(
                    np.abs(expp - c * thpp) * np.abs(exp - c * thp) / (np.abs(exp) + eps)
                ) / varsum(ex) / 0.027
            elif mode == "rmzj":
                # Zanazzi-Jona R-factor (modified)
                cepst = np.max(np.abs(thp)) * c
                r = varsum(
                    np.abs(expp-c*thpp) * np.abs(exp-c*thp) / (np.abs(exp) + cepst)
                ) / varsum(np.abs(expp))
            elif mode == "rpe":
                # Pendry R-factor
                r = varsum((ye - yt)**2) / varsum(ye**2 + yt**2)
            else:
                raise ValueError("unknown mode \"{}\"".format(mode))
            results.append(r)

            #print("DEBUG: RFactor._calc: mode=\"{}\", r={}".format(mode, r))

        return results
