import numpy as np
import h5py

def update_spurious(survey, cat_version, pointing, survey_dir = ''):
    '''
    Create or update a dataset indicating which objects have been identified as spurious.
    '''
    survey = survey.upper()

    # Load catalogue.
    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    catalogue_filename = f'{catalogue_id}.h5'

    # Load in external file with list of spurious objects. Text file with each spurious id on a new line.
    spurious_list = list(set(np.loadtxt(f'{catalogue_id}-spurious.dat', dtype=int)))
    close_list = list(set(np.loadtxt(f'{catalogue_id}-close.dat', dtype=int)))

    if type(spurious_list) == int:
        spurious_list = [spurious_list]
    if type(close_list) == int:
        close_list = [close_list]

    spurious_list.sort()
    close_list.sort()

    with h5py.File(catalogue_filename, 'a') as hf:

        spurious_ids = [list(hf['photom/ID'][:]).index(id) for id in spurious_list]
        close_ids = [list(hf['photom/ID'][:]).index(id) for id in close_list]

        if 'spurious' in hf.keys():
            del hf['spurious']
        if 'close' in hf.keys():
            del hf['close']
            
        # True if spurious.
        hf['spurious'] = np.zeros(len(hf['photom/ID'][:]))
        hf['spurious'][spurious_ids] = 1

        hf['close'] = np.zeros(len(hf['photom/ID'][:]))
        hf['close'][close_ids] = 1

