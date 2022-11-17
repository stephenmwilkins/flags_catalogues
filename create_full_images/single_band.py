

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe


def create_single_band_image(filter, pointing, version):

    norm = mpl.colors.Normalize(vmin=0., vmax=10.)

    filter_ = filter.split('.')[-1].lower()

    image_filename = f'{ceers_dir}/images/{version}/ceers_nircam{pointing}_{filter_}_sci_bkgsub.fits'

    hdu = fits.open(image_filename)
    image = hdu[0].data  # 1 = science,

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

    fig.savefig(f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_{filter_}_v{version}.png')


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointings = [3, 6]
    versions = ['0.2']

    filters = []
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W',
                                             'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W']]

    for filter in filters:

        for pointing in pointings:

            for version in versions:

                print(filter, pointing, version)

                create_single_band_image(filter, pointing, version)
