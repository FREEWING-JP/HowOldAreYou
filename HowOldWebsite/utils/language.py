# -*- coding: UTF-8 -*-


__author__ = 'Hao Yu'


def reflect_get_class(class_full_name):
    parts = class_full_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
