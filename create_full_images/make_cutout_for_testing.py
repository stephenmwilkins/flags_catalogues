

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointing = 1
    version = '0.2'

    filters = []
    filters += ['f115w', 'f150w', 'f200w', 'f277w', 'f356w', 'f444w']
    # filters = ['f115w']

    for filter in filters:

        print(filter)

        image_filename = f'{ceers_dir}/images/{version}/ceers_nircam{pointing}_{filter}_sci_bkgsub_match.fits'
        hdu = fits.open(image_filename)
        image = hdu[0].data  # 0 = science,

        cutout = image[:1000, :1000]

        # plt.imshow(cutout)
        # plt.show()

        np.save(f'{ceers_dir}/images/{version}/cutout_{filter}.npy', cutout)
