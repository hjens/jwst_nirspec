import pylab as pl
import numpy as np
import sys
sys.path.append('../..')
import jwst_nirspec as jn

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


if __name__ == '__main__':
    test_nirspec_sensitivity()