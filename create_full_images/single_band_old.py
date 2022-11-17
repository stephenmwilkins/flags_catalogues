

import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from astropy.io import fits

# from astropy.visualization import make_lupton_rgb, SqrtStretch, LogStretch, hist, simple_norm

from astropy.visualization import (MinMaxInterval, SqrtStretch, LogStretch,
                                   ImageNormalize, ManualInterval, PercentileInterval, ZScaleInterval)


def create_single_band_image(filter, pointing, version):

    image_filename = f'{ceers_dir}/images/ceers_nircam{pointing}_{f}_v{version}_i2d.fits'

    hdu = fits.open(image_filename)
    image = hdu[1].data  # 1 = science,

    # image[image == 0.0] = None

    print(image.shape)

    print(np.std(image[image < 0.0]))
    print(np.std(image[image > 0.0]))

    threshold = -np.percentile(image[image < 0.0], 0.32)
    print(threshold)

    dpi = 1000

    figsize = np.array(image.shape)[::-1]/dpi
    print(figsize)

    # # interval = ZScaleInterval(contrast=0.9)
    # interval = PercentileInterval(0.999)
    # stretch = SqrtStretch()
    #
    # norm = ImageNormalize(image, interval=interval,
    #                       stretch=stretch)
    #
    # print(norm)

    # or equivalently using positional arguments
    # norm = ImageNormalize(image, MinMaxInterval(), SqrtStretch())

    # Display the image
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes((0.0, 0.0, 1., 1.))

    # im = ax.imshow(image, origin='lower', norm=norm, cmap='Greys_r')

    cmap = cmr.get_sub_cmap('cmr.ember', 0.15, 1.00)

    ax.imshow(image, cmap='Greys', vmin=-threshold*2, vmax=threshold*2, origin='lower')
    ax.imshow(np.ma.masked_where(image <= threshold, image),
              cmap=cmap, vmin=threshold, vmax=100*threshold, origin='lower')

    ax.set_axis_off()
    fig.savefig(f'{ceers_dir}/myimages/ceers_nircam{pointing}_{f}_v{version}.png')


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointings = [1]
    versions = ['0.2']

    filters = []
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W',
                                             'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W']]

    filters_ = [f.split('.')[-1].lower() for f in filters]

    filters_ = ['f200w']

    for filter in filters_:

        for pointing in pointings:

            for version in versions:
