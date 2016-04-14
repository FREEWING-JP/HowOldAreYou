# -*- coding: UTF-8 -*-

from HowOldWebsite.kernel import get_predictor
from HowOldWebsite.kernel import named_feature_combine
from HowOldWebsite.models import RecordSex

__author__ = 'Hao Yu'


def sex_estimate(database_face_array, feature_extracted_array):
    try:
        n_faces = len(database_face_array)
        result_sex_estimated = __do_estimate(feature_extracted_array, n_faces)
        database_sex_result = \
            __do_save_sex_to_database_all(database_face_array,
                                          result_sex_estimated)
        return True, database_sex_result
    except Exception as e:
        # print(e)
        return False, None


def __do_estimate(feature_jar, n_faces):
    feature_for_sex = []
    for ith in range(n_faces):
        feature_for_sex.append(
            named_feature_combine(feature_jar, combine_name='sex', ith=ith))
    sex_predictor = get_predictor('SEX')
    result = sex_predictor.predict(feature_for_sex)
    return result


def __do_save_sex_to_database_all(database_face, sex):
    database_sex = []
    for ith in range(len(database_face)):
        record = __do_save_sex_to_database(database_face[ith], sex[ith])
        database_sex.append(record)
    return database_sex


def __do_save_sex_to_database(face_record, sex_predict):
    database_record_sex = RecordSex(original_face=face_record,
                                    sex_predict=sex_predict)
    database_record_sex.save()
    return database_record_sex
