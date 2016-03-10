# -*- coding: UTF-8 -*-

from django.db import models


# ===== 数据库记录项 =====

class RecordOriginalImage(models.Model):
    # 原始大图片
    id = models.UUIDField()
    upload_time = models.DateTimeField()
    user_ip = models.GenericIPAddressField()
    source_url = models.URLField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    size_scale = models.BigIntegerField()
    used_flag = models.IntegerField()


class RecordFace(models.Model):
    # 检测出来的人脸
    id = models.UUIDField()
    original_image = models.ForeignKey(RecordOriginalImage, on_delete=models.CASCADE)
    detect_time = models.DateTimeField()
    location_x = models.IntegerField()
    location_y = models.IntegerField()
    used_flag = models.IntegerField()


class RecordSex(models.Model):
    # 检测出来的性别
    id = models.UUIDField()
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    sex_predict = models.IntegerField()
    sex_user = models.IntegerField()
    used_flag = models.IntegerField()


class RecordAge(models.Model):
    # 检测出来的年龄
    id = models.UUIDField()
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    age_predict = models.IntegerField()
    age_user = models.IntegerField()
    used_flag = models.IntegerField()


class RecordSmile(models.Model):
    # 检测出来的微笑程度
    id = models.UUIDField()
    original_face = models.ForeignKey(RecordFace, on_delete=models.CASCADE)
    smile_predict = models.IntegerField()
    smile_user = models.IntegerField()
    used_flag = models.IntegerField()


# ===== 模型记录 =====

class ModelSex(models.Model):
    # 性别模型
    id = models.UUIDField()
    gen_time = models.DateTimeField()
    accuracy = models.DecimalField()
    used_flag = models.IntegerField()


class ModelAge(models.Model):
    # 年龄模型
    id = models.UUIDField()
    gen_time = models.DateTimeField()
    accuracy = models.DecimalField()
    used_flag = models.IntegerField()


class ModelSmile(models.Model):
    # 微笑模型
    id = models.UUIDField()
    gen_time = models.DateTimeField()
    accuracy = models.DecimalField()
    used_flag = models.IntegerField()
