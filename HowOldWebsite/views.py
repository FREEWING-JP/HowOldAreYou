# -*- coding: UTF-8 -*-

import json
import uuid

from django.http import HttpResponse
from django.shortcuts import render

from HowOldWebsite.process.process_estimate_smile import smile_estimate
from HowOldWebsite.train.trainer import Trainer
from .models import RecordFace
from .models import RecordOriginalImage
from .process.process_detect_face import face_detect
from .process.process_estimate_age import age_estimate
from .process.process_estimate_sex import sex_estimate
from .process.process_fetch_image import image_fetch
from .process.process_result_arrange import result_arrange
from .utils import do_message_maker

__author__ = 'Hao Yu'


def index(request):
    howold_photos = RecordOriginalImage.objects.count()
    howold_faces = RecordFace.objects.count()
    context = {
        'how_old_show_statics': True,
        'howold_photos': howold_photos,
        'howold_faces': howold_faces,
    }
    return render(request, 'index.html', context)


def review(request):
    return render(request, 'review.html')


def review_data(request):
    how_old_face = RecordFace.objects.filter(used_flag=0).first()
    result = {}
    success = True
    try:
        how_old_sex = how_old_face.recordsex_set.first()
        how_old_age = how_old_face.recordage_set.first()
        how_old_smile = how_old_face.recordsmile_set.first()
        result['id'] = str(how_old_face.id)
        result['sex'] = how_old_sex.sex_predict
        result['age'] = how_old_age.age_predict
        result['smile'] = how_old_smile.smile_predict
    except Exception as e:
        # print(e)
        success = False
        pass

    return HttpResponse(
        do_message_maker(success=success,
                         message=result))


def fisher(request):
    result = {}

    # check if in POST method
    if not request.method == "POST":
        return HttpResponse(json.dumps({'success': False,
                                        'message': 'Must in POST method',
                                        'tip': 'POST only'
                                        }))

    # print('Save The Image ...')
    result_upload, database_image_upload, image_upload = \
        image_fetch(request)
    if not result_upload:
        return HttpResponse(
            do_message_maker(success=False,
                             message='Upload Failed',
                             tip='JPG only'))
    result['image'] = database_image_upload

    # print('Detect Face ...')
    result_detect, database_face_detected, feature_extracted = \
        face_detect(database_image_upload, image_upload)
    if not result_detect:
        return HttpResponse(
            do_message_maker(success=False,
                             message='Face Detect Failed'))
    result['face'] = database_face_detected

    # print('Predict Sex ...')
    result_sex_estimate, database_sex_estimated = \
        sex_estimate(database_face_detected,
                     feature_extracted)
    if not result_sex_estimate:
        return HttpResponse(
            do_message_maker(success=False,
                             message='Sex Estimate Failed'))

    # print('Predict Age ...')
    result_age_estimate, database_age_estimated = \
        age_estimate(database_face_detected,
                     database_sex_estimated,
                     feature_extracted)
    if not result_age_estimate:
        return HttpResponse(
            do_message_maker(success=False,
                             message='Age Estimate Failed'))

    # print('Predict Smile ...')
    result_smile_estimate, database_smile_estimated = \
        smile_estimate(database_face_detected,
                       feature_extracted)
    if not result_smile_estimate:
        return HttpResponse(
            do_message_maker(success=False,
                             message='Smile Estimate Failed'))

    # print('Done!')
    final_result = result_arrange(raw_image=database_image_upload,
                                  arr_face=database_face_detected,
                                  arr_sex=database_sex_estimated,
                                  arr_age=database_age_estimated,
                                  arr_smile=database_smile_estimated)
    # print(final_result)
    return HttpResponse(
        do_message_maker(success=True,
                         message=final_result))


def feedback(request):
    # check if in POST method
    if not request.method == "POST":
        return HttpResponse(json.dumps({'success': False,
                                        'message': 'Must in POST method',
                                        'tip': 'POST only'
                                        }))

    success = True
    try:
        # Get the parameters
        face_id = uuid.UUID(request.POST.get('face_id', ''))
        sex_user = int(request.POST.get('sex', ''))
        age_user = float(request.POST.get('age', ''))
        smile_user = float(request.POST.get('smile', ''))

        # Update into the database
        database_face = RecordFace.objects.get(id=face_id)
        database_face.recordsex_set.update(sex_user=sex_user)
        database_face.recordage_set.update(age_user=age_user)
        database_face.recordsmile_set.update(smile_user=smile_user)
        database_face.used_flag = 1
        database_face.save()
    except Exception as e:
        # print(e)
        success = False

    return HttpResponse(
        do_message_maker(success=success))


def train(request):
    train_models = []
    model_names = ['sex', 'age', 'smile']
    if "POST" == request.method:
        for mod in model_names:
            if request.POST.get(mod, '') in [True, "true", 1]:
                train_models.append(mod)

    if "GET" == request.method:
        for mod in model_names:
            if request.GET.get(mod, '') in [True, "true", 1]:
                train_models.append(mod)

    success = Trainer.train(train_models)
    return HttpResponse(
        do_message_maker(success=success))
