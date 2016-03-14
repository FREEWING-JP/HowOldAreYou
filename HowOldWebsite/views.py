# -*- coding: UTF-8 -*-
from  datetime import *
import json
import uuid
import os

from django.http import HttpResponse
from django.shortcuts import render

from .models import RecordOriginalImage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request, 'index.html')


def fisher(request):
    if not request.method == "POST":
        response_data = {'success': False,
                         'message': 'Must in POST method'
                         }
        return HttpResponse(json.dumps(response_data))

    image_url = request.POST.get('ImageURL', '')
    image_file = request.FILES.getlist('file')

    # print('Save The Image ...')
    if not image_url == '':
        fetch_image_by_url(image_url, request)
    elif len(image_file) >= 1:
        fetch_image_by_uploading(image_file, request)
    else:
        response_data = {'success': False,
                         'message': 'No image'
                         }
        return HttpResponse(json.dumps(response_data))

    print('Detect Face ...')
    print('Predict Sex ...')
    print('Predict Age ...')
    print('Predict Smile ...')
    return HttpResponse("Hello Fisher!")


def fetch_image_by_uploading(file, request):
    # print('Save image by upload')
    pic_id = uuid.uuid4()
    os.path.join(BASE_DIR, "upload")
    image = file[0]
    record_original_image = RecordOriginalImage(id=pic_id,
                                                upload_time=datetime.today(),
                                                source_url='USER UPLOAD',
                                                user_ip=request.META['REMOTE_ADDR'],
                                                size_x=0,
                                                size_y=0,
                                                size_scale=0,
                                                used_flag=0
                                                )


def fetch_image_by_url(url, request):
    print('Save image by url')
    pic_id = uuid.uuid4()
    os.path.join(BASE_DIR, "upload")
    record_original_image = RecordOriginalImage(id=pic_id,
                                                upload_time=datetime.today(),
                                                source_url=url,
                                                user_ip=request.META['REMOTE_ADDR'],
                                                size_x=0,
                                                size_y=0,
                                                size_scale=0,
                                                used_flag=0
                                                )
