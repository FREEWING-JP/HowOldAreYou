# -*- coding: UTF-8 -*-

from __future__ import print_function

from sklearn.externals import joblib


class Kernal:
    """
    The models, including the models for feature extracting and the
    models for predicting.
    """
    # To search the face
    __model_face_detector = None
    # To extract face landmark
    __model_feature_landmark = None
    # To extract aam feature
    __model_feature_aam = None
    # To extract deep feature from BernoulliRBM
    __model_feature_bernoulli_rbm = None
    # To extract deep feature from ConvNets
    __model_feature_conv_nets = None

    # Sex predictor
    __model_predict_sex = None
    # Age predictor
    __model_predict_age = None
    # Smile predictor
    __model_predict_smile = None

    __storage = {
        #
        'model_face_detector': __model_face_detector,
        #
        'model_feature_landmark': __model_feature_landmark,
        'model_feature_aam': __model_feature_aam,
        'model_feature_bernoulli_rbm': __model_feature_bernoulli_rbm,
        'model_feature_conv_nets': __model_feature_conv_nets,
        #
        'model_predict_sex': __model_predict_sex,
        'model_predict_age': __model_predict_age,
        'model_predict_smile': __model_predict_smile,
    }

    def load_data(self, model, path):
        try:
            Kernal.__storage[model] = joblib.load(path)
            print('Load {} done!'.format(model))
        except Exception as e:
            # print(e)
            print('Load {} error!'.format(model))
            pass

    def save_data(self, model, path):
        try:
            joblib.dump(Kernal.__storage[model], path)
            print('Save {} done!'.format(model))
        except Exception as e:
            # print(e)
            print('Save {} error!'.format(model))
            pass

    def get_instance(self, model):
        instance = None
        try:
            instance = Kernal.__storage[model]
        except Exception as e:
            # print(e)
            return instance
