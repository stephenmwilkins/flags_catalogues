

from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

import pandas as pd
from astropy.table import Table
from astropy.io import ascii, fits
from synthesizer.filters import SVOFilterCollection
import pysep.sep as sep
import pysep.utils
import pysep.plots.image
import pysep.analyse



def create_significant_plots(hf, img, output_dir = None, N = None):

    # --- select phtometry group
    photom = hf['photom']

    if N:
        ids = photom['ID'][:N] # useful for testing
    else:
        ids = photom['ID'][:]

    for i, id in enumerate(ids):

        x = photom['X'][i]
        y = photom['Y'][i]

        cutout = img.make_cutout(y, x, 50)

        fig, ax = pysep.plots.image.make_significance_plot(cutout)

        fn = f'{output_dir}/significance_{id}.png'
        print(fn)
        fig.savefig(fn)


        cutout = img.make_cutout(y, x, 200)

        fig, ax = pysep.plots.image.make_significance_plot(cutout)

        fn = f'{output_dir}/wide_significance_{id}.png'
        print(fn)
        fig.savefig(fn)



if __name__ == '__main__':


    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'  # this should be replaced by an environment variable or similar

    pointings = [1]
    versions = ['0.2']
    N = 10 # testing purposes

    detection_filter = 'f200w' # should replace by a stacked detection image


    for pointing in pointings:

        for version in versions:

            detection_image = pysep.utils.ImageFromMultiFITS(f'{ceers_dir}/images/ceers_nircam{pointing}_{detection_filter}_v{version}_i2d.fits')
            detection_image.measure_background_map() # required

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            cat_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

            with h5py.File(cat_filename,'r') as hf:

                create_significant_plots(hf, detection_image, output_dir = output_dir, N = N)
