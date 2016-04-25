# -*- coding: UTF-8 -*-

import numpy as np

from HowOldWebsite.benchmark.benchmarker import Benchmarker
from HowOldWebsite.kernel.feature import named_feature_combine

__author__ = 'Hao Yu'


class BaseTrainer:
    def __init__(self):
        self.model_name = None
        self.model_id = None
        self.model_path = None
        self.model_file_path = None
        # Deep copy here
        self.model = None

    def train(self, n_faces, feature_jar, target):
        self.do_train(n_faces, feature_jar, target)
        score = self.do_run_benchmark()
        self.do_save_to_database(score)

    def do_train(self, n_faces, feature_jar, target):
        # Make feature
        feature = []
        for ith in range(n_faces):
            feature.append(
                named_feature_combine(feature_jar,
                                      combine_name=self.model_name,
                                      ith=ith))
        feature = np.array(feature)

        # Train
        self.model.set_params(verbose=1)
        self.model.fit(feature, target.ravel())
        self.model.set_params(verbose=0)

    def do_run_benchmark(self):
        bm = Benchmarker()
        score = bm.get_benchmark(model=self.model, model_name=self.model_name)
        return score

    def do_save_to_database(self, accuracy):
        pass
