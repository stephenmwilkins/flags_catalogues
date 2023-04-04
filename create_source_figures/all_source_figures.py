
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')

from synthesizer.filters import FilterCollection
import pysep.sep as sep
import pysep.utils
import pysep.plots.image
import pysep.analyse

from create_sed_plot import create_sed_plot
from create_pz_plot import create_pz_plot
from create_multiband_image import create_multiband_image
from create_significance_plots import create_significance_plots
from create_multi_image import create_multi_image
from create_image_cutouts import create_image_cutouts

if __name__ == '__main__':

    subcat = 'high-z.v0.1'
    survey = 'CEERS'
    pointing = 4
    version = '0.51.2'


    filters = []
    filters += [f'HST/ACS_WFC.{f}' for f in ['F606W', 'F814W']]
    filters += [f'HST/WFC3_IR.{f}' for f in ['F105W', 'F125W', 'F160W']]
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]

    img_filters = [f'JWST/NIRCam.{f}' for f in ['F115W','F150W', 'F200W','F277W','F356W','F410M','F444W']]

    detection_filter = 'f200w' # should replace by a stacked detection image

    create_sed_plot(survey, version, pointing, filters = filters, subcat = subcat)
    create_pz_plot(survey, version, pointing, subcat = subcat)
    #create_multiband_image(survey, version, pointing, filters = img_filters, subcat = subcat)
    create_significance_plots(survey, version, pointing, detection_filter, subcat = subcat)
    create_multi_image(survey, version, pointing, img_filters, subcat = subcat)
    create_image_cutouts(survey, version, pointing, img_filters, subcat = subcat)
