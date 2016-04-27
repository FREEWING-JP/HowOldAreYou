# -*- coding: UTF-8 -*-

import copy
import os
import shutil
import uuid

import django.conf
import numpy as np
from sklearn.externals import joblib

from HowOldWebsite.features.util_feature import UtilFeature

__author__ = 'Hao Yu'


class BaseEstimator:
    database_relation = None
    object_model = None
    features_name = []

    def __init__(self):
        pass

    # ==========     ==========     ==========
    # Helper
    # ==========     ==========     ==========
    @classmethod
    def get_estimator_name(cls):
        # name = self.__class__.__name__
        name = cls.__name__
        name = name.replace('Estimator', '')
        name = name.lower()
        return name

    # ==========     ==========     ==========
    # Feature
    # ==========     ==========     ==========

    @classmethod
    def feature_extract(cls, feature_jar, pic_jar):
        for key in cls.features_name:
            if key not in feature_jar.keys():
                features = UtilFeature.extract_all(key, pic_jar)
                feature_jar[key] = features
        return feature_jar

    @classmethod
    def feature_combine(cls, feature_jar):
        feature = []
        for ith in range(len(cls.features_name)):
            feature_single = feature_jar[cls.features_name[ith]]
            if ith == 0:
                feature = feature_single
                continue
            else:
                feature = np.concatenate((feature, feature_single), 1)

        return feature

    @classmethod
    def feature_reduce(cls, feature_combined):
        return feature_combined

    # ==========     ==========     ==========
    # Train
    # ==========     ==========     ==========

    @classmethod
    def train(cls, feature, target):
        """
            Train model
        """
        cls.estimator_load()
        model = copy.deepcopy(cls.object_model)
        model.set_params(verbose=1)
        model.fit(feature, target)
        model.set_params(verbose=0)
        return model

    # ==========     ==========     ==========
    # Estimate
    # ==========     ==========     ==========

    @classmethod
    def estimate(cls, feature):
        """
            Do estimations
        """
        cls.estimator_load()
        result = cls.object_model.predict(feature)
        return result

    @classmethod
    def estimator_load(cls, model_id=None, force=False):
        """
            Load estimator for class
        """
        if (cls.object_model is None) or force:
            cls.object_model = cls.estimator_get(model_id=model_id)
        return cls.object_model

    @classmethod
    def estimator_get(cls, model_id=None):
        """
            Load estimator from file
        """
        estimator = None
        try:
            if model_id is None:
                model_id = cls.database_model_get()
            estimator_name = cls.get_estimator_name()
            path = os.path.join(django.conf.settings.SAVE_DIR['MODEL'],
                                'model_' + estimator_name,
                                str(model_id),
                                estimator_name + '.pkl')
            estimator = joblib.load(path)
        except Exception as e:
            # print(e)
            pass

        return estimator

    # ==========     ==========     ==========
    # Database Model
    # ==========     ==========     ==========

    @classmethod
    def database_model_get(cls):
        model_id = None
        database_model = cls.database_relation.objects.filter(used_flag=1). \
            order_by('-gen_time').first()
        if database_model is None:
            model_id = 'default'
        else:
            model_id = database_model.id
        return model_id

    @classmethod
    def database_model_delete(cls, model_id):
        success = False
        model_uuid_id = None
        try:
            # Is defalut?
            assert model_id != 'default'

            # Is active?
            if (isinstance(model_id, uuid.UUID)):
                model_uuid_id = model_id
            else:
                model_uuid_id = uuid.UUID('urn:uuid:{}'.format(model_id))

            datase_object = cls.database_relation.objects.filter(id=model_uuid_id)
            assert datase_object is not None

            # assert datase_object.used_flag == 0

            # Delete it!
            datase_object.delete()
            estimator_name = cls.get_estimator_name()
            path = os.path.join(django.conf.settings.SAVE_DIR['MODEL'],
                                'model_' + estimator_name,
                                str(model_uuid_id))
            shutil.rmtree(path)
            success = True
        except Exception as e:
            pass

        return success
