

import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits


def convert_ngdeep_to_hdf5(pointing, version, dir=''):
    """ converts the photom, zphot and pz (split to ZGRID and PZ) of given ngdeep photometry versions into a HDF5 file """

    # --- the output filename
    output_filename = f'{dir}/cats/ngdeep_NIRCam{pointing}_v{version}.h5'

    # --- open catalogues to include
    ngdeep_photom = Table.read(f'{dir}/cats/NGDEEP_NIRCam{pointing}_v{version}_photom.fits')
    ngdeep_zphot = Table.read(f'{dir}/cats/NGDEEP_NIRCam{pointing}_v{version}_photz_quantities.fits')
    ngdeep_pz = Table()
    ngdeep_pz['PZ'] = fits.open(f'{dir}/cats/NGDEEP_NIRCam{pointing}_v{version}_photz_pz.fits')[0].data
    ngdeep_grid = fits.open(f'{dir}/cats/NGDEEP_v{version}_photz_zgrid.fits')[0].data

    # print(ngdeep_photom.colnames)
    #
    # hdu = fits.open(f'{dir}/cats/ngdeep_NIRCam{pointing}_v{version}_photom.fits')
    # hdu.info()
    # print(hdu[1].header)

    with h5py.File(output_filename, 'w') as hf:

        # add in photometry

        photom = hf.create_group('photom')  # create group for photometry catalogue

        for col in ngdeep_photom.colnames:
            photom[col] = ngdeep_photom[col].data

        # create both a top-level photometric redshift group and a ngdeep pz group inside
        pz = hf.create_group('pz/ngdeep')

        for col in ngdeep_zphot.colnames:
            pz[col] = ngdeep_zphot[col]

        pz['ZGRID'] = ngdeep_grid
        pz['PZ'] = ngdeep_pz['PZ']

    return output_filename


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ngdeep_dir = '/Users/jt458/ngdeep'

    pointings = [1]
    versions = ['0.1']

    for pointing in pointings:
        for version in versions:
            output_filename = convert_ngdeep_to_hdf5(pointing, version, dir=ngdeep_dir)

            with h5py.File(output_filename, 'r') as hf:
                hf.visit(print)  # print a list of all datasets/groups

            # --- open up the resulting HDF file to check
