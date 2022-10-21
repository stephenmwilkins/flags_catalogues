
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

from synthesizer.filters import SVOFilterCollection





def create_sed_plot(hf, output_dir = None, filters = None, N = None):

    # --- select phtometry group
    photom = hf['photom']

    # if not filters:
        # --- figure out a way to automaticall get the filters. This may require using an attribute in the HDF5 file

    fc = SVOFilterCollection(filters)

    filters_ = [f.split('.')[-1][:-1] for f in filters] # conversion from SVO (our) filter names to CEERS convention
    wavelengths = np.array([fc.filter[f].pivwv()/1E4 for f in filters])

    if N:
        ids = photom['ID'][:N] # useful for testing
    else:
        ids = photom['ID'][:]


    for i, id in enumerate(ids):

        fig = plt.figure(figsize = (3.5, 2.5))

        left  = 0.2
        width = 0.75
        height = 0.6
        bottom = 0.25

        ax = fig.add_axes((left, bottom, width, height))

        fluxes = np.array([photom[f][i] for f in filters_])
        flux_errors = np.array([photom['D'+f][i] for f in filters_])

        ax.errorbar(wavelengths, fluxes, yerr =flux_errors, fmt = 'o', c = 'k', ms = 2, lw=1)

        ax.set_ylim([0., 1.2*np.max(fluxes[np.isfinite(fluxes)])])
        ax.set_xlim([0.4, 4.7])
        ax.set_ylabel(r'$\rm f_{\nu}/nJy $')
        ax.set_xlabel(r'$\rm \lambda/\mu m$')

        fn = f'{output_dir}/sed_{id}.png'
        print(fn)
        fig.savefig(fn)



if __name__ == '__main__':


    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'  # this should be replaced by an environment variable or similar

    pointings = [1,2,3,6]
    pointings = [1]
    versions = ['0.2']
    N = 10 # testing purposes

    filters = []
    filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
    filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]

    for pointing in pointings:

        for version in versions:

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            output_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

            with h5py.File(output_filename,'r') as hf:

                # create_SED(hf) # all
                create_sed_plot(hf, output_dir = output_dir, filters = filters, N = N)
