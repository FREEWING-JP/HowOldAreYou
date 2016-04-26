# -*- coding: UTF-8 -*-


from HowOldWebsite.models import ModelSmile
from .base_estimator import BaseEstimator

__author__ = 'Hao Yu'


class EstimatorSmile(BaseEstimator):
    database_relation = ModelSmile
    features_name = ['lbp', 'landmark']
