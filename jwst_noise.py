"""
This file contains functions for rebinning spectra to NIRSpec resolutions
and adding NIRSpec noise realizations.
"""

import utility_functions as uf
import numpy as np
from scipy.interpolate import interp1d


def rebin_spectrum(wavel, flux, z, resolution=100):
    """
    Rebin a spectrum to NIRSpec resolution

    :param wavel: The input wavelengths in A, restframe
    :param flux: The input flux in erg/s/A
    :param z: The redshift
    :param resolution: The NIRSpec resolution. Can be
    100 or 1000
    :return: (wavel, flux) tuple with the bin centers in A
    and the flux in each bin in erg/s/A
    """
    wavel_range = [wavel.min(), wavel.max()]
    wavel_bins_out = uf.nirspec_bins(z=z, resolution=resolution,
                                     wavel_range=wavel_range)
    wavel_out = (wavel_bins_out[1:] + wavel_bins_out[:-1]) / 2.
    flux_out = np.zeros_like(wavel_out)
    idx = np.digitize(wavel, wavel_bins_out)
    for i in range(len(wavel_out)):
        flux_out[i] = np.mean(flux[idx == (i + 1)])
    # If parts of the input are lower res than the output,
    # there will be NaNs. Use interpolation to deal with that
    f = interp1d(wavel, flux)
    nan_idx = flux_out != flux_out
    flux_out[nan_idx] = f(wavel_out[nan_idx])
    return wavel_out, flux_out


def get_noise_realization_fixed_sn(wavel, flux, S_N_target, z=7.,
                                   resolution=100.):
    pass


def get_noise_realization_fixed_t(wavel, flux, t, z=7.,
                                  resolution=100):
    pass