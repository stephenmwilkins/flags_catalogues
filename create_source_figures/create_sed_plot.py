
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

from synthesizer.filters import FilterCollection


def create_sed_plot(survey, cat_version, pointing, filters, subcat = None, survey_dir = '', N = None):

    survey = survey.upper()

    # Save the images here.
    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Catalogue to use.
    cat_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    if subcat != None:
        cat_filename += f'-{subcat}'

    with h5py.File(cat_filename+'.h5','r') as hf:

        # Select phtometry group
        photom = hf['photom']

        fc = FilterCollection(filters, new_lam = np.arange(5000., 55000., 1.))

        # Conversion from synthesizer filter names to survey convention
        filters_ = [f.split('.')[-1][1:-1] for f in filters] 

        # Get pivot wavelengths.
        wavelengths = np.array([fc.filters[f].pivwv()/1E4 for f in filters])

        # Useful for testing.
        if N:
            ids = photom['ID'][:N]
        else:
            ids = photom['ID'][:]


        for i, id in enumerate(ids):

            # Figure properties.
            fig = plt.figure(figsize = (3.5, 2.5))

            left  = 0.2
            width = 0.75
            height = 0.6
            bottom = 0.25

            ax = fig.add_axes((left, bottom, width, height))

            # Get fluxes in each band and corresponding errors.
            fluxes = np.array([photom['FLUX_'+f][i] for f in filters_])
            flux_errors = np.array([photom['FLUXERR_'+f][i] for f in filters_])

            # PLot the SED.
            ax.errorbar(wavelengths, fluxes, yerr =flux_errors, fmt = 'o', c = 'k', ms = 2, lw=1)

            ax.set_ylim([0., 1.2*np.max(fluxes[np.isfinite(fluxes)])])
            ax.set_xlim([0.4, 4.7])
            ax.set_ylabel(r'$\rm f_{\nu}/nJy $')
            ax.set_xlabel(r'$\rm \lambda/\mu m$')

            fn = f'{output_dir}/sed_{id}.png'
            fig.savefig(fn)
            plt.close(fig)