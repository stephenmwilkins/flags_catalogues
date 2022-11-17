
import sys
import numpy as np
import h5py
import pandas as pd
from astropy.table import Table, join, hstack
from astropy.io import ascii, fits


# this should be replaced by an environment variable or similar
ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

subcat = '-high-z.v0.1'
if len(sys.argv) > 1:
    subcat = '-'+sys.argv[1]


pointings = [1, 2, 3, 6]
pointings = [1, 2, 3, 6]
versions = ['0.2']


for pointing in pointings:
    for version in versions:

        filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat}'

        # open HDF5 catalogue

        d = {}

        with h5py.File(filename+'.h5', 'r') as hf:

            # print(hf.visit(print))

            sh = hf['photom/ID'][:].shape

            def add_to_dict(name, item):
                if isinstance(item, h5py.Dataset):
                    if item[:].shape == sh:
                        name = name.replace('/', '-')
                        d[name] = item[:]

            hf.visititems(add_to_dict)

        df = pd.DataFrame(d)

        xml = df.to_xml(parser='etree')

        with open(f'{filename}.xml', 'w') as f:
            f.writelines(xml)


# hf.visititems(make_copy)
