import numpy as np
import h5py

from selection_criteria import CEERS, NGDEEP

def create_subcatalogue(survey, cat_version, pointing, code, survey_dir = ''):
    '''Create a subcatalogue based on one of the defined selction criteria'''

    survey = survey.upper()

    # List of surveys with available selection criteria.
    survey_list = {'CEERS':CEERS, 'NGDEEP':NGDEEP}

    # Identifier for the new subcatalogue.
    subcat_name = f'-{code}'
    new_catalogue_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}{subcat_name}.h5'

    # Load the full catalogue.
    catalogue_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{cat_version}.h5'
    with h5py.File(catalogue_filename, 'r') as hf:

        # Get the selection array.
        sel = survey_list[survey](hf)
        criteria_ = sel.criteria[code]
        s = sel.get_selection(criteria_)

        # Create new subcatalogue.
        hfn = h5py.File(new_catalogue_filename, 'w')

        def make_copy(name, item):
            if isinstance(item, h5py.Dataset):
                if name.split('/')[-1] == 'ZGRID': # Don't apply the selection within ZGRID. Just copy it.
                    hfn[name] = item[:]
                else:
                    hfn[name] = item[s]

        hf.visititems(make_copy)

        hfn.close()