# -*- coding: UTF-8 -*-
__author__ = 'haoyu'

import uuid
import os

import cv2

from .models import RecordOriginalImage
from HowOldAreYou.settings import SAVE_DIR


def image_fetch(request):
    image_url = request.POST.get('ImageURL', '')
    image_file = request.FILES.getlist('file')
    if not image_url == '':
        return do_fetch_image_by_url(image_url, request)
    elif len(image_file) >= 1:
        return do_fetch_image_by_uploading(image_file, request)
    else:
        return False


def do_fetch_image_by_uploading(file, request):
    # print('Save image by upload')
    try:
        image_file = file[0]
        pic_id = uuid.uuid4()
        upload_filename = os.path.join(SAVE_DIR['ORIGINAL_IMAGE'], str(pic_id) + '.jpg')

        # Save the image to disk (NOTICE: now the image is in memory)
        with open(upload_filename, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        record_original_image, cv_image = do_save_original_image_to_database(pic_id=pic_id,
                                                                             upload_filename=upload_filename,
                                                                             request=request,
                                                                             method='UPLOAD')
        return True, record_original_image, cv_image
    except Exception as e:
        # print(e)
        return False


def do_fetch_image_by_url(url, request):
    # print('Save image by url')
    try:
        pic_id = uuid.uuid4()
        upload_filename = os.path.join(SAVE_DIR['ORIGINAL_IMAGE'], str(pic_id) + '.jpg')

        # Todo: Do fetch image here
        record_original_image, cv_image = do_save_original_image_to_database(pic_id=pic_id,
                                                                             upload_filename=upload_filename,
                                                                             request=request,
                                                                             method='URL')

        return True, record_original_image, cv_image
    except:
        return False


def do_save_original_image_to_database(pic_id, upload_filename, request, method):
    cv_image = cv2.imread(upload_filename)

    url = 'UNKNOW'
    if 'UPLOAD' == method:
        url = 'USER_UPLOAD'
    elif 'URL' == method:
        url = request.POST.get('ImageURL', '')
    else:
        url = 'UNKNOW'

    record_original_image = RecordOriginalImage(id=pic_id,
                                                source_url=url,
                                                user_ip=request.META['REMOTE_ADDR'],
                                                size_x=cv_image.shape[1],
                                                size_y=cv_image.shape[0],
                                                size_scale=os.path.getsize(upload_filename)
                                                )
    record_original_image.save()

    return record_original_image, cv_image
