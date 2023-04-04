

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import cmasher as cmr
import h5py
from astropy.io import fits
from astropy.visualization import make_lupton_rgb


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointing = 1
    version = '0.2'

    filters = []
    filters += ['f115w', 'f150w', 'f200w', 'f277w', 'f356w', 'f444w']

    rgb_filters = {''}  # ultimately want to stack groups

    imgs = {}

    for filter in filters:
        imgs[filter] = np.load(f'{ceers_dir}/images/{version}/cutout_{filter}.npy')

    im = {}
    im['r'] = imgs['f356w'] + imgs['f444w']
    im['g'] = imgs['f200w'] + imgs['f277w']
    im['b'] = imgs['f115w'] + imgs['f150w']

    # for f in ['r', 'g', 'b']:
    #     threshold = -np.percentile(im[f][im[f] < 0.0], 0.32)
    #     norm = plt.Normalize(0.0, threshold*10.)
    #     im[f] = norm(im[f])

    image = make_lupton_rgb(im['r'], im['g'], im['b'], Q=8, stretch=0.1)

    fig = plt.figure(figsize=(4, 4), dpi=250)
    ax = fig.add_axes((0.0, 0.0, 1., 1.))
    ax.imshow(image)
    ax.set_axis_off()

    fig.savefig(f'rgb_test.png')
