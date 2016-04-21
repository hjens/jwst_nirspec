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


def noise_realization_fixed_sn(wavel, flux, signal_to_noise,
                               z=7., resolution=100.):
    """
    Generate a noise realization for a given S/N ratio,
    rather than a given exposure time. The S/N is
    measured at 1500 A

    :param wavel: The restframe wavelength in A
    :param flux: The flux in erg/s/A
    :param signal_to_noise: The output S/N at 1500 A
    :param z: The redshift
    :param resolution: The NIRSpec resolution
    :return: Array with the noise to be added to
    the spectrum
    """
    s_n_spectrum = uf.signal_to_noise(wavel, flux, 3600., z,
                             resolution)
    idx_1500 = np.argmin(np.abs(wavel-1500.))
    s_n_spectrum *= signal_to_noise / s_n_spectrum[idx_1500]
    noise_sigma = flux/s_n_spectrum
    noise = np.random.normal(loc=0.0, scale=noise_sigma,
                             size=wavel.shape)
    return noise


def noise_realization_fixed_t(wavel, flux, exp_time_seconds, z=7.,
                              resolution=100):
    """
    Generate a realization of Gaussian noise
    for a given spectrum and integration time

    :param wavel: The restframe wavelength in A
    :param flux: The flux in erg/s/A
    :param exp_time_seconds: The exposure time in seconds
    :param z: The redshift
    :param resolution: The NIRSpec resolution. Can
    be 100 or 1000
    :return: Array with the noise to be added to
    the spectrum
    """
    S_N = uf.signal_to_noise(wavel, flux, exp_time_seconds, z,
                             resolution)
    noise_sigma = flux/S_N
    noise = np.random.normal(loc=0.0, scale=noise_sigma,
                             size=wavel.shape)
    return noise
