

import numpy as np
import h5py
from flare.photom import flux_to_m

from selections import criteria, CEERS


F22_ids = {}
F22_ids[1] = [1730, 1875, 3858, 3908, 3910, 4143, 5534, 6059, 7227, 8817]


if __name__ == '__main__':

    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    # criteria_code = 'F22'
    criteria_code = 'high-z.v0.1'
    pointings = [1, 2, 3, 6]
    pointings = [1]
    versions = ['0.2']

    criteria_ = criteria[criteria_code]

    for pointing in pointings:
        for version in versions:

            catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

            with h5py.File(catalogue_filename, 'r') as hf:

                sel = CEERS(hf)

                s = sel.get_selection(criteria_)

                # sel.check_sources(F22_ids[pointing])


# CEERS1_1730  215.010022  53.013641  27.7  0.97  13.36  0.84  1.08  4.4
# CEERS1_1875  214.951936  52.971742  27.1  0.92  8.92  0.06  0.57  5.4
# CEERS1_3858  214.994402  52.989379  27.2  0.99  8.95  0.15  0.18  7.6
# CEERS1_3908  215.005189  52.996580  27.3  0.96  9.04  1.29  0.06  5.3
# CEERS1_3910  215.005365  52.996697  28.0  0.96  9.55  1.05  0.39  5.7
# CEERS1_4143  214.966717  52.968286  28.1  0.84  8.98  0.60  1.23  4.0
# CEERS1_5534  214.950078  52.949267  27.9  1.00  8.62  0.30  0.39  12.6
# CEERS1_6059  215.011706  52.988303  27.0  1.00  9.01  0.06  0.06  48.0
# CEERS1_7227  215.037504  52.999394  28.3  0.85  11.23  0.30  1.86  4.0
# CEERS1_8817  215.043999  52.994302  28.1  1.00  10.60  0.42  0.36  12.1
