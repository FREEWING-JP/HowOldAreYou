# -*- coding: UTF-8 -*-

import os

import django.conf
import dlib
import numpy as np
import skimage.feature
from sklearn.externals import joblib

from HowOldWebsite.utils.image import do_rgb2gray

__author__ = 'Hao Yu'

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


def __do_lbp_hog(image_gray, P=8, R=1,
                 pixels_per_cell=(32, 32), cells_per_block=(2, 2)):
    feature_lbp = skimage.feature.local_binary_pattern(image_gray,
                                                       P=P, R=R,
                                                       method='nri_uniform')
    feature_lbp_hog = skimage.feature.hog(feature_lbp,
                                          pixels_per_cell=pixels_per_cell,
                                          cells_per_block=cells_per_block)
    return feature_lbp_hog.ravel()


def __do_lbp(image_gray, P=8, R=1):
    feature = skimage.feature.local_binary_pattern(image_gray,
                                                   P=P, R=R,
                                                   method='nri_uniform')
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


def __do_hog(image_gray, pixels_per_cell=(32, 32), cells_per_block=(2, 2)):
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


def feature_extract_all(image):
    image_gray = do_rgb2gray(image)

    feature = {}

    extractor_landmark = get_feature_extractor('LANDMARK')
    extractor_rbm = get_feature_extractor('RBM')
    extractor_hog = get_feature_extractor('HOG')
    extractor_lbp = get_feature_extractor('LBP')
    extractor_lbp_hog = get_feature_extractor('LBP_HOG')

    # Get features
    f_landmark = extractor_landmark(image_gray)
    f_rbm = extractor_rbm(image)
    f_hog = extractor_hog(image_gray)
    f_lbp = extractor_lbp(image_gray)
    f_lbp_hog = extractor_lbp_hog(image_gray)

    # Save features
    feature['landmark'] = [f_landmark]
    feature['rbm'] = [f_rbm]
    feature['hog'] = [f_hog]
    feature['lbp'] = [f_lbp]
    feature['lbp_hog'] = [f_lbp_hog]

    return feature


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
        return feature_combine(features, 'lbp', 'rbm', ith)
    elif 'smile' == combine_name:
        return feature_combine(features, 'lbp', 'landmark', ith)
    return None


def do_collect_feature(feature_jar, feature_single):
    for key in feature_single.keys():
        if key not in feature_jar.keys():
            feature_jar[key] = []

        feature_jar[key].append(feature_single[key][0])

    return feature_jar
