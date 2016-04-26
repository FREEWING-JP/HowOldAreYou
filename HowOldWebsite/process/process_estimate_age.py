# -*- coding: UTF-8 -*-


from HowOldWebsite.estimators.estimator_age import EstimatorAge
from HowOldWebsite.models import RecordAge

__author__ = 'Hao Yu'


def age_estimate(database_face_array, feature_jar):
    success = False
    database_record = None

    try:
        n_faces = len(database_face_array)
        result_estimated = __do_estimate(feature_jar, n_faces)
        database_record = \
            __do_save_to_database(database_face_array, result_estimated)
        success = True
    except Exception as e:
        # print(e)
        pass

    return success, database_record


def __do_estimate(feature_jar, n_faces):
    feature = EstimatorAge.feature_combine(feature_jar)
    feature = EstimatorAge.feature_reduce(feature)
    result = EstimatorAge.estimate(feature)
    return result


def __do_save_to_database(database_face, age):
    database_record = []
    for ith in range(len(database_face)):
        record = RecordAge(original_face=database_face[ith],
                           value_predict=age[ith])
        database_record.append(record)
    return database_record
