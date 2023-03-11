import numpy as np
import h5py

from selection_criteria import CEERS, NGDEEP

def create_subcatalogue(survey, version, pointing, code):

    survey = survey.upper()
    survey_list = {'CEERS':CEERS, 'NGDEEP':NGDEEP}

    survey_dir = f'/Users/jt458/{survey.lower()}'

    subcat_name = f'-{code}'

    print(pointing, code)

    catalogue_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}.h5'
    new_catalogue_filename = f'{survey_dir}/cats/{survey}_NIRCam{pointing}_v{version}{subcat_name}.h5'

    with h5py.File(catalogue_filename, 'r') as hf:

        sel = survey_list[survey](hf)

        criteria_ = sel.criteria[code]

        s = sel.get_selection(criteria_)

        hfn = h5py.File(new_catalogue_filename, 'w')

        def make_copy(name, item):
            if isinstance(item, h5py.Dataset):
                # print(name)
                if name.split('/')[-1] == 'ZGRID':
                    hfn[name] = item[:]
                else:
                    hfn[name] = item[s]

        hf.visititems(make_copy)

        hfn.close()

#if __name__ == '__main__':

    #pointings = np.arange(1,11)
    #version = '0.51.2'
    #survey = 'CEERS'
    #code = 'high-z.v0.1'

    #for pointing in pointings:
        #create_subcatalogue(survey, version, pointing, code)