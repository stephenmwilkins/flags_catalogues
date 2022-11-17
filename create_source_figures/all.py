

from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import h5py
from PIL import Image

from synthesizer.filters import SVOFilterCollection


from images import create_image, create_multiimage
from pz import create_pz_plot
from sed import create_sed_plot


plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    subcat = '-high-z.v0.1'
    pointings = [2, 3, 6]
    versions = ['0.2']

    filters = []
    filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
    filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W',
                                             'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W']]

    cutout_filters = [f'JWST/NIRCam.{f}' for f in ['F115W',
                                                   'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W']]
    cutout_filters_ = [f.split('.')[-1].lower() for f in cutout_filters]

    for pointing in pointings:

        for version in versions:

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}'

            Path(output_dir).mkdir(parents=True, exist_ok=True)  #  create output directory

            catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}.h5'

            # imgs = {f: Image.open(
            #     f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_{f}_v{version}.png') for f in cutout_filters_}
            #
            # imgs2 = {}
            # imgs2['detection'] = Image.open(
            #     f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_detect_with-sources.png')
            # imgs2['segmentation'] = Image.open(
            #     f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_segmap.png')

            with h5py.File(catalogue_filename, 'r') as hf:

                create_sed_plot(hf, output_dir=output_dir, filters=filters)
                create_pz_plot(hf, output_dir=output_dir)
                # create_multiimage(hf, imgs, cutout_filters_, output_dir=output_dir)
                # create_image(hf, imgs2, output_dir=output_dir)
