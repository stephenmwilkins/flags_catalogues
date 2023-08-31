

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

def create_multiband_image(survey, img_version, pointing, filters, cat_version = None, subcat = None, size = 50, survey_dir = '', N = None):

    # Should the same catalogue and image versions be used?
    if cat_version == None:
        cat_version = img_version

    survey = survey.upper()

    # Save the images here.
    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Catalogue to use.    
    output_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    if subcat != None:
        output_filename += f'-{subcat}'

    # Get filter names in correct format and load corresponding image.
    filters_ = [f.split('.')[-1].lower() for f in filters]
    imgs = {f: pysep.utils.ImageFromMultiFITS(f'{survey_dir}/images/{survey.lower()}_nircam{pointing}_{f}_v{img_version}_i2d.fits') for f in filters_}

    with h5py.File(output_filename+'.h5','r') as hf:

        # Select phtometry group.
        photom = hf['photom']

        # Useful for testing.
        if N:
            ids = photom['ID'][:N]
        else:
            ids = photom['ID'][:]

        for i, id in enumerate(ids):

            # X and Y position of the source.
            x = photom['X'][i]
            y = photom['Y'][i]

            # Create the set of cutout images using pysep.
            cutouts = [imgs[f].make_cutout(y, x, size).data for f in ['f115w', 'f150w', 'f200w', 'f277w', 'f356w', 'f410m', 'f444w']]
            fig, ax = pysep.plots.image.make_images_plot(cutouts) # --- plot the cutout science image # TODO: add better scaling

            fn = f'{output_dir}/multiband_cutout_{id}.png'
            fig.savefig(fn)
            plt.close(fig)
    for img in list(imgs.values()):
        img.hdu.close()
