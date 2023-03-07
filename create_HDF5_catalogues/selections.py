

import numpy as np
import h5py
import operator as op

from synthesizer.utils import flux_to_m, m_to_flux

# Have removed spurious for now as doesn't exist in catalogue until visual checks.
criteria = {}
criteria['F22'] = [
    ('pz/ceers/INT_ZGT7', op.gt, 0.7),
    ('pz/ceers/ZA', op.gt, 8.5),
    ('pz/ceers/CHIA', op.lt, 60),
    ('dchi2', op.gt, 4),
    ('nd_det', op.gt, 2),
    ('nd_opt3', op.eq, 0),
]


criteria['high-z.v0.1'] = [
    ('photom/FLUX_277', op.gt, m_to_flux(28.5)),
    ('pz/ceers/INT_ZGT4', op.gt, 0.9),
    ('pz/ceers/ZA', op.gt, 4.5),
    ('pz/ceers/CHIA', op.lt, 60),
    ('nd_det', op.gt, 4),
    ('nd_opt3', op.eq, 0),
]


class CEERS:

    """ selection criteria relevant for CEERS """

    def __init__(self, hf):

        self.hf = hf

        self.cat = {}

        self.p = hf['photom']  # photometry group
        self.pz = hf['pz/ceers']  # photometric redshift group

        self.za = self.pz['ZA'][:]

        # ---------------- ADD SELECTION CRITERIA HERE

        # --- calculate the signal-to-noise in each of the bands
        ai = 3  # aperture index
        sn = {f: hf['photom/FLUX_'+f+'_APER'][:, ai]/hf['photom/FLUXERR_'+f+'_APER'][:, ai]
              for f in ['606', '814', '115', '150', '200', '277', '356', '444']}

        # --- calculate the number of bands where S/N>5.5
        sn_det = np.array([sn[f] > 5.5
                           for f in ['115', '150', '200', '277', '356', '444']])  # for every galaxies this looks like [True, True, True, False, False, False] depending whether the condition is met.

        # this sums the above, i.e. True = 1, False = 0. Thus this tells us how many bands are detected at S/N>5.5
        self.cat['nd_det'] = np.sum(sn_det, axis=0)

        # --- calculate where S/N>3 to remove objects with detections in bands below the Lyman-break
        sn_opt3 = np.array([sn[f] > 3.0
                           for f in ['606', '814', '115', '150']])  # for every galaxies this looks like [True, True, True, False, False, False] depending whether the condition is met.

        # this sums the above, i.e. True = 1, False = 0. Thus this tells us how many bands are detected at S/N>5.5

        # -- for galaxies at z<9 we can ignore F814W THIS NEEDS CHECKING
        sn_opt3[1, (self.za < 8)] = 0.0
        sn_opt3[2, (self.za < 11)] = 0.0  # -- for galaxies at z<11 we can ignore F115W
        sn_opt3[3, (self.za < 12)] = 0.0  # -- for galaxies at z<12 we can ignore F150W

        self.cat['nd_opt3'] = np.sum(sn_opt3, axis=0)

        # --- calculate where S/N>3 to remove objects with detections in bands below the Lyman-break
        sn_opt2 = np.array([sn[f] > 2.0
                           for f in ['606', '814', '115', '150']])  # for every galaxies this looks like [True, True, True, False, False, False] depending whether the condition is met.

        # this sums the above, i.e. True = 1, False = 0. Thus this tells us how many bands are detected at S/N>5.5

        # -- for galaxies at z<9 we can ignore F814W THIS NEEDS CHECKING
        sn_opt2[1, (self.za < 8)] = 0.0
        sn_opt2[2, (self.za < 11)] = 0.0  # -- for galaxies at z<11 we can ignore F115W
        sn_opt2[3, (self.za < 12)] = 0.0  # -- for galaxies at z<12 we can ignore F150W

        self.cat['nd_opt2'] = np.sum(sn_opt2, axis=0)

        #CHI2_HI is not in the new catalogues. Using CHIA for now.
        self.cat['dchi2'] = self.pz['CHI2_LOW'][:] - self.pz['CHIA'][:]

        self.s_ = np.ones(len(self.za), dtype=bool)
        self.s = self.s_

    # def F22(self):
    #
    #     s = (self.pz['INT_ZGT7'][:] > 0.7)
    #     s = s & (self.za > 8.5)
    #     s = s & (self.pz['CHIA'][:] < 60)
    #     s = s & (self.cat['dchi2'] > 4)
    #     # ensure that objects detected in at least two relevant bands
    #     s = s & (self.cat['nd_det'] > 2)
    #     # ensure no objects are detected (at S/N>3) in the bands below the Lyman-break
    #     s = s & (self.cat['nd_opt3'] == 0)
    #
    #     self.s = s
    #
    #     return s

    def get_selection(self, criteria_list):

        self.criteria_list = criteria_list
        s = self.s_

        for criteria in criteria_list:
            p, op, c = criteria

            if p in self.cat.keys():

                s = s & op(self.cat[p], c)

            else:

                s = s & op(self.hf[p][:], c)

        self.s = s

        print(f'number of sources selected: {np.sum(s)}')

        return s

    def check_sources(self, ids):

        missing = list(set(ids) - set(self.p['ID'][self.s]))

        print('missing IDs:', missing)

        for id in missing:

            i = list(self.p['ID'][:]).index(id)

            print(self.p['ID'][i], '-'*10)

            for criteria in self.criteria_list:

                p, op, c = criteria

                if p in self.cat.keys():
                    value = self.cat[p][i]
                else:
                    value = self.hf[p][i]

                print(p, op, c, '|', f'{value:.2f}', op(value, c))