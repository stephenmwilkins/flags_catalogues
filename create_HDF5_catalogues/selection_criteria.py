import numpy as np
import h5py
import operator as op
from synthesizer.utils import fnu_to_m, m_to_fnu

# Define a new class for each survey with the relevant selection criteria and functions.

class CEERS:

    """ selection criteria relevant for CEERS """

    def __init__(self, hf):

        self.hf = hf

        self.cat = {}

        self.p = hf['photom'] # Photmetry group
        self.pz = hf['pz/ceers'] # Photometric redshift group
        self.za = self.pz['ZA'][:]

        # ---------------- Define different criteria here ----------------
        self.criteria = {}
        self.criteria['F22'] = [
            ('pz/ceers/INT_ZGT7', op.gt, 0.7),
            ('pz/ceers/ZA', op.gt, 8.5),
            ('pz/ceers/CHIA', op.lt, 60),
            ('dchi2', op.gt, 4),
            ('nd_det', op.gt, 2),
            ('nd_opt3', op.eq, 0),
        ]
        self.criteria['CEERS_colours'] = [
            ('photom/FLUX_277', op.gt, 100),
            ('pz/ceers/INT_ZGT4', op.gt, 0.9),
            ('pz/ceers/ZA', op.gt, 4.5),
            ('pz/ceers/CHIA', op.lt, 60),
            ('nd_det', op.gt, 4),
            ('nd_opt3', op.eq, 0),
        ]

        self.criteria['CEERS_colours_v3'] = [
            ('photom/FLUX_277', op.gt, 50),
            ('pz/ceers/INT_ZGT4', op.gt, 0.9),
            ('pz/ceers/ZA', op.gt, 4.5),
            ('pz/ceers/CHIA', op.lt, 60),
            ('nd_det', op.gt, 4),
            ('nd_opt3', op.eq, 0),
        ]

        self.criteria['CEERS_colours_v4'] = [
            ('photom/FLUX_277', op.gt, 50),
            ('pz/ceers/INT_ZGT4', op.gt, 0.9),
            ('pz/ceers/ZA', op.gt, 4.5),
            ('pz/ceers/CHIA', op.lt, 60),
            ('nd_det', op.gt, 4),
            ('nd_opt2', op.eq, 0),
        ]

        # ---------------- Include calculations required for criteria here ----------------

        # --- calculate the signal-to-noise in each of the bands
        ai = 3  # aperture index
        sn = {f: hf['photom/FLUX_'+f+'_APER'][:, ai]/hf['photom/FLUXERR_'+f+'_APER'][:, ai]
              for f in ['606', '814', '115', '150', '200', '277', '356', '444']}
        
        self.cat['SN_277'] = hf['photom/FLUX_277_APER'][:, ai]/hf['photom/FLUXERR_277_APER'][:, ai]

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
        sn_opt3[0, (self.za < 6)] = 0.0
        sn_opt3[1, (self.za < 7)] = 0.0
        sn_opt3[2, (self.za < 9.9)] = 0.0  # -- for galaxies at z<11 we can ignore F115W
        sn_opt3[3, (self.za < 13.2)] = 0.0  # -- for galaxies at z<12 we can ignore F150W

        self.cat['nd_opt3'] = np.sum(sn_opt3, axis=0)

        # --- calculate where S/N>3 to remove objects with detections in bands below the Lyman-break
        sn_opt2 = np.array([sn[f] > 2.0
                           for f in ['606', '814', '115', '150']])  # for every galaxies this looks like [True, True, True, False, False, False] depending whether the condition is met.

        # this sums the above, i.e. True = 1, False = 0. Thus this tells us how many bands are detected at S/N>5.5

        # -- for galaxies at z<9 we can ignore F814W THIS NEEDS CHECKING
        sn_opt2[0, (self.za < 6)] = 0.0
        sn_opt2[1, (self.za < 7)] = 0.0
        sn_opt2[2, (self.za < 9.9)] = 0.0  # -- for galaxies at z<11 we can ignore F115W
        sn_opt2[3, (self.za < 13.2)] = 0.0  # -- for galaxies at z<12 we can ignore F150W

        self.cat['nd_opt2'] = np.sum(sn_opt2, axis=0)

        #CHI2_HI is not in the new catalogues. Using CHIA for now.
        self.cat['dchi2'] = self.pz['CHI2_LOW'][:] - self.pz['CHIA'][:]

        self.s_ = np.ones(len(self.za), dtype=bool)
        self.s = self.s_

# ---------------- Functions required for each survey ----------------

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

class NGDEEP:

    """ selection criteria relevant for NGDEEP """

    def __init__(self, hf):

        self.hf = hf

        self.cat = {}

        self.p = hf['photom']  # Photometry group
        self.pz = hf['pz/ngdeep']  # Photometric redshift group
        self.za = self.pz['ZA'][:]

        # ---------------- Define different criteria here ----------------
        self.criteria = {}
        self.criteria['high-z.v0.1'] = [
            ('photom/FLUX_277', op.gt, m_to_fnu(28.5)),
            ('pz/ngdeep/INT_ZGT4', op.gt, 0.9),
            ('pz/ngdeep/ZA', op.gt, 4.5),
            ('pz/ngdeep/CHIA', op.lt, 60),
            ('nd_det', op.gt, 4),
]
        # ---------------- Include calculations required for criteria here ----------------

        # --- calculate the signal-to-noise in each of the bands
        ai = 3  # aperture index
        sn = {f: hf['photom/FLUX_'+f+'_APER'][:, ai]/hf['photom/FLUXERR_'+f+'_APER'][:, ai]
              for f in ['814', '115', '150', '200', '277', '356', '444']}

        # --- calculate the number of bands where S/N>5.5
        sn_det = np.array([sn[f] > 5.5
                           for f in ['115', '150', '200', '277', '356', '444']])  # for every galaxies this looks like [True, True, True, False, False, False] depending whether the condition is met.

        # this sums the above, i.e. True = 1, False = 0. Thus this tells us how many bands are detected at S/N>5.5
        self.cat['nd_det'] = np.sum(sn_det, axis=0)

        #CHI2_HI is not in the new catalogues. Using CHIA for now.
        self.cat['dchi2'] = self.pz['CHI2_LOW'][:] - self.pz['CHIA'][:]

        self.s_ = np.ones(len(self.za), dtype=bool)
        self.s = self.s_

# ---------------- Functions required for each survey ----------------

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