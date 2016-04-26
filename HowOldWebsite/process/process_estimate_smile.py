# -*- coding: UTF-8 -*-


from HowOldWebsite.estimators.estimator_smile import EstimatorSmile
from HowOldWebsite.models import RecordSmile

__author__ = 'Hao Yu'


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
    feature = EstimatorSmile.feature_combine(feature_jar)
    feature = EstimatorSmile.feature_reduce(feature)
    result = EstimatorSmile.estimate(feature)
    return result


def __do_save_smile_to_database_all(database_face, smile):
    database_smile = []
    for ith in range(len(database_face)):
        record = __do_save_smile_to_database(database_face[ith], smile[ith])
        database_smile.append(record)
    return database_smile


def __do_save_smile_to_database(face_record, smile_predict):
    database_record_smile = RecordSmile(original_face=face_record,
                                        value_predict=smile_predict)
    database_record_smile.save()
    return database_record_smile
