

import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits


def convert_ceers_to_hdf5(pointing, version, dir=''):
    """ converts the photom, zphot and pz (split to ZGRID and PZ) of given CEERS photometry versions into a HDF5 file """

    # --- the output filename
    output_filename = f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'

    # --- open catalogues to include
    ceers_photom = Table.read(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photom.fits')
    ceers_zphot = Table.read(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photz_quantities.fits')
    ceers_pz = Table.read(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photz_pz.fits')
    ceers_grid = fits.open(f'{dir}/cats/CEERS_v{version}_photz_zgrid.fits')[0].data

    # print(ceers_photom.colnames)
    #
    # hdu = fits.open(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photom.fits')
    # hdu.info()
    # print(hdu[1].header)

    with h5py.File(output_filename, 'w') as hf:

        # add in photometry

        photom = hf.create_group('photom')  # create group for photometry catalogue

        for col in ceers_photom.colnames:
            photom[col] = ceers_photom[col].data

        # create both a top-level photometric redshift group and a ceers pz group inside
        pz = hf.create_group('pz/ceers')

        for col in ceers_zphot.colnames:
            pz[col] = ceers_zphot[col]

        pz['ZGRID'] = ceers_grid
        pz['PZ'] = ceers_pz['PZ']

    return output_filename


if __name__ == '__main__':

    # this should be replaced by an environment variable or similar
    ceers_dir = '/Users/jt458/ceers'

    pointings = np.arange(1,11)
    versions = ['0.51.2']

    for pointing in pointings:
        for version in versions:
            output_filename = convert_ceers_to_hdf5(pointing, version, dir=ceers_dir)

            with h5py.File(output_filename, 'r') as hf:
                hf.visit(print)  # print a list of all datasets/groups

            # --- open up the resulting HDF file to check
