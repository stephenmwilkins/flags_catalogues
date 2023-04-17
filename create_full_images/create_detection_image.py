

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmasher as cmr
import h5py
from astropy.io import fits
import matplotlib.patheffects as pe
from matplotlib.collections import EllipseCollection


def create_detection_image(survey, img_version, pointing, cat_version = None, add_sources=False, survey_dir = ''):
    '''Create detection image with colour maps differntiating background and potential sources.
        Circle and indicate photometric redshift of sources using add_sources.'''

    survey = survey.upper()

    # Should the same catalogue and image versions be used?
    if cat_version == None:
        cat_version = img_version

    # Load the detection image.
    image_filename = f'{survey_dir}/images/{img_version}/detect{pointing}_277-356_sci.fits'
    hdu = fits.open(image_filename)
    image = hdu[0].data 

    # Define threshold for switching between the two colour maps.
    threshold = -np.percentile(image[image < 0.0], 0.32)

    # Define figure properties.
    dpi = 1000
    figsize = np.array(image.shape)[::-1]/dpi
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes((0.0, 0.0, 1., 1.))

    norm = mpl.colors.Normalize(vmin=0., vmax=10.)
    cmap = cmr.get_sub_cmap('cmr.ember', 0.15, 1.00)
    zcmap = cmr.get_sub_cmap('cmr.pride', 0.00, 1.00)

    # Use grey colur map for background pixels. 
    ax.imshow(image, cmap='Greys', vmin=-threshold*2, vmax=threshold*2, origin='lower')
    # Second colourmap for sources.
    ax.imshow(np.ma.masked_where(image <= threshold, image),
              cmap=cmap, vmin=threshold, vmax=100*threshold, origin='lower')

    # Plot circles around the sources if required.
    if add_sources:

        # Load catalogue file.
        cat_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}.h5'

        with h5py.File(cat_filename, 'r') as hf:

            z = hf[f'pz/{survey.lower()}/ZA'][:]
            photom = hf['photom']
            x = photom['X'][:]
            y = photom['Y'][:]
            # a = photom['A_IMAGE'][:]
            # b = photom['B_IMAGE'][:]
            # theta = photom['THETA_IMAGE'][:]
            # radius = photom['KRON_RADIUS'][:]
            #area = photom['ISOAREA_IMAGE'][:]
            size = [5]*len(z)

        '''
        # Size of marker is dependent on image size.
        minsize = 2.
        size = np.sqrt(area)
        size[size < minsize] = minsize
        size[~np.isfinite(size)] = minsize
        '''

        # Plot circles and colour by redshift.
        zcolor = zcmap(norm(z))
        ax.scatter(x, y, size, facecolors='none', marker='o',
                   edgecolors=zcolor, linewidth=0.3, alpha=0.7)

        # X, Y = np.meshgrid(x, y)
        # XY = np.column_stack((X.ravel(), Y.ravel()))
        # ec = EllipseCollection(a, b, theta, units='x', offsets=XY)
        # ec.set_array((X + Y).ravel())
        # ax.add_collection(ec)

        # Add redshift labels
        for i in range(len(size)):
            ax.text(x[i] + 10, y[i], f'{z[i]:.2f}', color=zcolor[i], fontsize=1,
                    ha='left', va='center', path_effects=[pe.withStroke(linewidth=0.2, foreground='white')])

    ax.set_axis_off()

    if add_sources:
        fig.savefig(
            f'{survey_dir}/myimages/{survey}_nircam{pointing}_v{img_version}_detect_with-sources.png')
    if not add_sources:
        fig.savefig(f'{survey_dir}/myimages/{survey}_nircam{pointing}_v{img_version}_detect.png')