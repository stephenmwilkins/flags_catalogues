
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

def create_pz_plot(survey, cat_version, pointing, pz_types = None, subcat = None, survey_dir = '', N = None):

    survey = survey.upper()

    # Save the images here.
    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Catalogue to use.
    cat_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    if subcat != None:
        cat_filename += f'-{subcat}'

    # The P(z) estimates to be used. If none given use the default survey values.
    if pz_types == None:
        pz_types = [survey.lower()]

    with h5py.File(cat_filename+'.h5','r') as hf:

        # Select phtometry group
        photom = hf['photom']

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

            # Plot the full P(z) for each of the different estimates.
            for pz_type, ls in zip(pz_types, ['-','-.','--',':']):

                pz = hf[f'pz/{pz_type}']
                ax.plot(pz['ZGRID'][:], pz['PZ'][i], lw=1, c='k', ls=ls)


            ax.set_ylabel(r'$\rm P(z) $')
            ax.set_xlabel(r'$\rm z $')

            fn = f'{output_dir}/pz_{id}.png'
            fig.savefig(fn)
            plt.close()