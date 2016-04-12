# -*- coding: UTF-8 -*-

import numpy as np

from HowOldWebsite.kernel import get_predictor
from HowOldWebsite.models import RecordSmile

__author__ = 'haoyu'


def smile_estimate(database_face_array, feature_extracted_array):
    try:
        n_faces = len(database_face_array)
        result_smile_estimated = __do_estimate(feature_extracted_array, n_faces)
        database_smile_result = \
            __do_save_smile_to_database_all(database_face_array,
                                            result_smile_estimated)
        return True, database_smile_result
    except Exception as e:
        # print(e)
        return False, None


def __do_estimate(feature_jar, n_faces):
    feature_for_smile = []
    for ith in range(n_faces):
        feature_lbp_hog = feature_jar['lbp_hog'][ith]
        feature_landmark = feature_jar['landmark'][ith]
        feature_for_smile.append(np.concatenate((feature_lbp_hog,
                                                 feature_landmark)))
    smile_predictor = get_predictor('SMILE')
    result = smile_predictor.predict(feature_for_smile)
    return result


def __do_save_smile_to_database_all(database_face, smile):
    database_smile = []
    for ith in range(len(database_face)):
        record = __do_save_smile_to_database(database_face[ith], smile[ith])
        database_smile.append(record)
    return database_smile


def __do_save_smile_to_database(face_record, smile_predict):
    database_record_smile = RecordSmile(original_face=face_record,
                                        smile_predict=smile_predict)
    database_record_smile.save()
    return database_record_smile
