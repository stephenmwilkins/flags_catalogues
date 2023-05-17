

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe
from matplotlib.collections import EllipseCollection


def create_detection_image(pointing, img_version, cat_version = None, add_sources=False):

    if cat_version == None:
        cat_version = img_version

    norm = mpl.colors.Normalize(vmin=0., vmax=10.)

    image_filename = f'{ceers_dir}/images/detect{pointing}_277-356_sci_v{img_version}.fits'
    #image_filename = f'{ceers_dir}/images/{version}/ceers_nircam{pointing}_detect_277-356_sci.fits'

    hdu = fits.open(image_filename)

    image = hdu[0].data  # 0 = science,

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

    if add_sources:

        cat_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{cat_version}.h5'

        with h5py.File(cat_filename, 'r') as hf:

            z = hf['pz/ceers/ZA'][:]
            photom = hf['photom']
            x = photom['X'][:]
            y = photom['Y'][:]
            # a = photom['A_IMAGE'][:]
            # b = photom['B_IMAGE'][:]
            # theta = photom['THETA_IMAGE'][:]
            # radius = photom['KRON_RADIUS'][:]
            #area = photom['ISOAREA_IMAGE'][:]
            size = [5]*len(z)

        #print(np.min(area), np.max(area))
        
        '''
        minsize = 2.
        size = np.sqrt(area)
        size[size < minsize] = minsize
        size[~np.isfinite(size)] = minsize
        '''
        zcolor = zcmap(norm(z))

        ax.scatter(x, y, size, facecolors='none', marker='o',
                   edgecolors=zcolor, linewidth=0.3, alpha=0.7)  # plot markers

        # X, Y = np.meshgrid(x, y)
        # XY = np.column_stack((X.ravel(), Y.ravel()))
        # ec = EllipseCollection(a, b, theta, units='x', offsets=XY)
        # ec.set_array((X + Y).ravel())
        # ax.add_collection(ec)

        # --- add redshift labels
        for i in range(len(size)):
            ax.text(x[i] + 10, y[i], f'{z[i]:.2f}', color=zcolor[i], fontsize=1,
                    ha='left', va='center', path_effects=[pe.withStroke(linewidth=0.2, foreground='white')])

    ax.set_axis_off()

    if add_sources:

        fig.savefig(
            f'{ceers_dir}/myimages/ceers_nircam{pointing}_detect_with-sources_v{img_version}.png')

    if not add_sources:

        fig.savefig(f'{ceers_dir}/myimages/ceers_nircam{pointing}_detect_v{img_version}.png')


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/jt458/ceers'

    pointings = [4]
    versions = ['0.51.2']

    for pointing in pointings:
        for version in versions:
            create_detection_image(pointing, version, add_sources=True)
