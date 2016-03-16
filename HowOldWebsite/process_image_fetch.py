# -*- coding: UTF-8 -*-
__author__ = 'haoyu'

from datetime import *
import uuid
import os

from .models import RecordOriginalImage
from HowOldAreYou.settings import BASE_DIR


def image_fetch(request):
    image_url = request.POST.get('ImageURL', '')
    image_file = request.FILES.getlist('file')
    if not image_url == '':
        return fetch_image_by_url(image_url, request)
    elif len(image_file) >= 1:
        return fetch_image_by_uploading(image_file, request)
    else:
        return False, False


def fetch_image_by_uploading(file, request):
    # print('Save image by upload')
    try:
        image_file = file[0]
        pic_id = uuid.uuid4()
        filename = str(pic_id) + '.jpg'
        upload_filename = os.path.join(BASE_DIR, "upload", "original_image", filename)
        with open(upload_filename, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        record_original_image = RecordOriginalImage(id=pic_id,
                                                    upload_time=datetime.today(),
                                                    source_url='USER UPLOAD',
                                                    user_ip=request.META['REMOTE_ADDR'],
                                                    size_x=0,
                                                    size_y=0,
                                                    size_scale=0,
                                                    used_flag=0
                                                    )
        record_original_image.save()
        return True, record_original_image
    except:
        return False, False


def fetch_image_by_url(url, request):
    # print('Save image by url')
    try:
        pic_id = uuid.uuid4()
        filename = str(pic_id) + '.jpg'
        upload_filename = os.path.join(BASE_DIR, "upload", "original_image", filename)
        record_original_image = RecordOriginalImage(id=pic_id,
                                                    upload_time=datetime.today(),
                                                    source_url=url,
                                                    user_ip=request.META['REMOTE_ADDR'],
                                                    size_x=0,
                                                    size_y=0,
                                                    size_scale=0,
                                                    used_flag=0
                                                    )
        record_original_image.save()
        return True, record_original_image
    except:
        return False, False
