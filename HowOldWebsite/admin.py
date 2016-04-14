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
    list_display = ('__str__', 'detect_time', 'used_flag')


admin.site.register(RecordFace, RecordFaceAdmin)


class RecordSexAdmin(admin.ModelAdmin):
    fields = ['sex_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('__str__', 'sex_predict', 'sex_user', 'used_flag')
    actions = None


admin.site.register(RecordSex, RecordSexAdmin)


class RecordAgeAdmin(admin.ModelAdmin):
    fields = ['age_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('__str__', 'age_predict', 'user_report', 'used_flag')
    actions = None

    def user_report(self, obj):
        if obj.age_user == -1:
            return ""
        return str(obj.age_user)

    user_report.admin_order_field = 'age_user'


admin.site.register(RecordAge, RecordAgeAdmin)


class RecordSmileAdmin(admin.ModelAdmin):
    fields = ['smile_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('__str__', 'smile_predict', 'user_report', 'used_flag')
    actions = None

    def user_report(self, obj):
        if obj.smile_user == -1:
            return ""
        return str(obj.smile_user)

    user_report.admin_order_field = 'smile_user'


admin.site.register(RecordSmile, RecordSmileAdmin)


# Model

def model_make_active(modeladmin, request, queryset):
    queryset.update(used_flag=1)


model_make_active.short_description = "Active Selected Model"


def model_make_disactive(modeladmin, request, queryset):
    queryset.update(used_flag=0)


model_make_disactive.short_description = "Disactive Selected Model"


class ModelSexAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')

    actions = [model_make_active, model_make_disactive]


admin.site.register(ModelSex, ModelSexAdmin)


class ModelAgeAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')
    actions = [model_make_active, model_make_disactive]


admin.site.register(ModelAge, ModelAgeAdmin)


class ModelSmileAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')
    actions = [model_make_active, model_make_disactive]


admin.site.register(ModelSmile, ModelSmileAdmin)
