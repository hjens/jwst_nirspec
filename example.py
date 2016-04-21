import numpy as np
import pylab as pl
import sys
sys.path.append('..')
import jwst_noise

# Read a sample galaxy spectrum
sample_spectrum = np.loadtxt('tests/sample_spectrum.dat',
                             skiprows=1)
wavel = sample_spectrum[:,0]
flux = sample_spectrum[:,1]

# Rebin the spectrum to NIRSpec resolution
wavel_R100, flux_R100 = jwst_noise.rebin_spectrum(wavel, flux, z=7,
                                          resolution=100)
wavel_R1000, flux_R1000 = jwst_noise.rebin_spectrum(wavel, flux, z=7,
                                            resolution=1000)

# Generate some noise. This can be done by specifying either a
# fixed exposure time or a fixed S/N level at 1500 A
noise_R100 = jwst_noise.noise_realization_fixed_t(wavel_R100, flux_R100,
                                                  exp_time_seconds=9000,
                                                  z=7, resolution=100)
noise_R1000 = jwst_noise.noise_realization_fixed_sn(wavel_R1000,
                                                    flux_R1000,
                                                    signal_to_noise=5,
                                                    z=7,
                                                    resolution=1000)

# Plot results
pl.subplot(121)
pl.plot(wavel, flux, label='Raw')
pl.plot(wavel_R100, flux_R100, label='R=100')
pl.plot(wavel_R100, flux_R100+noise_R100, label='R=100, 9000 s noise')
pl.xlabel('Wavelength (A)')
pl.ylabel('Flux (erg/s/A)')
pl.legend(loc='best')
pl.subplot(122)
pl.plot(wavel_R1000, flux_R1000, label='R=1000')
pl.plot(wavel_R1000, flux_R1000+noise_R1000, label='R=1000, S/N=5')
pl.xlabel('Wavelength (A)')
pl.ylabel('Flux (erg/s/A)')
pl.legend(loc='best')
pl.show()