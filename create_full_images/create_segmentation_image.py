

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe
from matplotlib.collections import EllipseCollection


def create_segmentation_image(survey, img_version, pointing, add_sources=False, survey_dir = ''):
    '''Create a segmentation image'''

    survey = survey.upper()

    # Load image data.
    image_filename = f'{survey_dir}/images/{img_version}/segmap_nrc{pointing}.fits'
    hdu = fits.open(image_filename)
    image = hdu[0].data 

    # Define figure properties.
    dpi = 1000
    figsize = np.array(image.shape)[::-1]/dpi
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes((0.0, 0.0, 1., 1.))

    # Assign colours to sources.
    vals = np.linspace(0, 1, np.max(image))
    np.random.shuffle(vals)
    cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))

    ax.imshow(np.ma.masked_where(image == 0, image), cmap=cmap, origin='lower')

    fig.savefig(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_v{img_version}_segmap.png')

