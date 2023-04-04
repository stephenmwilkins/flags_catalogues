

import numpy as np
import h5py
from astropy.io import ascii

def match_specz(survey, version, pointing, tolerance_arcsec = 0.15):
    '''Match to a spectroscopic redshift catalogue based on some arcsecond tolerance'''

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    tolerance_deg = tolerance_arcsec/3600.

    # --- specz catalogue #TODO Maybe change this to read in a more common file type (fits).
    specz_catalogue_name = f'{survey_dir}/cats/egs_specz_0822.ascii'
    specz_catalogue = ascii.read(specz_catalogue_name)

    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'

    catalogue_filename = f'{catalogue_id}.h5'

    with h5py.File(catalogue_filename, 'a') as hf:

        ids = hf['photom/ID'][:]
        N = len(ids)

        # Create a general 'z' dataset. This will store the best available redshift.
        if 'specz' in hf.keys():
            del hf['z']

        hf.create_dataset('z', data=hf[f'pz/{survey.lower()}/ZA'][:])  # best redshift
        z = hf['z']

        # Create dataset to store spectroscopic redshifts.
        if 'specz' in hf.keys():
            del hf['specz']

        specz = hf.create_group('specz')
        for k in ['z', 'quality']:
            specz.create_dataset(k, data=np.full(N, -1)) # Default value is -1 for an object with no spectroscopic confirmation.
        specz.create_dataset('catalogue', data=np.full(N, 'N',dtype='S10')) # Indicate the catalogue the redshift originates from.

        # Calculate separations.
        ra = hf['photom/RA'][:]
        dec = hf['photom/DEC'][:]

        for i in range(len(specz_catalogue['ra'])):

            r = np.sqrt((ra-specz_catalogue['ra'][i])**2 +
                        (dec-specz_catalogue['dec'][i])**2)

            j = np.argmin(r)

            # For objects within the given tolerance, save the spectroscopic redshift information.
            if r[j] < tolerance_deg:
                print(
                    f"{ids[j]} {specz_catalogue['z'][i]:.2f} {hf[f'pz/{survey.lower()}/ZA'][j]:.2f} | {hf[f'pz/{survey.lower()}/ZA'][j]-specz_catalogue['z'][i]:.2f}")

                for k in ['z', 'quality', 'catalogue']:
                    specz[k][j] = specz_catalogue[k][i]

        # Add spectroscopic redshifts to best redshift dataset.
        sz = specz['z'][:] > 0
        z[sz] = specz['z'][sz]

        hf.flush()
        hf.visit(print)