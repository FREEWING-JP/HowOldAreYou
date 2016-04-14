# -*- coding: UTF-8 -*-

__author__ = 'Hao Yu'


def result_arrange(raw_image,
                   arr_face,
                   arr_sex,
                   arr_age,
                   arr_smile):
    result = {}

    n_faces = len(arr_face)
    result['pic_id'] = str(raw_image.id)
    result['n_faces'] = n_faces
    result['width'] = raw_image.size_x
    result['height'] = raw_image.size_y

    result['faces'] = []

    for itr in range(n_faces):
        t_face = {}
        t_face['id'] = str(arr_face[itr].id)
        t_face['left'] = arr_face[itr].location_left
        t_face['right'] = arr_face[itr].location_right
        t_face['top'] = arr_face[itr].location_top
        t_face['bottom'] = arr_face[itr].location_bottom
        t_face = __do_set_value(var=t_face, key='sex', subkey='value', value=int(arr_sex[itr].sex_predict))
        t_face = __do_set_value(var=t_face, key='age', subkey='value', value=float(arr_age[itr].age_predict))
        t_face = __do_set_value(var=t_face, key='smile', subkey='value', value=float(arr_smile[itr].smile_predict))

        result['faces'].append(t_face)

    return result


def __do_set_value(var, key, subkey, value):
    if key not in var.keys():
        var[key] = {}
    if subkey not in var[key].keys():
        var[key][subkey] = {}
    var[key][subkey] = value

    return var
