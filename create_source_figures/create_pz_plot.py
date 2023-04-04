
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

def create_pz_plot(survey, version, pointing, pz_types = None, subcat = None, N = None):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    if subcat != None:
        output_filename += f'-{subcat}'

    if pz_types == None:
        pz_types = [survey.lower()]

    with h5py.File(output_filename+'.h5','r') as hf:

        # --- select phtometry group
        photom = hf['photom']

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

            for pz_type, ls in zip(pz_types, ['-','-.','--',':']):

                pz = hf[f'pz/{pz_type}']
                ax.plot(pz['ZGRID'][:], pz['PZ'][i], lw=1, c='k', ls=ls)


            ax.set_ylabel(r'$\rm P(z) $')
            ax.set_xlabel(r'$\rm z $')

            fn = f'{output_dir}/pz_{id}.png'
            print(fn)
            fig.savefig(fn)