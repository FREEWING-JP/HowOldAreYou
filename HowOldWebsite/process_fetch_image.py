# -*- coding: UTF-8 -*-

# import cv2
import os
import uuid

import skimage.io

from HowOldAreYou.settings import SAVE_DIR
from .models import RecordOriginalImage

__author__ = 'haoyu'


def image_fetch(request):
    # Generate the id and save path
    pic_id = uuid.uuid4()
    upload_filename = os.path.join(SAVE_DIR['ORIGINAL_IMAGE'], str(pic_id) + '.jpg')

    # There are two ways to get the image:
    # Uploading and URL
    image_url = request.POST.get('ImageURL', '')
    image_file = request.FILES.getlist('file')

    if not image_url == '':
        return do_fetch_image_by_url(
            image_url, request, pic_id, upload_filename)
    elif len(image_file) >= 1:
        return do_fetch_image_by_uploading(
            image_file, request, pic_id, upload_filename)
    else:
        return False, None


def do_fetch_image_by_uploading(file, request, pic_id, upload_filename):
    # print('Save image by upload')
    try:
        image_file = file[0]

        # Save the image to disk (NOTICE: now the image is in memory)
        with open(upload_filename, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        cv_image = skimage.io.imread(upload_filename)
        size_scale = os.path.getsize(upload_filename)
        record_original_image = \
            do_save_original_image_to_database(pic_id=pic_id,
                                               size_picture=cv_image.shape,
                                               request=request,
                                               method='UPLOAD',
                                               size_scale=size_scale)
        return True, record_original_image, cv_image
    except Exception as e:
        # print(e)
        return False, None, None


def do_fetch_image_by_url(url, request, pic_id, upload_filename):
    # print('Save image by url')
    try:
        # Todo: Do fetch image here

        cv_image = skimage.io.imread(upload_filename)
        size_scale = os.path.getsize(upload_filename)
        database_original_image = \
            do_save_original_image_to_database(pic_id=pic_id,
                                               size_picture=cv_image.shape,
                                               request=request,
                                               method='URL',
                                               size_scale=size_scale)

        return True, database_original_image, cv_image
    except Exception as e:
        # print(e)
        return False, None, None


def do_save_original_image_to_database(pic_id, size_picture, request, method, size_scale):
    # url = 'UNKNOW'
    if 'UPLOAD' == method:
        url = 'USER_UPLOAD'
    elif 'URL' == method:
        url = request.POST.get('ImageURL', '')
    else:
        url = 'UNKNOW'

    database_original_image = \
        RecordOriginalImage(id=pic_id,
                            user_ip=request.META['REMOTE_ADDR'],
                            source_url=url,
                            size_x=size_picture[1],
                            size_y=size_picture[0],
                            size_scale=size_scale
                            )
    database_original_image.save()

    return database_original_image
