
import sys
import numpy as np
import h5py
import pandas as pd
from astropy.table import Table, join, hstack
from astropy.io import ascii, fits



def create_xml_catalogue(survey, cat_version, pointing, subcat = None, survey_dir = ''):

    survey = survey.upper()

    # Catalogue to use.
    filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    if subcat != None:
        filename += f'-{subcat}'

    d = {}
    with h5py.File(filename+'.h5', 'r') as hf:

        # print(hf.visit(print))

        sh = hf['photom/ID'][:].shape

        # Copy the data to a dictionary.
        def add_to_dict(name, item):
            if isinstance(item, h5py.Dataset):
                if item[:].shape == sh:
                    name = name.replace('/', '-')
                    d[name] = item[:]

        hf.visititems(add_to_dict)

    # Convert to pandas dataframe and then to XML.
    df = pd.DataFrame(d)

    xml = df.to_xml(parser='etree')

    # Write to XML.
    with open(f'{filename}.xml', 'w') as f:
        f.writelines(xml)

pointings = np.arange(1,11)
for pointing in pointings:
    create_xml_catalogue('CEERS', '0.51.2', pointing, subcat = 'high-z.v0.1', survey_dir='/Users/jt458/ceers')