# -*- coding: UTF-8 -*-


from HowOldWebsite.models import ModelSex
from .base_estimator import BaseEstimator

__author__ = 'Hao Yu'


class EstimatorSex(BaseEstimator):
    database_relation = ModelSex
    features_name = ['hog', 'lbp_hog']
