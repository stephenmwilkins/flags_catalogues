

import numpy as np
import h5py
from astropy.io import ascii

from selections import criteria, CEERS

if __name__ == '__main__':

    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'

    pointings = [1, 2, 3, 6]
    # pointings = [1]
    versions = ['0.2']

    tolerance_arcsec = 0.15
    tolerance_deg = tolerance_arcsec/3600.

    # --- specz catalogue
    specz_catalogue_name = f'{ceers_dir}/cats/egs_specz_0822.txt'
    specz_catalogue = ascii.read(specz_catalogue_name)
    # print(specz_catalogue)

    for pointing in pointings:
        for version in versions:

            catalogue_id = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}'

            catalogue_filename = f'{catalogue_id}.h5'

            with h5py.File(catalogue_filename, 'a') as hf:

                # hf.visit(print)

                ids = hf['photom/ID'][:]
                N = len(ids)

                # --- should be done earlier

                if 'specz' in hf.keys():
                    del hf['z']

                hf.create_dataset('z', data=hf['pz/ceers/ZA'][:])  # best redshift

                z = hf['z']

                if 'specz' in hf.keys():
                    del hf['specz']

                specz = hf.create_group('specz')
                for k in ['z', 'quality']:
                    specz.create_dataset(k, data=np.zeros(N))
                specz.create_dataset('catalogue', data=np.empty(N, dtype='S10'))

                ra = hf['photom/RA'][:]
                dec = hf['photom/DEC'][:]

                for i in range(len(specz_catalogue['ra'])):

                    r = np.sqrt((ra-specz_catalogue['ra'][i])**2 +
                                (dec-specz_catalogue['dec'][i])**2)

                    j = np.argmin(r)

                    if r[j] < tolerance_deg:
                        print(
                            f"{ids[j]} {specz_catalogue['z'][i]:.2f} {hf['pz/ceers/ZA'][j]:.2f} | {hf['pz/ceers/ZA'][j]-specz_catalogue['z'][i]:.2f}")

                        for k in ['z', 'quality', 'catalogue']:
                            specz[k][j] = specz_catalogue[k][i]

                sz = specz['z'][:] > 0  # identify galaxies with spectroscopic redshifts
                z[sz] = specz['z'][sz]  # update redshift to use spectrosocpic redshifts where available

                hf.flush()
                hf.visit(print)
