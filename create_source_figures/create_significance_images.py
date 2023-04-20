

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



def create_significance_images(survey, img_version, pointing, detection_filter, cat_version = None, subcat = None, survey_dir = '', N = None):

    # Should the same catalogue and image versions be used?
    if cat_version == None:
        cat_version = img_version

    survey = survey.upper()

    # Save the images here.
    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Catalogue to use.
    cat_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    if subcat != None:
        cat_filename += f'-{subcat}'

    # Load the image in the detection band.
    detection_filter = detection_filter.lower()
    img = pysep.utils.ImageFromMultiFITS(f'{survey_dir}/images/{survey.lower()}_nircam{pointing}_{detection_filter}_v{img_version}_i2d.fits')
    
    # Measure background using pysep.
    img.measure_background_map()
    
    with h5py.File(cat_filename+'.h5','r') as hf:

        # Select phtometry group
        photom = hf['photom']

        # Useful for testing.   
        if N:
            ids = photom['ID'][:N]
        else:
            ids = photom['ID'][:]

        for i, id in enumerate(ids):

            # X and Y position of source.
            x = photom['X'][i]
            y = photom['Y'][i]

            # Make narrow and wide significance plots with pysep.
            cutout = img.make_cutout(y, x, 50)

            fig, ax = pysep.plots.image.make_significance_plot(cutout)

            fn = f'{output_dir}/significance_{id}.png'
            fig.savefig(fn)


            cutout = img.make_cutout(y, x, 200)

            fig, ax = pysep.plots.image.make_significance_plot(cutout)

            fn = f'{output_dir}/wide_significance_{id}.png'
            fig.savefig(fn)
            plt.close()