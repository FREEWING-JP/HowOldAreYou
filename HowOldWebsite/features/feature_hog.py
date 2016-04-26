# -*- coding: UTF-8 -*-


import skimage
import skimage.feature

from .base_feature import BaseFeature

__author__ = 'Hao Yu'


class FeatureHog(BaseFeature):
    extractor = skimage.feature.hog
    default_param = {
        'pixels_per_cell': (32, 32),
        'cells_per_block': (2, 2),
    }
    layer = 'gray'

    @classmethod
    def extract(cls, picture=None, params=default_param):
        feature = cls.extractor(picture,
                                pixels_per_cell=params['pixels_per_cell'],
                                cells_per_block=params['cells_per_block'])

        return feature.ravel()
