import numpy as np
import h5py

def update_spurious(survey, cat_version, pointing, survey_dir = ''):
    '''
    Create or update a dataset indicating which objects have been identified as spurious.
    '''
    survey = survey.upper()

    print('-'*30)
    print(pointing)

    # Load in external file with list of spurious objects. Text file with each spurious id on a new line.
    spurious_list = list(np.loadtxt(f'{catalogue_id}-spurious.dat', dtype=int))

    # Load catalogue.
    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}'
    catalogue_filename = f'{catalogue_id}.h5'

    with h5py.File(catalogue_filename, 'a') as hf:

        spurious_ids = [list(hf['photom/ID'][:]).index(id) for id in spurious_list]

        if 'spurious' in hf.keys():
            del hf['spurious']
            
        # True if spurious.
        hf['spurious'] = np.zeros(len(hf['photom/ID'][:]))
        hf['spurious'][spurious_ids] = 1