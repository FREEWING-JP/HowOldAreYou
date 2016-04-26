# -*- coding: UTF-8 -*-


import skimage
import skimage.feature

from .base_feature import BaseFeature

__author__ = 'Hao Yu'


class FeatureLbpHog(BaseFeature):
    extractor = None
    default_param = {
        'P': 8,
        'R': 1,
        'method': 'nri_uniform',
        'pixels_per_cell': (32, 32),
        'cells_per_block': (2, 2),
    }

    @classmethod
    def extract(cls, picture=None, params=default_param):
        feature_lbp = skimage.feature.local_binary_pattern(picture,
                                                           P=params['P'],
                                                           R=params['R'],
                                                           method=params['method'])

        feature_lbp_hog = skimage.feature.hog(feature_lbp,
                                              pixels_per_cell=params['pixels_per_cell'],
                                              cells_per_block=params['cells_per_block'])
        return feature_lbp_hog.ravel()
