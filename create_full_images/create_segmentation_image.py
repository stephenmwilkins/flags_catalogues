

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe
from matplotlib.collections import EllipseCollection


def create_segmentation_image(survey, version, pointing, add_sources=False):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    image_filename = f'{survey_dir}/images/{survey}_nircam{pointing}_segmap_v{version}.fits'

    hdu = fits.open(image_filename)

    image = hdu[0].data 

    dpi = 1000

    figsize = np.array(image.shape)[::-1]/dpi

    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes((0.0, 0.0, 1., 1.))

    vals = np.linspace(0, 1, np.max(image))
    np.random.shuffle(vals)
    cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))

    ax.imshow(np.ma.masked_where(image == 0, image), cmap=cmap, origin='lower')

    fig.savefig(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_v{version}_segmap.png')

