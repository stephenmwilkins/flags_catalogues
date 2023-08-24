import h5py
import numpy as np

def compare_catalogue(new_cat, old_cat):

    with h5py.File(new_cat, 'r') as hf:
        new_ID = set(hf['photom/ID'][:])
    with h5py.File(old_cat, 'r') as hf:
        old_ID = set(hf['photom/ID'][:])

    in_new = [i for i in new_ID ^ old_ID if i in new_ID]

    s = []
    for i in new_ID:
        if i in in_new:
            s += [True]
        else:
            s += [False]

    with h5py.File(new_cat, 'r') as hf:

        # Create new subcatalogue.
        hfn = h5py.File(f'{new_cat.split(".h5")[0]}-diff.h5', 'w')

        def make_copy(name, item):
            if isinstance(item, h5py.Dataset):
                if name.split('/')[-1] == 'ZGRID': # Don't apply the selection within ZGRID. Just copy it.
                    hfn[name] = item[:]
                else:
                    hfn[name] = item[s]

        hf.visititems(make_copy)

        hfn.close()

if __name__ == '__main__':
    pointings = np.arange(1,11)
    for pointing in pointings:
        compare_catalogue(f'/Users/jt458/ceers/cats/CEERS_NIRCam{pointing}_v0.51.3-CEERS_colours_v4.h5',f'/Users/jt458/ceers/cats/CEERS_NIRCam{pointing}_v0.51.3-CEERS_colours_v3.h5')





