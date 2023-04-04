
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')



def create_pz_plot(hf, pz_types = ['ceers'], output_dir = None, N = None):

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

if __name__ == '__main__':


    ceers_dir = '/Users/jt458/ceers'  # this should be replaced by an environment variable or similar

    pointings = [1]
    #pointings = np.arange(1,11)
    versions = ['0.51.2']
    N = 10 # testing purposes


    for pointing in pointings:

        for version in versions:

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            output_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

            with h5py.File(output_filename,'r') as hf:

                # create_SED(hf) # all
                create_pz_plot(hf, output_dir = output_dir, N = N)