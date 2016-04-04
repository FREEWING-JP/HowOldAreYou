# -*- coding: UTF-8 -*-

__author__ = 'haoyu'

import numpy as np

from .models import RecordAge


def age_estimate(database_face_array, database_age_array):
    n_faces = len(database_face_array)
    feature_faces = []

    # Make the feature matrix
    for i_face in range(n_faces):
        single_face_feature = do_feature_extract(database_face_array[i_face])
        single_face_feature.extend([database_age_array[i_face].sex_predict])
        feature_faces.append(single_face_feature)

    # Do the estimation
    result_estimate = do_estimate(feature_faces)

    # Arrange the results
    database_result = do_arrange_result(database_face_array, result_estimate)

    # for face_record in database_face_array:
    #     result_estimate, database_age_estimated = do_age_estimate_single(face_record)
    #     database_result.append(database_age_estimated)
    return True, database_result


# def do_age_estimate_single(face_record):
#     # Read the face image
#     img = do_imread(os.path.join(SAVE_DIR['FACE'], str(face_record.id) + '.jpg'));
#
#     # Change the image to gray
#     img_gray = do_rgb2gray(img)
#
#     # Generate feature
#     result_feature, data_feature = do_feature_extract(img_gray)
#     # if not result_feature:
#     #     return False
#
#     # Do predict
#     result_predict, data_predict = do_estimate(data_feature)
#     # if not result_predict:
#     #     return False
#     database_record_age = do_save_age(face_record, data_predict)
#
#     return True, database_record_age


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
        database_result_single = do_save_age(face_array[ith], age_estimate[ith])
        database_result.append(database_result_single)
    return database_result


def do_save_age(face_record, sex_predict):
    database_record_age = RecordAge(original_face=face_record,
                                    age_predict=sex_predict)
    database_record_age.save()
    return database_record_age
