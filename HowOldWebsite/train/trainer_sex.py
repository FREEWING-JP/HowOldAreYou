# -*- coding: UTF-8 -*-

import copy
import os
import uuid

import numpy as np
from sklearn.externals import joblib

from HowOldAreYou.settings import SAVE_DIR
from HowOldWebsite.kernel import get_predictor
from HowOldWebsite.kernel import named_feature_combine
from HowOldWebsite.models import ModelSex
from .trainer_base import TrainerBase

__author__ = 'haoyu'


class TrainerSex(TrainerBase):
    def __init__(self):
        self.model_name = 'sex'
        self.model_id = uuid.uuid4()
        self.model_path = os.path.join(SAVE_DIR['MODEL'],
                                       'model_' + self.model_name.lower(),
                                       str(self.model_id))
        self.model_file_path = os.path.join(self.model_path,
                                            self.model_name.lower() + '.pkl')
        # Deep copy here
        self.model = copy.deepcopy(get_predictor(self.model_name.upper()))

    def train(self, n_faces, feature_jar, target):
        self.__do_train(n_faces, feature_jar, target)
        score = self.__do_run_benchmark()
        self.__do_save_to_database(score)

    def __do_train(self, n_faces, feature_jar, target):
        # Make feature
        feature = []
        for ith in range(n_faces):
            feature.append(
                named_feature_combine(feature_jar,
                                      combine_name=self.model_name,
                                      ith=ith))
        feature = np.array(feature)
        # Train
        self.model.fit(feature, target.ravel())

    def __do_run_benchmark(self):
        return 1

    def __do_save_to_database(self, accuracy):
        model = ModelSex(id=self.model_id,
                         accuracy=accuracy)
        os.mkdir(self.model_path)
        joblib.dump(self.model, self.model_file_path)

        model.save()
