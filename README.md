# Package overview
`jwst_nirspec` is a small collection of functions to transform simulated
galaxy spectra into mock JWST/NIRSpec observations. You can use it to
rebin spectra to NIRSpec's resolution and simulation observational noise.

# Installation
Download the package and put it in your Python path. Make sure
you can install it:

    import jwst_nirspec

You need to have `numpy` and `scipy` installed. For the example you also
 need `matplotlib`.

# Usage
The functions in the file `jwst_noise.py` are used for rebinning and
simulating noise. They should be understandable from their docstrings.

You can also look at the file `example.py` to see how to rebin a
spectrum and add noise.