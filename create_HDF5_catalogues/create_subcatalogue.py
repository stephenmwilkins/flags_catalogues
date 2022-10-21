



import numpy as np
import h5py



if __name__ == '__main__':

    ceers_dir = '/Users/stephenwilkins/Dropbox/Research/data/images/jwst/ceers'  # this should be replaced by an environment variable or similar

    pointings = [1,2,3,6]
    pointings = [1]
    versions = ['0.2']

    for pointing in pointings:
        for version in versions:


            catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}.h5'
            new_catalogue_filename = f'{ceers_dir}/cats/CEERS_NIRCam{pointing}_v{version}-colours.h5'

            with h5py.File(catalogue_filename,'r') as hf:

                # hf.visit(print) # print a list of all datasets/groups

                p = hf['photom'] # photometry group
                pz = hf['pz/ceers'] # photometric redshift group

                # --- apply a filter to all datasets

                sn = hf['photom/F200'][:]/hf['photom/DF200'][:]

                s = (pz['ZA'][:]>4.5) &(sn>10)

                print(f'number of sources selected: {np.sum(s)}')


                hfn = h5py.File(new_catalogue_filename,'w')

                def make_copy(name,item):
                    if isinstance(item, h5py.Dataset):
                        print(name)
                        if name.split('/')[-1] == 'ZGRID':
                            hfn[name] = item[:]
                        else:
                            hfn[name] = item[s]

                hf.visititems(make_copy)

                hfn.close()
