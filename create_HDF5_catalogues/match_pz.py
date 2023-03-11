import glob

import numpy as np
import h5py
from astropy.io import ascii
from astropy.table import Table

# Seems to be an issue with IDs.

def match_pz(survey, version, pointing, tolerance_arcsec = 0.15):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    tolerance_deg = tolerance_arcsec/3600.

    catalogue_files = glob.glob(f'{survey_dir}/external_cats/pz/*.ecsv')
    catalogue_names = [c.split('/')[-1].split('.')[0] for c in catalogue_files]
    catalogues = {}

    for catalogue_name, catalogue_file in zip(catalogue_names, catalogue_files):

        catalogues[catalogue_name] = Table.read(catalogue_file)

    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'
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
            matched_.create_dataset('z', data=np.full(N, -1))
            matched_.create_dataset('id', data=np.empty(N, 'S10'))

            # --- could potentially simply loop over datasets and copy everything over

            # --- loop over every galaxy in the base catalogue and check if its in the external catalogue

            for i, (ra_, dec_) in enumerate(zip(ra, dec)):

                r = np.sqrt((ra_ - ecat['ra'].value)**2 +
                            (dec_ - ecat['dec'].value)**2)

                j = np.argmin(r)

                if r[j] < tolerance_deg:
                    #print(
                        #f"{ids[i]} {ecat['id'][j]} {ecat['z'][j]:.2f} {hf[f'pz/{survey}/ZA'][i]:.2f} | {hf[f'pz/{survey}/ZA'][i]-ecat['z'][j]:.2f}")

                    for k in ['z', 'id']:
                        matched_[k][i] = ecat[k][j]

        # hf.visit(print)

#if __name__ == '__main__':
    #survey = 'CEERS'
    #pointings = np.arange(1,11)
    #version = '0.51.2'

    #for pointing in pointings:
        #match_pz(survey, version, pointing)