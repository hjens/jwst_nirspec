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
    print 'flux:', flux_nJy, ' nJy'
    print 'should be around 0.3995'
    print 'Luminosity distance:', c2t.luminosity_distance(z)


if __name__ == '__main__':
    #test_nirspec_sensitivity()
    test_flux_to_njy()