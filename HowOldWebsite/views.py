# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

from .process_detect_face import face_detect
from .process_estimate_age import age_estimate
from .process_estimate_sex import sex_estimate
from .process_estimate_smile import smile_estimate
from .process_fetch_image import image_fetch
from .process_result_arrange import result_arrange


def index(request):
    return render(request, 'index.html')


def fisher(request):
    result = {}

    # check if in POST method
    if not request.method == "POST":
        return HttpResponse(json.dumps({'success': False,
                                        'message': 'Must in POST method',
                                        'tip': 'POST only'
                                        }))

    # print('Save The Image ...')
    result_upload, database_image_upload, cv_image_upload = image_fetch(request)
    if not result_upload:
        return HttpResponse(do_message_maker(success=False, message='Upload Failed', tip='JPG only'))
    result['image'] = database_image_upload

    # print('Detect Face ...')
    result_detect, database_face_detected = face_detect(database_image_upload, cv_image_upload)
    if not result_detect:
        return HttpResponse(do_message_maker(success=False, message='Face Detect Failed'))
    result['face'] = database_face_detected

    # print('Predict Sex ...')
    result_sex_estimate, database_sex_estimated = sex_estimate(database_face_detected)
    if not result_sex_estimate:
        return HttpResponse(do_message_maker(success=False, message='Sex Estimate Failed'))

    # print('Predict Age ...')
    result_age_estimate, database_age_estimated = age_estimate(database_face_detected, database_sex_estimated)
    if not result_age_estimate:
        return HttpResponse(do_message_maker(success=False, message='Age Estimate Failed'))

    # print('Predict Smile ...')
    result_smile_estimate, database_smile_estimated = smile_estimate(database_face_detected)
    if not result_smile_estimate:
        return HttpResponse(do_message_maker(success=False, message='Smile Estimate Failed'))

    # print('Done!')
    final_result = result_arrange(arr_face=database_face_detected,
                                  arr_sex=database_sex_estimated,
                                  arr_age=database_age_estimated,
                                  arr_smile=database_smile_estimated)
    # print(final_result)
    return HttpResponse(do_message_maker(success=True, message=str(final_result)))


def do_message_maker(success, message=None, tip=None):
    return json.dumps({'success': success,
                       'message': message,
                       'tip': tip
                       })
