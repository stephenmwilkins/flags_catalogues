

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe


def create_single_band_image(survey, version, pointing, filters):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    norm = mpl.colors.Normalize(vmin=0., vmax=10.)

    for filter in filters:
        filter_ = filter.split('.')[-1].lower()

        image_filename = f'{survey_dir}/images/{survey.lower()}_nircam{pointing}_{filter_}_sci_bkgsub_v{version}.fits'

        hdu = fits.open(image_filename)
        image = hdu[0].data 

        threshold = -np.percentile(image[image < 0.0], 0.32)

        dpi = 1000

        figsize = np.array(image.shape)[::-1]/dpi

        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_axes((0.0, 0.0, 1., 1.))

        cmap = cmr.get_sub_cmap('cmr.ember', 0.15, 1.00)
        zcmap = cmr.get_sub_cmap('cmr.pride', 0.00, 1.00)

        ax.imshow(image, cmap='Greys', vmin=-threshold*2, vmax=threshold*2, origin='lower')
        ax.imshow(np.ma.masked_where(image <= threshold, image),
                cmap=cmap, vmin=threshold, vmax=100*threshold, origin='lower')

        ax.set_axis_off()

        fig.savefig(f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_{filter_}_v{version}.png')
