"""
This file contains functions for rebinning spectra to NIRSpec resolutions
and adding NIRSpec noise realizations.
"""

import utility_functions as uf
import numpy as np
from scipy.interpolate import interp1d
import os


def rebin_spectrum(wavel_in, flux_in, resolution=100):
    pass


def get_noise_realization_fixed_sn(wavel, flux, S_N_target, z=7.,
                                   resolution=100.):
    pass


def get_noise_realization_fixed_t(wavel, flux, t, z=7.,
                                  resolution=100):
    pass


def nirspec_sensitivity(wavel_mu, resolution):
    """
    Get the minimum flux observable at S/N=10 for the
    given resolution for exposure time t=10^4 s with NIRSpec

    :param wavel_mu: The observer frame wavelength in mu
    :param resolution: The NIRSpec resolution (100 or 1000)
    :return: The minimum flux in nJy
    """
    if resolution == 100:
        nirspec_data = np.loadtxt(uf.resource_filename('nirspec_sensitivity_R100.dat'))
    elif resolution == 1000:
        nirspec_data = np.loadtxt(uf.resource_filename('nirspec_sensitivity_R1000.dat'))
    else:
        raise ValueError('Unsupported resolution')

    wavel_nirspec = nirspec_data[:, 0]
    flux_nirspec = nirspec_data[:, 2]
    f = interp1d(wavel_nirspec, flux_nirspec)
    return f(wavel_mu)


def signal_to_noise(wavel, flux, t, z=7., resolution=100):
    pass
