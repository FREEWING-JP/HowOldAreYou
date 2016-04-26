# -*- coding: UTF-8 -*-

__author__ = 'Hao Yu'


def result_arrange(result_arr):
    result = dict()
    # Basic information
    result['pic_id'] = str(result_arr['raw_image'].id)
    result['n_faces'] = len(result_arr['face'])
    result['width'] = result_arr['raw_image'].size_x
    result['height'] = result_arr['raw_image'].size_y
    result['faces'] = []

    # Face information
    for itr in range(result['n_faces']):
        t_face = dict()
        t_arr_face = result_arr['face'][itr]

        # Face basic information
        t_face['id'] = str(t_arr_face.id)
        t_face['left'] = t_arr_face.location_left
        t_face['right'] = t_arr_face.location_right
        t_face['top'] = t_arr_face.location_top
        t_face['bottom'] = t_arr_face.location_bottom

        # Face estimation value
        t_face = __do_set_value(var=t_face, key='sex', subkey='value',
                                value=int(result_arr['sex'][itr].value_predict))
        t_face = __do_set_value(var=t_face, key='age', subkey='value',
                                value=float(result_arr['age'][itr].value_predict))
        t_face = __do_set_value(var=t_face, key='smile', subkey='value',
                                value=float(result_arr['smile'][itr].value_predict))

        result['faces'].append(t_face)

    # Save to database
    result_arr['raw_image'].save()
    for key in ['face', 'sex', 'age', 'smile']:
        for ith in range(result['n_faces']):
            result_arr[key][ith].save()

    return result


def __do_set_value(var, key, subkey, value):
    if key not in var.keys():
        var[key] = {}
    if subkey not in var[key].keys():
        var[key][subkey] = {}
    var[key][subkey] = value

    return var
