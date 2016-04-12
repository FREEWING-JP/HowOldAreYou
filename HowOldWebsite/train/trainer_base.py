# -*- coding: UTF-8 -*-

__author__ = 'haoyu'


class TrainerBase:
    def train(self, n_faces, feature_jar, target):
        pass

    def __do_train(self, n_faces, feature_jar, target):
        pass

    def __do_run_benchmark(self):
        pass

    def __do_save_to_database(self, accuracy):
        pass
