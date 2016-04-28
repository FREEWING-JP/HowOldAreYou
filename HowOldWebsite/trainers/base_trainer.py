# -*- coding: UTF-8 -*-

import os
import uuid

import django.conf
from sklearn.externals import joblib

from HowOldWebsite.benchmarkers.base_benchmarker import BaseBenchmarker

__author__ = 'Hao Yu'


class BaseTrainer:
    def __init__(self, estimator):
        self.model = None
        self.model_id = uuid.uuid4()
        self.estimator = estimator
        self.model_name = self.estimator.get_estimator_name()
        self.model_path = os.path.join(django.conf.settings.SAVE_DIR['MODEL'],
                                       'model_' + self.model_name,
                                       str(self.model_id))

        self.model_file_path = os.path.join(self.model_path,
                                            self.model_name + '.pkl')

    def train(self, feature_jar, target):
        self.do_train(feature_jar, target)
        score = self.do_run_benchmark()
        self.do_save(score)

    def do_train(self, feature_jar, target):
        # Make feature
        feature = self.estimator.feature_combine(feature_jar)

        # Train
        self.model = self.estimator.train(feature, target)

    def do_run_benchmark(self):
        bm = BaseBenchmarker()
        score = bm.get_benchmark(model=self.model, model_name=self.model_name)
        return score

    def do_save(self, accuracy):
        # Save to disk
        os.mkdir(self.model_path)
        joblib.dump(self.model, self.model_file_path)

        # Save to database
        self.estimator.database_relation(id=self.model_id, accuracy=accuracy).save()
