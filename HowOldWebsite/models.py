# -*- coding: UTF-8 -*-

from django.db import models


# ===== 数据库记录项 =====

RecordUsedFlag = ((0, 'Never Used'),
                  (1, 'Available For Train'),
                  (2, 'Used For Train'))
ModelUsedFlag = ((0, 'Freeing'),
                 (1, 'Using'))


class RecordOriginalImage(models.Model):
    # 原始大图片
    id = models.UUIDField(primary_key=True)
    upload_time = models.DateTimeField()
    user_ip = models.GenericIPAddressField()
    source_url = models.URLField(blank=True)
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    size_scale = models.BigIntegerField()
    used_flag = models.IntegerField(choices=RecordUsedFlag)


class RecordFace(models.Model):
    # 检测出来的人脸
    id = models.UUIDField(primary_key=True)
    original_image = models.ForeignKey(RecordOriginalImage, on_delete=models.CASCADE)
    detect_time = models.DateTimeField()
    landmarks = models.TextField()
    location_x = models.IntegerField()
    location_y = models.IntegerField()
    used_flag = models.IntegerField(choices=RecordUsedFlag)


class RecordSex(models.Model):
    # 检测出来的性别
    id = models.UUIDField(primary_key=True)
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    sex_predict = models.IntegerField()
    sex_user = models.IntegerField(blank=True)
    used_flag = models.IntegerField(choices=RecordUsedFlag)


class RecordAge(models.Model):
    # 检测出来的年龄
    id = models.UUIDField(primary_key=True)
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    age_predict = models.IntegerField()
    age_user = models.IntegerField(blank=True)
    used_flag = models.IntegerField(choices=RecordUsedFlag)


class RecordSmile(models.Model):
    # 检测出来的微笑程度
    id = models.UUIDField(primary_key=True)
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    smile_predict = models.IntegerField()
    smile_user = models.IntegerField(blank=True)
    used_flag = models.IntegerField(choices=RecordUsedFlag)


# ===== 模型记录 =====

class ModelSex(models.Model):
    # 性别模型
    id = models.UUIDField(primary_key=True)
    gen_time = models.DateTimeField()
    accuracy = models.FloatField()
    used_flag = models.IntegerField(choices=ModelUsedFlag)


class ModelAge(models.Model):
    # 年龄模型
    id = models.UUIDField(primary_key=True)
    gen_time = models.DateTimeField()
    accuracy = models.FloatField()
    used_flag = models.IntegerField(choices=ModelUsedFlag)


class ModelSmile(models.Model):
    # 微笑模型
    id = models.UUIDField(primary_key=True)
    gen_time = models.DateTimeField()
    accuracy = models.FloatField()
    used_flag = models.IntegerField(choices=ModelUsedFlag)
