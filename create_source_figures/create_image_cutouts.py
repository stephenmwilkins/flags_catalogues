

from PIL import Image
from synthesizer.filters import FilterCollection
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py


plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')


def create_image_cutouts(survey, version, pointing, filters, size=300, subcat = None, N=None):
    """ create image cutouts from pngs for every image in dictionary individualy """

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    filters_ = [f.split('.')[-1].lower() for f in filters]

    imgs = {f: Image.open(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_{f}_v{version}.png') for f in filters_}

    imgs2 = {}
    imgs2['detection'] = Image.open(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_v{version}_detect_with-sources.png')
    imgs2['segmentation'] = Image.open(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_v{version}_segmap.png')
    
    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    cat_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    if subcat != None:
        cat_filename += f'-{subcat}'

    with h5py.File(cat_filename+'.h5', 'r') as hf:
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