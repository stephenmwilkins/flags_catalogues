

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
from synthesizer.filters import FilterCollection
import pysep.sep as sep
import pysep.utils
import pysep.plots.image
import pysep.analyse



def create_significance_plots(survey, version, pointing, detection_filter, subcat = None, N = None):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    if subcat != None:
        output_filename += f'-{subcat}'

    detection_filter = detection_filter.lower()

    img = pysep.utils.ImageFromMultiFITS(f'{survey_dir}/images/{survey.lower()}_nircam{pointing}_{detection_filter}_v{version}_i2d.fits')
    img.measure_background_map() # required
    
    with h5py.File(output_filename+'.h5','r') as hf:

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