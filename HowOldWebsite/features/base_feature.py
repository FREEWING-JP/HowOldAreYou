# -*- coding: UTF-8 -*-

__author__ = 'Hao Yu'


class BaseFeature:
    extractor = None
    default_param = None
    layer = 'rgb'

    @classmethod
    def extract(cls, pictures=None, params=None):
        return None

    @classmethod
    def extract_all(cls, picture_jar=None, params=default_param):
        result = []
        if params is None:
            params = cls.default_param
        for pic in picture_jar[cls.layer]:
            tmp_result = cls.extract(picture=pic, params=params)
            result.append(tmp_result)
        return result
