# -*- coding: UTF-8 -*-

from HowOldWebsite.utils.language import reflect_get_class


class FeatureUtil:
    @classmethod
    def __make_class_name(cls, feature_name):
        feature_name_split = feature_name.split('_')
        feature_name = ''.join([f.capitalize() for f in feature_name_split])
        feature_class_name = 'Feature{}'.format(feature_name)
        return feature_class_name

    @classmethod
    def __make_full_class_name(cls, feature_name):
        class_name = cls.__make_class_name(feature_name=feature_name)
        model_name = 'feature_{}'.format(feature_name.lower())
        full_class_name = 'HowOldWebsite.features.{}.{}'.format(model_name, class_name)
        return full_class_name

    @classmethod
    def extract(cls, feature_name, pic, params=None):
        object_class_name = cls.__make_full_class_name(feature_name=feature_name)
        object_class = reflect_get_class(object_class_name)
        feature = object_class.extract(picture=pic, params=params)
        return feature

    @classmethod
    def extract_all(cls, feature_name, pic_jar, params=None):
        object_class_name = cls.__make_full_class_name(feature_name=feature_name)
        object_class = reflect_get_class(object_class_name)
        features = object_class.extract_all(picture_jar=pic_jar, params=params)
        return features
