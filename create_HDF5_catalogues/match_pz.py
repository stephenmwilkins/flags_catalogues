
import glob

import numpy as np
import h5py
from astropy.io import ascii
from astropy.table import Table

from selections import criteria, CEERS


# Not 100% convinced this is working correctly yet.
if __name__ == '__main__':

    """ matches with other catalogues """

    ceers_dir = '/Users/jt458/ceers'

    pointings = np.arange(1,11)
    #pointings = [2]
    versions = ['0.51.2']

    tolerance_arcsec = 0.15
    tolerance_deg = tolerance_arcsec/3600.

    catalogue_files = glob.glob(f'{ceers_dir}/external_cats/pz/*.ecsv')
    catalogue_names = [c.split('/')[-1].split('.')[0] for c in catalogue_files]
    catalogues = {}

    for catalogue_name, catalogue_file in zip(catalogue_names, catalogue_files):

        catalogues[catalogue_name] = Table.read(catalogue_file)

    for pointing in pointings:
        for version in versions:

            catalogue_id = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'
            catalogue_filename = f'{catalogue_id}.h5'

            with h5py.File(catalogue_filename, 'a') as hf:

                # hf.visit(print)

                ids = hf['photom/ID'][:]
                N = len(ids)

                ra = hf['photom/RA'][:]
                dec = hf['photom/DEC'][:]

                if 'matched' in hf.keys():
                    del hf['matched']

                matched = hf.create_group('matched')

                for catalogue_name in catalogue_names:

                    print('-'*10, catalogue_name)

                    ecat = catalogues[catalogue_name]

                    matched_ = matched.create_group(catalogue_name)
                    matched_.create_dataset('z', data=np.empty(N))
                    matched_.create_dataset('id', data=np.empty(N, dtype='S10'))

                    # --- could potentially simply loop over datasets and copy everything over

                    # --- loop over every galaxy in the base catalogue and check if its in the external catalogue

                    for i, (ra_, dec_) in enumerate(zip(ra, dec)):

                        r = np.sqrt((ra_ - ecat['ra'].value)**2 +
                                    (dec_ - ecat['dec'].value)**2)

                        j = np.argmin(r)

                        if r[j] < tolerance_deg:
                            print(
                                f"{ids[i]} {ecat['id'][j]} {ecat['z'][j]:.2f} {hf['pz/ceers/ZA'][i]:.2f} | {hf['pz/ceers/ZA'][i]-ecat['z'][j]:.2f}")

                            for k in ['z', 'id']:
                                matched_[k][i] = ecat[k][j]

                # hf.visit(print)
