# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

from .process_detect_face import face_detect
from .process_estimate_sex import sex_estimate
from .process_fetch_image import image_fetch


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
    result_estimate, database_sex_estimated = sex_estimate(database_face_detected)
    if not result_estimate:
        return HttpResponse(do_message_maker(success=False, message='Sex Estimate Failed'))

    print('Predict Age ...')

    print('Predict Smile ...')

    print('Done!')
    return HttpResponse(do_message_maker(success=True, message='Hello, Fisher'))


def do_message_maker(success, message=None, tip=None):
    return json.dumps({'success': success,
                       'message': message,
                       'tip': tip
                       })
