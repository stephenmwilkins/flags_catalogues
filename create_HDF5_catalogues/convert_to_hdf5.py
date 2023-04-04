import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits

def convert_to_hdf5(survey, version, pointing):
    '''Convert survey fits files to a single hdf5 catalogue'''

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    output_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}.h5'

    # Open the required catalogues.
    cat_photom = Table.read(f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}_photom.fits')
    cat_zphot = Table.read(f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}_photz_quantities.fits')
    cat_pz = Table.read(f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}_photz_pz.fits')
    cat_grid = fits.open(f'{survey_dir}/cats/{survey}_v{version}_photz_zgrid.fits')[0].data

    with h5py.File(output_filename, 'w') as hf:

        # Create group for photometry catalogue.
        photom = hf.create_group('photom')

        for col in cat_photom.colnames:
            photom[col] = cat_photom[col].data

        # Create both a top-level photometric redshift group and a ceers pz group inside
        pz = hf.create_group(f'pz/{survey.lower()}')

        # Store the full pz and the associated redshift grid.
        for col in cat_zphot.colnames:
            pz[col] = cat_zphot[col]

        pz['ZGRID'] = cat_grid
        pz['PZ'] = cat_pz['PZ']

    return output_filename