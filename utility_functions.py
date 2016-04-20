"""
This file contains utility functions used by jwst_noise.
Some of them can also be useful on their own

"""
import os
import numpy as np
from scipy.interpolate import interp1d
import c2raytools as c2t

# This directory contains the sensitivity for NIRSpec, downloaded from
# http://www.stsci.edu/jwst/instruments/nirspec/sensitivity/
ETC_DIR = 'NIRSpec_ETC/'


def flux_wavel_to_obs_frame(wavel, flux, z=7.):
    """
    Convert the flux and wavelength to observer
    frame

    :param wavel: Rest frame wavelength
    :param flux: Rest frame flux
    :param z: Redshift
    :return: (wavel, flux) tuple. The wavelength and
    flux in the observer frame
    """
    wavel_obs = wavel * (1. + z)
    flux_obs = flux / (1. + z)
    return wavel_obs, flux_obs


def flux_to_njy(wavel, flux, z=7.):
    """
    Convert flux in the rest frame to  nJy
    and the wavelength to observer frame

    :param wavel: The rest frame wavelength in A
    :param flux: The rest frame flux in erg/s/A
    :param z: Redshift
    :return: (wavel, flux) tuple. The wavelength and
    flux in in obs frame A and nJy respectively
    """
    # Scale to observer frame
    wavel_obs, flux_obs = flux_wavel_to_obs_frame(wavel, flux, z)
    # erg/s/A -> erg/s/A/cm^2
    D_L = c2t.luminosity_distance(z)
    cm_per_Mpc = 3.08e24
    D_L_cm = D_L*cm_per_Mpc
    flux_obs_lam = flux_obs/(4.*np.pi*D_L_cm**2)
    # erg/s/A/cm^2 -> Jy
    wavel_obs_um = wavel_obs*1e-4
    flux_nJy = 1e9*(wavel_obs_um)**2*flux_obs_lam/3e-13

    return wavel_obs, flux_nJy


def nirspec_bins(z=None, wavel_range=None, resolution=100):
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
        nirspec_data = np.loadtxt(_resource_filename('nirspec_sensitivity_R100.dat'))
    elif resolution == 1000:
        nirspec_data = np.loadtxt(_resource_filename('nirspec_sensitivity_R1000.dat'))
    else:
        raise ValueError('Unsupported resolution')

    wavel_nirspec = nirspec_data[:, 0]
    flux_nirspec = nirspec_data[:, 2]
    f = interp1d(wavel_nirspec, flux_nirspec)
    return f(wavel_mu)


def signal_to_noise(wavel, flux, t, z=7., resolution=100):
    pass


def _resource_filename(filename):
    """
    Get the full path to a resource file.
    For internal use only.

    :param filename: The file name of the resource
    :return: The full path to the file
    """
    package_dir = os.path.dirname(__file__)
    fullpath = os.path.join(package_dir, ETC_DIR, filename)
    return fullpath