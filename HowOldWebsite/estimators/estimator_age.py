# -*- coding: UTF-8 -*-


from HowOldWebsite.models import ModelAge
from .base_estimator import BaseEstimator

__author__ = 'Hao Yu'


class EstimatorAge(BaseEstimator):
    database_relation = ModelAge
    features_name = ['lbp', 'rbm']
