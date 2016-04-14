# -*- coding: UTF-8 -*-

from django.contrib import admin

from .models import ModelAge
from .models import ModelSex
from .models import ModelSmile
from .models import RecordAge
from .models import RecordFace
from .models import RecordOriginalImage
from .models import RecordSex
from .models import RecordSmile

__author__ = 'Hao Yu'


# Record

class RecordOriginalImageAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['upload_time', 'used_flag']
    list_display = ('id', 'upload_time', 'size_x', 'size_y', 'user_ip', 'used_flag')


admin.site.register(RecordOriginalImage, RecordOriginalImageAdmin)


class RecordFaceAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['detect_time', 'used_flag']
    list_display = ('id', 'original_image', 'detect_time', 'used_flag')


admin.site.register(RecordFace, RecordFaceAdmin)


class RecordSexdmin(admin.ModelAdmin):
    fields = ['sex_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('id', 'original_face', 'sex_predict', 'sex_user', 'used_flag')


admin.site.register(RecordSex, RecordSexdmin)


class RecordAgeAdmin(admin.ModelAdmin):
    fields = ['age_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('id', 'original_face', 'age_predict', 'age_user', 'used_flag')


admin.site.register(RecordAge, RecordAgeAdmin)


class RecordSmileAdmin(admin.ModelAdmin):
    fields = ['smile_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('id', 'original_face', 'smile_predict', 'smile_user', 'used_flag')


admin.site.register(RecordSmile, RecordSmileAdmin)


# Model

class ModelSexAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')


admin.site.register(ModelSex, ModelSexAdmin)


class ModelAgeAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')


admin.site.register(ModelAge, ModelAgeAdmin)


class ModelSmileAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')


admin.site.register(ModelSmile, ModelSmileAdmin)
