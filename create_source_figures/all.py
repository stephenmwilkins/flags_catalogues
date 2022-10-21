
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

from synthesizer.filters import SVOFilterCollection
import pysep.sep as sep
import pysep.utils
import pysep.plots.image
import pysep.analyse


from sed import create_sed_plot
from pz import create_pz_plot
from images import create_multiband_image
from detection import create_significance_plots



if __name__ == '__main__':


    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'  # this should be replaced by an environment variable or similar

    subcat = '-highz'
    pointings = [1]
    versions = ['0.2']



    filters = []
    filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
    filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]

    img_filters = [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]
    img_filters_ = [f.split('.')[-1].lower() for f in img_filters]

    detection_filter = 'f200w' # should replace by a stacked detection image



    for pointing in pointings:

        for version in versions:

            output_dir = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}'

            Path(output_dir).mkdir(parents=True, exist_ok=True) # create output directory

            output_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}.h5'

            imgs = {f: pysep.utils.ImageFromMultiFITS(f'{ceers_dir}/images/ceers_nircam{pointing}_{f}_v{version}_i2d.fits') for f in img_filters_}

            detection_image = pysep.utils.ImageFromMultiFITS(f'{ceers_dir}/images/ceers_nircam{pointing}_{detection_filter}_v{version}_i2d.fits')
            detection_image.measure_background_map() # required

            with h5py.File(output_filename,'r') as hf:

                create_sed_plot(hf, output_dir = output_dir, filters = filters)
                create_pz_plot(hf, output_dir = output_dir)
                create_multiband_image(hf, imgs, img_filters, output_dir = output_dir)
                create_significance_plots(hf, detection_image, output_dir = output_dir)
