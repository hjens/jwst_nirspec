"""
This file contains functions for rebinning spectra to NIRSpec resolutions
and adding NIRSpec noise realizations.
"""

import utility_functions as uf
import numpy as np
from scipy.interpolate import interp1d

def rebin_spectrum(wavel_in, flux_in, resolution=100):
    pass


def get_noise_realization_fixed_sn(wavel, flux, S_N_target, z=7.,
                                   resolution=100.):
    pass


def get_noise_realization_fixed_t(wavel, flux, t, z=7.,
                                  resolution=100):
    pass


def nirspec_sensitvity(wavel_mu, resolution):
    pass


def signal_to_noise(wavel, flux, t, z=7., resolution=100):
    pass