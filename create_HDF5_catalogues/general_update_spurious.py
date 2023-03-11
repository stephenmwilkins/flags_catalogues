import numpy as np
import h5py

def update_spurious(survey, version, pointing):

    survey = survey.upper()
    survey_dir = f'/Users/jt458/{survey.lower()}'

    print('-'*30)
    print(pointing)

    catalogue_id = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}'

    catalogue_filename = f'{catalogue_id}.h5'

    spurious_list = list(np.loadtxt(f'{catalogue_id}-spurious.dat', dtype=int))

    with h5py.File(catalogue_filename, 'a') as hf:

        spurious_ids = [list(hf['photom/ID'][:]).index(id) for id in spurious_list]

        if 'spurious' in hf.keys():
            del hf['spurious']

        hf['spurious'] = np.zeros(len(hf['photom/ID'][:]))
        hf['spurious'][spurious_ids] = 1