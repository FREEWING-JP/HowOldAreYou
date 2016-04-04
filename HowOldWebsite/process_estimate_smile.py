# -*- coding: UTF-8 -*-

__author__ = 'haoyu'

import numpy as np

from .models import RecordSmile


def smile_estimate(database_face_array):
    n_faces = len(database_face_array)
    feature_faces = []

    # Make the feature matrix
    for i_face in range(n_faces):
        single_face_feature = do_feature_extract(database_face_array[i_face])
        feature_faces.append(single_face_feature)

    # Do the estimation
    result_estimate = do_estimate(feature_faces)

    # Arrange the results
    database_result = do_arrange_result(database_face_array, result_estimate)

    return True, database_result


def do_feature_extract(img):
    try:
        pass
    except Exception as e:
        # print(e)
        return False

    return [1, 2, 3, 4, 5]


def do_estimate(feature):
    try:
        n_samples = len(feature)
        result = np.ones(n_samples)
    except Exception as e:
        # print(e)
        return False

    return result


def do_arrange_result(face_array, age_estimate):
    database_result = []
    for ith in range(len(face_array)):
        database_result_single = do_save_smile(face_array[ith], age_estimate[ith])
        database_result.append(database_result_single)
    return database_result


def do_save_smile(face_record, smile_predict):
    database_record_smile = RecordSmile(original_face=face_record,
                                        smile_predict=smile_predict)
    database_record_smile.save()
    return database_record_smile
