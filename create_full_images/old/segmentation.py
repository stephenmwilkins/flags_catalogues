

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe
from matplotlib.collections import EllipseCollection


def create_segmentation_image(pointing, version, add_sources=False):

    # norm = mpl.colors.Normalize(vmin=0., vmax=10.)

    image_filename = f'{ceers_dir}/images/ceers_nircam{pointing}_segmap_v{version}.fits'

    hdu = fits.open(image_filename)

    image = hdu[0].data  # 0 = science,

    dpi = 1000

    figsize = np.array(image.shape)[::-1]/dpi

    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes((0.0, 0.0, 1., 1.))

    # cmap = cmr.get_sub_cmap('cmr.ember', 0.15, 1.00)
    # zcmap = cmr.get_sub_cmap('cmr.pride', 0.00, 1.00)

    vals = np.linspace(0, 1, np.max(image))
    np.random.shuffle(vals)
    cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))

    ax.imshow(np.ma.masked_where(image == 0, image), cmap=cmap, origin='lower')

    fig.savefig(
        f'{ceers_dir}/myimages/ceers_nircam{pointing}_segmap_v{version}.png')


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/jt458/ceers'

    pointings = [4]
    versions = ['0.51.2']

    for pointing in pointings:
        for version in versions:
            create_segmentation_image(pointing, version, add_sources=True)
