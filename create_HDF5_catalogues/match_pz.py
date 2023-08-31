import glob

import numpy as np
import h5py
from astropy.io import ascii
from astropy.table import Table

# Seems to be an issue with IDs.

def match_pz(survey, cat_version, pointing, tolerance_arcsec = 0.15, survey_dir = ''):
    '''Match to an external photometric redshift catalogue based on some arcsecond tolerance'''

    survey = survey.upper()

    tolerance_deg = tolerance_arcsec/3600.

    # Load in external catalogues.
    catalogue_files = glob.glob(f'{survey_dir}/external_cats/pz/*')
    catalogue_names = [c.split('/')[-1].split('.')[0] for c in catalogue_files]
    catalogues = {}

    for catalogue_name, catalogue_file in zip(catalogue_names, catalogue_files):

        catalogues[catalogue_name] = Table.read(catalogue_file)

    # Load the survey catalogue.
    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    catalogue_filename = f'{catalogue_id}.h5'
    with h5py.File(catalogue_filename, 'a') as hf:

        ids = hf['photom/ID'][:]
        N = len(ids)

        ra = hf['photom/RA'][:]
        dec = hf['photom/DEC'][:]

        # Create a group for storing information from the matached catalogues.
        if 'matched' in hf.keys():
            del hf['matched']

        matched = hf.create_group('matched')

        for catalogue_name in catalogue_names:

            ecat = catalogues[catalogue_name]

            # Create a group within the matched group for each individual catalogue.
            matched_ = matched.create_group(catalogue_name)
            matched_.create_dataset('z', data=np.full(N, -1, dtype = 'float')) # Dataset storing the redshift from that catalogue, -1 if no match.
            matched_.create_dataset('id', data=np.full(N, 'N', dtype='S10')) # The object id in that catalogue, 'N' if no match.

            # Loop over every galaxy in the base catalogue and check if its in the external catalogue.
            for i, (ra_, dec_) in enumerate(zip(ra, dec)):

                r = np.sqrt((ra_ - ecat['ra'].value)**2 +
                            (dec_ - ecat['dec'].value)**2)

                j = np.argmin(r)

                # Add to matched if within the given tolerance.
                if r[j] < tolerance_deg:
                    for k in ['z', 'id']:
                        matched_[k][i] = ecat[k][j]