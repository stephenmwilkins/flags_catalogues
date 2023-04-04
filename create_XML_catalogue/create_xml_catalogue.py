
import sys
import numpy as np
import h5py
import pandas as pd
from astropy.table import Table, join, hstack
from astropy.io import ascii, fits



def create_xml_catalogue(survey, version, pointing, subcat = None):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
    if subcat != None:
        filename += f'-{subcat}'

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

create_xml_catalogue('CEERS', '0.51.2', 4, subcat = 'high-z.v0.1')