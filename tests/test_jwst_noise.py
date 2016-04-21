import pylab as pl
import numpy as np
import sys
sys.path.append('../..')
import jwst_nirspec as jn
import c2raytools as c2t


def test_nirspec_sensitivity():
    wavel_R100 = np.linspace(0.7, 5, 100) # Wavelength in mu
    wavel_R1000 = np.linspace(1.0, 5.0, 100)
    sens_R100 = jn.nirspec_sensitivity(wavel_R100, resolution=100)
    sens_R1000 = jn.nirspec_sensitivity(wavel_R1000, resolution=1000)
    pl.plot(wavel_R100, sens_R100, label='R=100')
    pl.plot(wavel_R1000, sens_R1000, label='R=1000')
    pl.xlabel('Wavelength (um)')
    pl.ylabel('Sensitivity (nJy)')
    pl.legend(loc='best')
    pl.title('Compare to plots at http://www.stsci.edu/jwst/instruments/nirspec/sensitivity/')
    pl.show()


def test_flux_to_njy():
    # According to http://tomdwelly.com/tools_lumtoflux.php
    # 1e40 erg/s/A at 1000 A, z=8 is 0.3995 nJy
    z = 8.
    wavel_obsframe = 1000.
    wavel_restframe = 1000./(1.+z)
    flux_obsframe = 1.e40
    flux_restframe = flux_obsframe*(1.+z)
    wavel_obs, flux_nJy = jn.flux_to_njy(wavel=wavel_restframe,
                                         flux=flux_restframe, z=z)
    print 'test_flux_to_njy'
    print 'flux:', flux_nJy, ' nJy'
    print 'should be around 0.3995'
    print 'Luminosity distance:', c2t.luminosity_distance(z)


def test_nirspec_bins():
    # Test that the resolution as a function of wavelength
    # is the same as in the data files
    for resolution in [100, 1000]:
        pl.figure()
        bins = jn.nirspec_bins(resolution=resolution)
        dlambda = bins[1:]-bins[:-1]
        bin_centers = bins[1:] + dlambda/2.
        R = bin_centers/dlambda

        nirspec_data = jn.utility_functions._get_nirspec_data(resolution=resolution)
        wavel_nirspec = nirspec_data[:, 0]
        specres_nirspec = nirspec_data[:, 1]

        pl.plot(bin_centers, R, label='Calculated')
        pl.plot(wavel_nirspec*1e4, specres_nirspec, label='From file')
        pl.xlabel('Wavelength')
        pl.ylabel('Calculated R')
        pl.legend(loc='best')
        pl.title('test nirspec_bins, R=%d. Curves should be similar' % resolution)
    pl.show()


def test_signal_to_noise():
    # Find flux that gives the same flux density at some wavelength
    # Make sure S/N is approx 10
    # 100 nJy at 2 um, t=1e4
    # 3.6e40 erg/s/A
    z = 7
    t = 1e4
    wavel_restframe = 2.*1.e4/(1+z)
    flux = 3.6e40
    SN = jn.signal_to_noise(wavel_restframe, flux, t, z)
    print 'test signal_to_noise'
    print 'Flux :', jn.flux_to_njy(wavel_restframe, flux, z)[1], ' nJy'
    print 'Signal to noise:', SN
    print 'Should be on the order of 10'


def test_rebin_spectrum():
    sample_spectrum = np.loadtxt('sample_spectrum.dat', skiprows=1)
    wavel = sample_spectrum[:,0]
    flux = sample_spectrum[:,1]
    # Rebin
    wavel_R100, flux_R100 = jn.rebin_spectrum(wavel, flux, z=7,
                                              resolution=100)
    wavel_R1000, flux_R1000 = jn.rebin_spectrum(wavel, flux, z=7,
                                                resolution=1000)
    pl.plot(wavel, flux, label='Raw spectrum')
    pl.plot(wavel_R1000, flux_R1000, label='R=1000')
    pl.plot(wavel_R100, flux_R100, label='R=100', linewidth=2.)
    pl.xlabel('Wavel (A)')
    pl.ylabel('Flux')
    pl.title('test rebin_spectrum')
    pl.legend(loc='best')
    pl.show()


def test_noise_realization_fixed_t():
    # Generate a sine wave signal to use as a spectrum
    sample_spectrum = np.loadtxt('sample_spectrum.dat', skiprows=1)
    wavel = sample_spectrum[:,0]
    flux = sample_spectrum[:,1]
    t = 5.*3600. # 5 hours
    wavel, flux = jn.rebin_spectrum(wavel, flux, z=7, resolution=100)
    noise = jn.noise_realization_fixed_t(wavel, flux, t)
    pl.plot(wavel, flux, label='noise free')
    pl.plot(wavel, flux+noise, label='noisy')
    pl.legend(loc='best')
    pl.title('Test fixed exposure time')
    pl.show()


def test_noise_realization_fixed_sn():
    # Generate a sine wave signal to use as a spectrum
    sample_spectrum = np.loadtxt('sample_spectrum.dat', skiprows=1)
    wavel = sample_spectrum[:,0]
    flux = sample_spectrum[:,1]
    sn = 5
    wavel, flux = jn.rebin_spectrum(wavel, flux, z=7, resolution=100)
    noise = jn.noise_realization_fixed_sn(wavel, flux,
                                          signal_to_noise=sn, z=7,
                                          resolution=100)
    pl.plot(wavel, flux, label='noise free')
    pl.plot(wavel, flux+noise, label='noisy')
    pl.legend(loc='best')
    pl.title('Test fixed S/N=%d' % sn)
    pl.show()


if __name__ == '__main__':
    test_nirspec_sensitivity()
    test_flux_to_njy()
    test_nirspec_bins()
    test_signal_to_noise()
    test_rebin_spectrum()
    test_noise_realization_fixed_t()
    test_noise_realization_fixed_sn()