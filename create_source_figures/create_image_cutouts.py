

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


def create_image_cutouts(survey, img_version, pointing, filters, cat_version = None, size=300, subcat = None, survey_dir = '', N=None):
    """ create image cutouts from pngs for every image in dictionary individualy """

    # Should the same catalogue and image versions be used?
    if cat_version == None:
        cat_version = img_version

    survey = survey.upper()

    # Get filter names in the right format.
    filters_ = [f.split('.')[-1].lower() for f in filters]

    # Open the single band image for each filter.
    imgs = {f: Image.open(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_{f}_v{img_version}.png') for f in filters_}

    # Open the detection and segementation images.
    imgs2 = {}
    imgs2['detection'] = Image.open(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_v{img_version}_detect_with-sources.png')
    imgs2['segmentation'] = Image.open(
        f'{survey_dir}/myimages/{survey.lower()}_nircam{pointing}_v{img_version}_segmap.png')
    
    # Save the images here.
    output_dir = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Catalogue to load.
    cat_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    if subcat != None:
        cat_filename += f'-{subcat}'

    with h5py.File(cat_filename+'.h5', 'r') as hf:
        # Select phtometry group
        photom = hf['photom']

        # For testing.
        if N:
            ids = photom['ID'][:N] 
        else:
            ids = photom['ID'][:]

        for i, id in enumerate(ids):

            # X and Y position of the source.
            x = photom['X'][i]
            y = photom['Y'][i]

            for img_name, img in imgs.items():

                # Figure properties based on X and Y position of source.
                fig = plt.figure(figsize=(1, 1), dpi=size)
                ax = fig.add_axes((0.0, 0.0, 1., 1.))
                left = int(x-size/2)
                upper = int(img.size[1]-y-size/2)
                right = int(x+size/2)
                lower = int(img.size[1]-y+size/2)

                # Crop and plot the image to create cutout.
                cutout = img.crop((left, upper, right, lower))
                ax.imshow(cutout)

                ax.set_axis_off()

                fn = f'{output_dir}/{img_name}_{id}.png'
                fig.savefig(fn)
                plt.close(fig)

            for img_name, img in imgs2.items():

                # Figure properties based on X and Y position of source.
                fig = plt.figure(figsize=(1, 1), dpi=size)
                ax = fig.add_axes((0.0, 0.0, 1., 1.))
                left = int(x-size/2)
                upper = int(img.size[1]-y-size/2)
                right = int(x+size/2)
                lower = int(img.size[1]-y+size/2)

                # Crop and plot the image to create cutout.
                cutout = img.crop((left, upper, right, lower))
                ax.imshow(cutout)

                ax.set_axis_off()

                fn = f'{output_dir}/{img_name}_{id}.png'
                fig.savefig(fn)
                plt.close(fig)
    for img in list(imgs.values()):
        img.close()
    for img in list(imgs2.values()):
        img.close()