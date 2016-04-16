# -*- coding: UTF-8 -*-

import uuid

from django.db import models

__author__ = 'Hao Yu'

# ===== Picture Record =====

RecordUsedFlag = ((0, 'Never Used'),
                  (1, 'Available For Train'),
                  (2, 'Used For Train'))


class RecordOriginalImage(models.Model):
    # The original big image
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    upload_time = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True)
    source_url = models.URLField(blank=True)
    size_x = models.IntegerField(default=0)
    size_y = models.IntegerField(default=0)
    size_scale = models.BigIntegerField(default=0)
    used_flag = models.IntegerField(choices=RecordUsedFlag, default=0)


class RecordFace(models.Model):
    # The faces detected
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    original_image = models.ForeignKey(RecordOriginalImage, on_delete=models.CASCADE)
    detect_time = models.DateTimeField(auto_now_add=True)
    landmarks = models.TextField(blank=True)
    location_left = models.IntegerField(default=0)
    location_right = models.IntegerField(default=0)
    location_top = models.IntegerField(default=0)
    location_bottom = models.IntegerField(default=0)
    used_flag = models.IntegerField(choices=RecordUsedFlag, default=0)


RecordSexFlag = ((-1, 'Unknown'),
                 (0, 'Female'),
                 (1, 'Male'))


class RecordSex(models.Model):
    # The sexs of the faces detected
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    sex_predict = models.IntegerField(choices=RecordSexFlag, default=0)
    sex_user = models.IntegerField(choices=RecordSexFlag, blank=True, default=-1)
    used_flag = models.IntegerField(choices=RecordUsedFlag, default=0)


class RecordAge(models.Model):
    # The ages of the faces detected
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    age_predict = models.IntegerField(default=0)
    age_user = models.IntegerField(blank=True, default=-1)
    used_flag = models.IntegerField(choices=RecordUsedFlag, default=0)


class RecordSmile(models.Model):
    # The smile degrees of the faces detected
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    smile_predict = models.IntegerField(default=0)
    smile_user = models.IntegerField(blank=True, default=-1)
    used_flag = models.IntegerField(choices=RecordUsedFlag, default=0)


# ===== Model Record =====

ModelUsedFlag = ((0, 'Unused'),
                 (1, 'Using'))


class ModelSex(models.Model):
    # The Sex Model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    gen_time = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField(default=0)
    used_flag = models.IntegerField(choices=ModelUsedFlag, default=0)


class ModelAge(models.Model):
    # The Age Model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    gen_time = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField(default=0)
    used_flag = models.IntegerField(choices=ModelUsedFlag, default=0)


class ModelSmile(models.Model):
    # The Smile Model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    gen_time = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField(default=0)
    used_flag = models.IntegerField(choices=ModelUsedFlag, default=0)
