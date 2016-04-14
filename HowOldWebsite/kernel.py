# -*- coding: UTF-8 -*-

import os

import django.conf
import dlib
import numpy as np
import skimage.feature
from sklearn.externals import joblib

__author__ = 'haoyu'

# The paths
__paths = {
    'MODEL_AGE': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'model_age'),
    'MODEL_SEX': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'model_sex'),
    'MODEL_SMILE': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'model_smile'),
    'FEATURE_LANDMARK': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'feature_landmark'),
    'FEATURE_RBM': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'feature_rbm'),
}

# The rectangle in dlib
box = dlib.rectangle(left=0, top=0, right=255, bottom=255)

# The features

__doer = {
    'rbm': None
}


def __do_lbp_hog(image_gray, P=8, R=180,
                 pixels_per_cell=(16, 16), cells_per_block=(1, 1)):
    feature_lbp = skimage.feature.local_binary_pattern(image_gray, P, R)
    feature_lbp_hog = skimage.feature.hog(feature_lbp,
                                          pixels_per_cell=pixels_per_cell,
                                          cells_per_block=cells_per_block)
    return feature_lbp_hog.ravel()


def __do_lbp(image_gray, P=8, R=180):
    feature = skimage.feature.local_binary_pattern(image_gray, P=P, R=R)
    return feature.ravel()


def __do_landmark(image_gray):
    feature = []
    extractor = dlib.shape_predictor(
        os.path.join(__paths['FEATURE_LANDMARK'],
                     'face_landmark.dat'))
    landmarks = extractor(image_gray, box)
    for point in landmarks.parts():
        feature.append(point.x)
        feature.append(point.y)

    return np.array(feature).ravel()


def __do_hog(image_gray, pixels_per_cell=(16, 16), cells_per_block=(1, 1)):
    feature = skimage.feature.hog(image_gray,
                                  pixels_per_cell=pixels_per_cell,
                                  cells_per_block=cells_per_block)
    return feature.ravel()


def __do_rbm(image):
    if __doer['rbm'] is None:
        __doer['rbm'] = joblib.load(
            os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'feature_rbm', 'rbm.pkl'))
    doer = __doer['rbm']
    feature = doer.transform(image.reshape(1, -1))
    return feature[0].ravel()


__map_feature_extractor = {
    'LANDMARK': __do_landmark,
    'RBM': __do_rbm,
    'HOG': __do_hog,
    'LBP': __do_lbp,
    'LBP_HOG': __do_lbp_hog,
}


def get_feature_extractor(name):
    try:
        return __map_feature_extractor[name]
    except Exception as e:
        # print(e)
        return None


def feature_combine(features, name_feature1, name_feature2, ith):
    try:
        feature1 = features[name_feature1][ith]
        feature2 = features[name_feature2][ith]
        return np.concatenate((feature1, feature2))
    except Exception as e:
        # print(e)
        pass
    return None


def named_feature_combine(features, combine_name, ith):
    if 'sex' == combine_name:
        return feature_combine(features, 'hog', 'lbp_hog', ith)
    elif 'age' == combine_name:
        return feature_combine(features, 'lbp_hog', 'rbm', ith)
    elif 'smile' == combine_name:
        return feature_combine(features, 'lbp_hog', 'landmark', ith)
    return None


# The predictors

__map_predictor = {
    'SEX': None,
    'AGE': None,
    'SMILE': None,
}


def get_predictor(name):
    name = name.upper()
    try:
        if __map_predictor[name] is None:
            load_predictor(name)
        return __map_predictor[name]
    except Exception as e:
        # print(e)
        return None


def load_predictor(model_name, model_id=None):
    '''
    If the id is not specified, we will find the model which is bing used or the
    newest, and read the id.
    Then we will load /model/model_NAME/ID/NAME.pkl ,
    '''
    try:
        if model_id is None:
            # Todo: Find the newest model and read the id
            model_id = 'default'

        path = os.path.join(__paths['MODEL_' + model_name.upper()], str(model_id), model_name.lower() + '.pkl')
        __map_predictor[model_name] = joblib.load(path)
    except:
        pass
