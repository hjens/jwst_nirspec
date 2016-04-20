"""
This file contains functions for rebinning spectra to NIRSpec resolutions
and adding NIRSpec noise realizations.
"""

import utility_functions as uf
import numpy as np
import os


def rebin_spectrum(wavel_in, flux_in, resolution=100):
    pass


def get_noise_realization_fixed_sn(wavel, flux, S_N_target, z=7.,
                                   resolution=100.):
    pass


def get_noise_realization_fixed_t(wavel, flux, t, z=7.,
                                  resolution=100):
    pass