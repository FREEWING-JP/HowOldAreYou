# -*- coding: UTF-8 -*-


import skimage
import skimage.feature

from .base_feature import BaseFeature

__author__ = 'Hao Yu'


class FeatureLbp(BaseFeature):
    extractor = skimage.feature.local_binary_pattern
    default_param = {
        'P': 8,
        'R': 1,
        'method': 'nri_uniform',
    }

    @classmethod
    def extract(cls, picture=None, params=default_param):
        feature = cls.extractor(picture,
                                P=params['P'],
                                R=params['R'],
                                method=params['method'])

        return feature.ravel()
