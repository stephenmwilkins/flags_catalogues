import numpy as np

from convert_to_hdf5 import convert_to_hdf5
from match_pz import match_pz
from match_specz import match_specz
from create_subcatalogue import create_subcatalogue
from update_spurious import update_spurious
from selection_criteria import CEERS, NGDEEP

surveys = ['CEERS', 'NGDEEP']
survey_info = {'CEERS':['0.51.2', np.arange(1,11)], 'NGDEEP':['0.1', [1]]}

#surveys = ['NGDEEP']
#survey_info = {'NGDEEP':['0.1', [1]]}

for survey in surveys:
    print(survey)
    for pointing in survey_info[survey][1]:
        print(pointing)
        
        convert_to_hdf5(survey, survey_info[survey][0], pointing)

        match_pz(survey, survey_info[survey][0], pointing)

        match_specz(survey, survey_info[survey][0], pointing)

        create_subcatalogue(survey, survey_info[survey][0], pointing, 'high-z.v0.1')
