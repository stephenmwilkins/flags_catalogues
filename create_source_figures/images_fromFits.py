

from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

from synthesizer.filters import SVOFilterCollection
import pysep.sep as sep
import pysep.utils
import pysep.plots.image
import pysep.analyse




def create_multiband_image(hf, imgs, filters, output_dir = None, size = 50, N = None):

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



if __name__ == '__main__':


    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'  # this should be replaced by an environment variable or similar

    pointings = [1]
    versions = ['0.2']
    N = 10 # testing purposes

    filters = []
    # filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
    # filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]

    filters_ = [f.split('.')[-1].lower() for f in filters]

    for pointing in pointings:

        for version in versions:


            # --- create the Image object. The Image object contains the science and weight arrays and can be easily masked
            imgs = {f: pysep.utils.ImageFromMultiFITS(f'{ceers_dir}/images/ceers_nircam{pointing}_{f}_v{version}_i2d.fits') for f in filters_}
            # img.measure_background_map()

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            cat_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

            with h5py.File(cat_filename,'r') as hf:


                create_multiband_image(hf, imgs, filters, output_dir = output_dir, N = N)
