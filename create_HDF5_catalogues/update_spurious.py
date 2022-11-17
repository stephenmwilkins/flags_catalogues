

import numpy as np
import h5py

from selections import criteria, CEERS

if __name__ == '__main__':

    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointings = [1, 2, 3, 6]
    # pointings = [1]
    versions = ['0.2']

    for pointing in pointings:
        for version in versions:

            print('-'*30)
            print(pointing)

            catalogue_id = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'

            catalogue_filename = f'{catalogue_id}.h5'

            spurious_list = np.loadtxt(f'{catalogue_id}-spurious.dat', dtype=int)

            spurious_ids = list(spurious_list-1)

            print(spurious_ids)

            with h5py.File(catalogue_filename, 'a') as hf:

                # hf.visit(print)

                if 'spurious' in hf.keys():
                    del hf['spurious']

                hf['spurious'] = np.zeros(len(hf['photom/ID'][:]))
                hf['spurious'][spurious_ids] = 1
