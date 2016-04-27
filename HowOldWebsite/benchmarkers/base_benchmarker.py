# -*- coding: UTF-8 -*-

import os

import django.conf
import numpy as np
from sklearn.externals import joblib

from HowOldWebsite.utils.language import reflect_get_class

__author__ = 'Hao Yu'


class BaseBenchmarker:
    data_description = None
    feature_jar = dict()
    target_jar = dict()

    @classmethod
    def load_std_data(cls):
        if cls.data_description is not None:
            return

        # Description file
        description_path = os.path.join(django.conf.settings.SAVE_DIR['STD_FACE_DESCRIPTION'],
                                        "how_old_data.pkl")
        cls.data_description = joblib.load(description_path)

        # Data file path
        data_file_path = django.conf.settings.SAVE_DIR['STD_FACE_MAT']

        debug_counter = 0
        for item in cls.data_description:
            debug_counter += 1
            if debug_counter >= 10:
                break
            try:
                pic_name = item[0]
                single_data_file = os.path.join(data_file_path, pic_name + '.pkl')
                single_data = joblib.load(single_data_file)

                for key in single_data['feature'].keys():
                    if key not in cls.feature_jar.keys():
                        cls.feature_jar[key] = []
                    cls.feature_jar[key].append(single_data['feature'][key][0])

                for key in single_data['target'].keys():
                    if key not in cls.target_jar.keys():
                        cls.target_jar[key] = []
                    cls.target_jar[key].append(single_data['target'][key][0])

            except Exception as e:
                # print(e)
                pass

    @classmethod
    def get_benchmark(cls, model, model_name):
        cls.load_std_data()

        score = 0

        try:
            # Get class
            class_name = 'HowOldWebsite.estimators.estimator_{}.Estimator{}'.format(model_name.lower(),
                                                                                    model_name.capitalize())
            obj_class = reflect_get_class(class_name)

            # Get score
            features = obj_class.feature_combine(cls.feature_jar)
            features = np.array(features)
            score = model.score(features, cls.target_jar[model_name.lower()])
        except Exception as e:
            # print(e)
            pass

        return score
