"""
This file contains utility functions used by jwst_noise.
These functions are not meant to be used on their own.
"""
import os

# This directory contains the sensitivity for NIRSpec, downloaded from
# http://www.stsci.edu/jwst/instruments/nirspec/sensitivity/
ETC_DIR = 'NIRSpec_ETC/'

def flux_wavel_to_obs_frame(wavel, flux, z=7.):
    pass


def flux_to_njy(wavel, flux, z=7.):
    pass


def nirspec_bins(z=None, wavel_range=None, resolution=100):
    pass


def resource_filename(filename):
    """
    Get the full path to a resource file

    :param filename: The file name of the resource
    :return: The full path to the file
    """
    package_dir = os.path.dirname(__file__)
    fullpath = os.path.join(package_dir, ETC_DIR, filename)
    return fullpath