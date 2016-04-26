# -*- coding: UTF-8 -*-

__author__ = 'Hao Yu'


class BaseFeature:
    extractor = None
    default_param = None

    @classmethod
    def extract(cls, pictures=None, params=None):
        return None

    @classmethod
    def extract_all(cls, picture=None, params=default_param):
        result = []
        for pic in picture:
            tmp_result = cls.extract(picture=pic, params=params)
            result.append([tmp_result])
        return result
