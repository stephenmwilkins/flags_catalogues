

from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

from synthesizer.filters import FilterCollection
import pysep.sep as sep
import pysep.utils
import pysep.plots.image
import pysep.analyse

def create_multiband_image(survey, version, pointing, filters, subcat = None, size = 50, N = None):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    if subcat != None:
        output_filename += f'-{subcat}'

    filters_ = [f.split('.')[-1].lower() for f in filters]
    imgs = {f: pysep.utils.ImageFromMultiFITS(f'{survey_dir}/images/{survey.lower()}_nircam{pointing}_{f}_v{version}_i2d.fits') for f in filters_}

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

            # --- make a new image from a cutout of another image

            cutouts = [imgs[f].make_cutout(y, x, size).data for f in ['f115w', 'f150w', 'f200w', 'f277w', 'f356w', 'f410m', 'f444w']]
            fig, ax = pysep.plots.image.make_images_plot(cutouts) # --- plot the cutout science image # TODO: add better scaling

            fn = f'{output_dir}/cutout_{id}.png'
            print(fn)
            fig.savefig(fn)

#filters = []
# filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
# filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
#filters += [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]
