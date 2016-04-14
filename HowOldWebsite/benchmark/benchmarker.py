# -*- coding: UTF-8 -*-

import os

import numpy as np
from sklearn.externals import joblib

from HowOldAreYou.settings import SAVE_DIR
from HowOldWebsite.kernel import named_feature_combine

__author__ = 'haoyu'


class Benchmarker:
    def __init__(self):
        self.__data_description = None
        self.__data_description_file_path = os.path.join(SAVE_DIR['STD_FACE_DESCRIPTION'], "how_old_data.pkl")
        # self.__data_face_path = SAVE_DIR['STD_FACE_IMAGE']
        self.__data_mat_file_path = SAVE_DIR['STD_FACE_MAT']

    def get_benchmark(self, model, model_name):
        if self.__data_description is None:
            self.__data_description = joblib.load(self.__data_description_file_path)

        features = []
        targets = []
        score = 0

        try:
            for item in self.__data_description:
                try:
                    pic_name = item[0]
                    mat_name = os.path.join(self.__data_mat_file_path, pic_name + '.pkl')
                    # feature_all = scipy.io.loadmat(mat_name)
                    image_info = joblib.load(mat_name)
                    if model_name == 'sex':
                        features.append(named_feature_combine(image_info['feature'], combine_name='sex', ith=0))
                        targets.append(image_info['sex'])
                    elif model_name == 'age':
                        features.append(named_feature_combine(image_info['feature'], combine_name='age', ith=0))
                        targets.append(image_info['age'])
                    elif model_name == 'smile':
                        features.append(named_feature_combine(image_info['feature'], combine_name='smile', ith=0))
                        targets.append(image_info['smile'])
                except Exception as e:
                    # print(e)
                    pass

            # Get the score
            features = np.array(features)
            score = model.score(features, targets)
        except Exception as e:
            # print(e)
            pass

        return score

    def __prepare(self):
        pass
