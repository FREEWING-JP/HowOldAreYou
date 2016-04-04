# -*- coding: UTF-8 -*-

__author__ = 'haoyu'


def result_arrange(arr_face,
                   arr_sex,
                   arr_age,
                   arr_smile):
    result = {}

    n_faces = len(arr_face)
    result['n_faces'] = n_faces

    result['faces'] = []

    for itr in range(n_faces):
        t_face = {}
        t_face['x1'] = arr_face[itr].location_x1
        t_face['x2'] = arr_face[itr].location_x2
        t_face['y1'] = arr_face[itr].location_y1
        t_face['y2'] = arr_face[itr].location_y2
        t_face = do_set_value(var=t_face, key='sex', subkey='value', value=arr_sex[itr].sex_predict)
        t_face = do_set_value(var=t_face, key='age', subkey='value', value=arr_age[itr].age_predict)
        t_face = do_set_value(var=t_face, key='smile', subkey='value', value=arr_smile[itr].smile_predict)

        result['faces'].append(t_face)

    return result


def do_set_value(var, key, subkey, value):
    if key not in var.keys():
        var[key] = {}
    if subkey not in var[key].keys():
        var[key][subkey] = {}
    var[key][subkey] = value

    return var
