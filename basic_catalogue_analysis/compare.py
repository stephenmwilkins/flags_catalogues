import h5py
import numpy as np

def compare_catalogue(new_cat, old_cat, create_new = True):
    '''Return an array of IDs that are present in the first catalogue but not in the second.'''

    # Get list of IDs for both catalogues.
    with h5py.File(new_cat, 'r') as hf:
        new_ID = list(hf['photom/ID'][:])
    with h5py.File(old_cat, 'r') as hf:
        old_ID = list(hf['photom/ID'][:])

    # List of IDs that only appear in the new catalogue.
    in_new = [i for i in set(new_ID) ^ set(old_ID) if i in new_ID]

    # Selection array.
    s = [i in in_new for i in new_ID]

    # Create a new catalogue containing on the objects that are in the new catalogue but not the old.
    if create_new == True:
        with h5py.File(new_cat, 'r') as hf:

            # Create new subcatalogue with the "-diff" suffix.
            hfn = h5py.File(f'{new_cat.split(".h5")[0]}-diff.h5', 'w')

            def make_copy(name, item):
                if isinstance(item, h5py.Dataset):
                    if name.split('/')[-1] == 'ZGRID': # Don't apply the selection within ZGRID. Just copy it.
                        hfn[name] = item[:]
                    else:
                        hfn[name] = item[s]

            hf.visititems(make_copy)

            hfn.close()

    # Return the array of IDs that are only in the new catalogue.
    return np.array(new_ID)[s]

