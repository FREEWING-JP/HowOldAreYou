# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

from .process_image_fetch import image_fetch
from .process_face_detect import face_detect


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
    result_upload, image_upload = image_fetch(request)
    if not result_upload:
        return HttpResponse(json.dumps({'success': False,
                                        'message': 'Upload Failed',
                                        'tip': 'JPG only'
                                        }))
    result['image'] = image_upload



    # print('Detect Face ...')
    result_detect, face_detected = face_detect(image_upload)
    if not result_detect:
        return HttpResponse(json.dumps({'success': False,
                                        'message': 'Face Detect Failed',
                                        'tip': None
                                        }))
    result['face'] = face_detected

    print('Predict Sex ...')
    print('Predict Age ...')
    print('Predict Smile ...')
    return HttpResponse("Hello, Fisher")
