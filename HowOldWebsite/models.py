# -*- coding: UTF-8 -*-

from django.db import models


# ===== 数据库记录项 =====

class RecordOriginalImage(models.Model):
    # 原始大图片
    pass


class RecordFace(models.Model):
    # 检测出来的人脸
    pass


class RecordSex(models.Model):
    # 检测出来的性别
    pass


class RecordAge(models.Model):
    # 检测出来的年龄
    pass


class RecordSmile(models.Model):
    # 检测出来的微笑程度
    pass


# ===== 模型记录 =====

class ModelSex(models.Model):
    # 性别模型
    pass


class ModelAge(models.Model):
    # 年龄模型
    pass


class ModelSmile(models.Model):
    # 微笑模型
    pass
