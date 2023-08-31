from PIL import Image
from synthesizer.filters import FilterCollection
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import h5py

def create_multi_image(survey, img_version, pointing, filters, cat_version = None, size=50, subcat = None, survey_dir = '', N=None):
    """ create a single image from a set of images  """

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
        # Select phtometry group.
        photom = hf['photom']

        # Useful for testing.
        if N:
            ids = photom['ID'][:N] 
        else:
            ids = photom['ID'][:]

        for i, id in enumerate(ids):

            # X and Y position of the source.
            x = photom['X'][i]
            y = photom['Y'][i]

            # Number of cutouts to include in the image.
            n = len(imgs)

            fig, axes = plt.subplots(1, n, figsize=(4*n, 4), dpi=size)
            plt.subplots_adjust(left=0, top=1, bottom=0, right=1, wspace=0.0, hspace=0.0)

            for filter_, ax in zip(filters_, axes):

                # Select filter.
                img = imgs[filter_]

                # Figure properties.
                left = int(x-size/2)
                upper = int(img.size[1]-y-size/2)
                right = int(x+size/2)
                lower = int(img.size[1]-y+size/2)
                
                # Crop and plot image.
                cutout = img.crop((left, upper, right, lower))
                ax.imshow(cutout)

                # Add cross hairs
                dp = 0.5
                ax.plot([size/2 + dp, size/2 + dp], [size/2 - 3 + dp, size/2 - 10 + dp],  lw=4, c='w')
                ax.plot([size/2 - 3 + dp, size/2 - 10 + dp], [size/2 + dp, size/2 + dp],  lw=4, c='w')

                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(4)

                ax.set_yticks([])
                ax.set_xticks([])
                # ax.set_axis_off()

            fn = f'{output_dir}/cutout_{id}.png'
            fig.savefig(fn, dpi=size)
            plt.close(fig)
    for img in list(imgs.values()):
        img.close()
    for img in list(imgs2.values()):
        img.close()