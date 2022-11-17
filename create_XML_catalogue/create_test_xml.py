


import pandas as pd
from astropy.table import Table
from astropy.io import ascii


photom_df = pd.DataFrame({'shape': ['square', 'circle', 'triangle'],
                    'degrees': [360, 360, 180],
                    'sides': [4, np.nan, 3]})

photom_df = photom.to_pandas()


xml = photom_df.to_xml(parser = 'etree')

with open('../data/test.xml', 'w') as f:
    f.writelines(xml)
