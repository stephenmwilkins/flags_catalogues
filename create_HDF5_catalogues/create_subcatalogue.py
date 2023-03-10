

import numpy as np
import h5py

from selections import criteria, CEERS

if __name__ == '__main__':

    ceers_dir = '/Users/jt458/ceers'

    # criteria_code = 'F22'
    criteria_code = 'high-z.v0.1'

    subcat_name = f'-{criteria_code}'
    pointings = np.arange(1,11)
    #pointings = [1]
    versions = ['0.51.2']

    criteria_ = criteria[criteria_code]

    for pointing in pointings:
        for version in versions:

            print(pointing, criteria_code)

            catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'
            new_catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}{subcat_name}.h5'

            with h5py.File(catalogue_filename, 'r') as hf:

                sel = CEERS(hf)

                s = sel.get_selection(criteria_)

                hfn = h5py.File(new_catalogue_filename, 'w')

                def make_copy(name, item):
                    if isinstance(item, h5py.Dataset):
                        # print(name)
                        if name.split('/')[-1] == 'ZGRID':
                            hfn[name] = item[:]
                        else:
                            hfn[name] = item[s]

                hf.visititems(make_copy)

                hfn.close()
