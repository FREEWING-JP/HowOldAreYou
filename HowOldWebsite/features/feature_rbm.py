# -*- coding: UTF-8 -*-

import os

import django.conf
from sklearn.externals import joblib

from .base_feature import BaseFeature

__author__ = 'Hao Yu'


class FeatureRbm(BaseFeature):
    extractor = joblib.load(
        os.path.join(django.conf.settings.SAVE_DIR['MODEL'],
                     'feature_rbm',
                     'rbm.pkl')
    )

    default_param = None

    @classmethod
    def extract(cls, picture=None, params=default_param):
        feature = cls.extractor.transform(picture.reshape(1, -1))

        return feature[0].ravel()
