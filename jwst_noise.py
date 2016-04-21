"""
This file contains functions for rebinning spectra to NIRSpec resolutions
and adding NIRSpec noise realizations.
"""

import utility_functions as uf
import numpy as np
from scipy.interpolate import interp1d


def rebin_spectrum(wavel_in, flux_in, z, resolution=100):
    """
    Rebin a spectrum to NIRSpec resolution

    :param wavel_in: The input wavelengths in A, restframe
    :param flux_in: The input flux in erg/s/A
    :param z: The redshift
    :param resolution: The NIRSpec resolution. Can be
    100 or 1000
    :return: (wavel, flux) tuple with the bin centers in A
    and the flux in each bin in erg/s/A
    """
    wavel_bins_out = uf.nirspec_bins(z=z, resolution=resolution)
    wavel_out = (wavel_bins_out[1:] + wavel_bins_out[:-1]) / 2.
    flux_out = np.zeros_like(wavel_out)
    idx = np.digitize(wavel_in, wavel_bins_out)
    for i in range(len(wavel_out)):
        flux_out[i] = np.mean(flux_in[idx == (i + 1)])
    # If parts of the input are lower res than the output,
    # there will be NaNs. Use interpolation to deal with that
    f = interp1d(wavel_in, flux_in)
    nan_idx = flux_out != flux_out
    flux_out[nan_idx] = f(wavel_out[nan_idx])
    return wavel_out, flux_out


def get_noise_realization_fixed_sn(wavel, flux, S_N_target, z=7.,
                                   resolution=100.):
    pass


def get_noise_realization_fixed_t(wavel, flux, t, z=7.,
                                  resolution=100):
    pass