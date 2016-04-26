# -*- coding: UTF-8 -*-


from HowOldWebsite.estimators.estimator_age import EstimatorAge
from HowOldWebsite.models import RecordAge

__author__ = 'Hao Yu'


def age_estimate(database_face_array, database_age_array, feature_extracted_array):
    try:
        n_faces = len(database_face_array)
        result_age_estimated = __do_estimate(feature_extracted_array, n_faces)
        database_age_result = \
            __do_save_age_to_database_all(database_face_array, result_age_estimated)

        return True, database_age_result
    except Exception as e:
        # print(e)
        return False, None


def __do_estimate(feature_jar, n_faces):
    feature = EstimatorAge.feature_combine(feature_jar)
    feature = EstimatorAge.feature_reduce(feature)
    result = EstimatorAge.estimate(feature)
    return result


def __do_save_age_to_database_all(database_face, age):
    database_age = []
    for ith in range(len(database_face)):
        record = __do_save_sex_to_database(database_face[ith], age[ith])
        database_age.append(record)
    return database_age


def __do_save_sex_to_database(face_record, sex_predict):
    database_record_age = RecordAge(original_face=face_record,
                                    value_predict=sex_predict)
    database_record_age.save()
    return database_record_age
