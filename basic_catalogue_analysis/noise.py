
#from synthesizer.filters import SVOFilterCollection
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

from synthesizer.utils import flux_to_m, m_to_flux

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/jt458/ceers'

    pointing = 1
    version = '0.51.2'
    filter = '277'

    catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

    with h5py.File(catalogue_filename, 'r') as hf:

        fig = plt.figure(figsize=(3.5, 3.5))

        left = 0.2
        width = 0.75
        height = 0.6
        bottom = 0.25

        ax = fig.add_axes((left, bottom, width, height))

        photom = hf['photom']

        photom.visit(print)

        # if not filters:
        # --- figure out a way to automaticall get the filters. This may require using an attribute in the HDF5 file

        flux = photom[f'FLUX_{filter}_APER'][:]
        flux_err = photom[f'FLUXERR_{filter}_APER'][:]

        flux = photom[f'FLUX_{filter}'][:]
        flux_err = photom[f'FLUXERR_{filter}'][:]

        ax.scatter(np.log10(flux), np.log10(flux_err), s=1, alpha=0.1)

        noise = m_to_flux(28.5)/5.

        ax.axhline(np.log10(noise))

        flux = 10**np.array([-1., 4.])
        flux_err = noise*((flux/5.)/noise)**0.3

        ax.plot(np.log10(flux), np.log10(flux_err))

        ax.set_xlim([0, 4.])
        ax.set_ylim([0, 4.])

        ax.set_xlabel(r'$\rm f_{\nu}/nJy $')
        ax.set_ylabel(r'$\rm \sigma$')

        fn = f'figs/noise.pdf'
        print(fn)
        fig.savefig(fn)