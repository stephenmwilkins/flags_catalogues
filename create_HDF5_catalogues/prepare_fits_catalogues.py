import numpy as np
from astropy.table import Table
from astropy.io import fits

def prepare_ceers_catalogue(version, dir = ''):
    """Splits the full CEERS catalogue into catalogues for different pointings."""

    # Open catalogues to include.
    photom = Table.read(f'{dir}/cats/CEERS_v{version}_photom.fits')
    zphot = Table.read(f'{dir}/cats/CEERS_v{version}_photz_quantities.fits')
    pz = fits.open(f'{dir}/cats/CEERS_v{version}_photz_pz.fits')[0].data


    pointings = np.arange(1,11)

    # Create new set of tables for each pointing.
    for pointing in pointings:
    
        photom_ = Table()
        zphot_ = Table()
        pz_ = Table()

        s = photom['FIELD'] == pointing

        for col in photom[s].colnames:
            photom_[col] = photom[col][s].data

        for col in zphot[s].colnames:
                zphot_[col] = zphot[col][s].data

        pz_['PZ'] = pz[s]
        
        # Names match June2022 catalogue format.
        photom_.write(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photom.fits', format = 'fits', overwrite = True)
        zphot_.write(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photz_quantities.fits', format = 'fits', overwrite = True)
        pz_.write(f'{dir}/cats/CEERS_NIRCam{pointing}_v{version}_photz_pz.fits', format = 'fits', overwrite = True)

        print(f'Split pointing {pointing}')

def prepare_ngdeep_catalogue(version, dir = ''):

    photom = Table.read(f'{dir}/cats/NGDEEP_v{version}_photom.fits')
    zphot = Table.read(f'{dir}/cats/NGDEEP_v{version}_photz_quantities.fits')
    pz = fits.open(f'{dir}/cats/NGDEEP_v{version}_photz_pz.fits')[0].data

    pointings = [1]

    for pointing in pointings:
        pz_ = Table()
        pz_['PZ'] = pz

        photom.write(f'{dir}/cats/NGDEEP_NIRCam{pointing}_v{version}_photom.fits', format = 'fits', overwrite = True)
        zphot.write(f'{dir}/cats/NGDEEP_NIRCam{pointing}_v{version}_photz_quantities.fits', format = 'fits', overwrite = True)
        pz_.write(f'{dir}/cats/NGDEEP_NIRCam{pointing}_v{version}_photz_pz.fits', format = 'fits', overwrite = True)     

if __name__ == '__main__':

    ceers_dir = '/Users/jt458/ceers'

    prepare_ceers_catalogue('0.51.2', dir = ceers_dir)

    prepare_ngdeep_catalogue('0.1', dir = '/Users/jt458/ngdeep')
