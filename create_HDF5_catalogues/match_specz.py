

import numpy as np
import h5py
from astropy.io import ascii

def match_specz(survey, version, pointing, tolerance_arcsec = 0.15):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    tolerance_deg = tolerance_arcsec/3600.

    # --- specz catalogue
    specz_catalogue_name = f'{survey_dir}/cats/egs_specz_0822.ascii'
    specz_catalogue = ascii.read(specz_catalogue_name)
    # print(specz_catalogue)

    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'

    catalogue_filename = f'{catalogue_id}.h5'

    with h5py.File(catalogue_filename, 'a') as hf:

        # hf.visit(print)

        ids = hf['photom/ID'][:]
        N = len(ids)

        # --- should be done earlier

        if 'specz' in hf.keys():
            del hf['z']

        hf.create_dataset('z', data=hf[f'pz/{survey.lower()}/ZA'][:])  # best redshift

        z = hf['z']

        if 'specz' in hf.keys():
            del hf['specz']

        specz = hf.create_group('specz')
        for k in ['z', 'quality']:
            specz.create_dataset(k, data=np.full(N, -1))
        specz.create_dataset('catalogue', data=np.empty(N, dtype='S10'))

        ra = hf['photom/RA'][:]
        dec = hf['photom/DEC'][:]

        for i in range(len(specz_catalogue['ra'])):

            r = np.sqrt((ra-specz_catalogue['ra'][i])**2 +
                        (dec-specz_catalogue['dec'][i])**2)

            j = np.argmin(r)

            if r[j] < tolerance_deg:
                print(
                    f"{ids[j]} {specz_catalogue['z'][i]:.2f} {hf[f'pz/{survey.lower()}/ZA'][j]:.2f} | {hf[f'pz/{survey.lower()}/ZA'][j]-specz_catalogue['z'][i]:.2f}")

                for k in ['z', 'quality', 'catalogue']:
                    specz[k][j] = specz_catalogue[k][i]

        sz = specz['z'][:] > 0  # identify galaxies with spectroscopic redshifts
        z[sz] = specz['z'][sz]  # update redshift to use spectrosocpic redshifts where available

        hf.flush()
        hf.visit(print)

#if __name__ == '__main__':
    #survey = 'CEERS'
    #version = '0.51.2'
    #pointings = np.arange(1,11)

    #for pointing in pointings:
        #match_specz(survey, version, pointing) 