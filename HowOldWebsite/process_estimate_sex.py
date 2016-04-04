# -*- coding: UTF-8 -*-

__author__ = 'haoyu'

import os

from HowOldAreYou.settings import SAVE_DIR
from .models import RecordSex
from .utils import do_imread
from .utils import do_rgb2gray


def sex_estimate(database_face_array):
    database_result = []
    for face_record in database_face_array:
        result_estimate, database_sex_estimated = do_sex_estimate_single(face_record)
        database_result.append(database_sex_estimated)
    return True, database_result


def do_sex_estimate_single(face_record):
    # Read the face image
    img = do_imread(os.path.join(SAVE_DIR['FACE'], str(face_record.id) + '.jpg'));

    # Change the image to gray
    img_gray = do_rgb2gray(img)

    # Generate feature
    result_feature, data_feature = do_feature_extract(img_gray)
    # if not result_feature:
    #     return False

    # Do predict
    result_predict, data_predict = do_estimate(data_feature)
    # if not result_predict:
    #     return False
    database_record_sex = do_save_sex(face_record, data_predict)

    return True, database_record_sex


def do_feature_extract(img):
    try:
        pass
    except Exception as e:
        # print(e)
        return False

    return True, [1, 2, 3, 4, 5]


def do_estimate(feature):
    try:
        pass
    except Exception as e:
        # print(e)
        return False

    return True, 1


def do_save_sex(face_record, sex_predict):
    database_record_sex = RecordSex(original_face=face_record,
                                    sex_predict=sex_predict)
    database_record_sex.save()
    return database_record_sex
