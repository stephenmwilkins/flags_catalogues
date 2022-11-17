

from PIL import Image
from synthesizer.filters import SVOFilterCollection
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py


plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')


def create_image(hf, imgs, output_dir=None, size=300, N=None):
    """ create image cutouts from pngs for every image in dictionary individualy """

    # --- select phtometry group
    photom = hf['photom']

    if N:
        ids = photom['ID'][:N]  #  useful for testing
    else:
        ids = photom['ID'][:]

    for i, id in enumerate(ids):

        x = photom['X'][i]
        y = photom['Y'][i]

        # --- make a new image from a cutout of another image

        for img_name, img in imgs.items():

            fig = plt.figure(figsize=(1, 1), dpi=size)
            ax = fig.add_axes((0.0, 0.0, 1., 1.))

            left = int(x-size/2)
            upper = int(img.size[1]-y-size/2)
            right = int(x+size/2)
            lower = int(img.size[1]-y+size/2)
            cutout = img.crop((left, upper, right, lower))
            ax.imshow(cutout)
            ax.set_axis_off()
            fn = f'{output_dir}/{img_name}_{id}.png'
            print(fn)
            fig.savefig(fn)


def create_multiimage(hf, imgs, filters_, output_dir=None, size=50, N=None):
    """ create a single image from a set of images  """

    # --- select phtometry group
    photom = hf['photom']

    if N:
        ids = photom['ID'][:N]  #  useful for testing
    else:
        ids = photom['ID'][:]

    for i, id in enumerate(ids):

        x = photom['X'][i]
        y = photom['Y'][i]

        # --- make a new image from a cutout of another image

        n = len(imgs)
        fig, axes = plt.subplots(1, n, figsize=(4*n, 4), dpi=size)
        plt.subplots_adjust(left=0, top=1, bottom=0, right=1, wspace=0.0, hspace=0.0)

        for filter_, ax in zip(filters_, axes):

            img = imgs[filter_]

            left = int(x-size/2)
            upper = int(img.size[1]-y-size/2)
            right = int(x+size/2)
            lower = int(img.size[1]-y+size/2)
            cutout = img.crop((left, upper, right, lower))
            ax.imshow(cutout)

            # --- add cross hairs
            dp = 0.5
            ax.plot([size/2 + dp, size/2 + dp], [size/2 - 3 + dp, size/2 - 10 + dp],  lw=4, c='w')
            ax.plot([size/2 - 3 + dp, size/2 - 10 + dp], [size/2 + dp, size/2 + dp],  lw=4, c='w')

            for axis in ['top', 'bottom', 'left', 'right']:
                ax.spines[axis].set_linewidth(4)

            ax.set_yticks([])
            ax.set_xticks([])
            # ax.set_axis_off()

        fn = f'{output_dir}/cutout_{id}.png'
        print(fn)
        fig.savefig(fn, dpi=size)


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointings = [1]
    versions = ['0.2']
    subcat = '-F22'
    # N = 10  # testing purposes
    N = 1

    filters = []
    # filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
    # filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W',
                                             'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W']]

    filters_ = [f.split('.')[-1].lower() for f in filters]

    for pointing in pointings:

        for version in versions:

            imgs = {f: Image.open(
                f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_{f}_v{version}.png') for f in filters_}

            imgs2 = {}
            imgs2['detection'] = Image.open(
                f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_detect_with-sources.png')
            imgs2['segmentation'] = Image.open(
                f'{ceers_dir}/myimages/{version}/ceers_nircam{pointing}_segmap.png')

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}'

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            cat_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}.h5'

            with h5py.File(cat_filename, 'r') as hf:

                create_multiimage(hf, imgs, filters_, output_dir=output_dir, N=N)
                # create_image(hf, imgs2, output_dir=output_dir, N=N)
