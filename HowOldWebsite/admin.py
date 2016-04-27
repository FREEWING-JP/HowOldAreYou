# -*- coding: UTF-8 -*-

import django.conf
from django.contrib import admin
from django.utils.html import format_html

from HowOldWebsite.utils.language import reflect_get_class
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
    list_display = ('img_show', 'detect_time', 'used_flag')

    def img_show(self, obj):
        s = u'<img src="{}face/{}.jpg" style="width:2em;height:2em">'
        return format_html(s, django.conf.settings.MEDIA_URL, str(obj.id))

    img_show.admin_order_field = 'image'


admin.site.register(RecordFace, RecordFaceAdmin)


class RecordSexAdmin(admin.ModelAdmin):
    fields = ['value_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('img_show', 'value_predict', 'value_user', 'used_flag')
    actions = None

    def img_show(self, obj):
        s = u'<img src="{}face/{}.jpg" style="width:2em;height:2em">'
        return format_html(s, django.conf.settings.MEDIA_URL, str(obj.original_face.id))

    img_show.admin_order_field = 'image'


admin.site.register(RecordSex, RecordSexAdmin)


class RecordAgeAdmin(admin.ModelAdmin):
    fields = ['value_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('img_show', 'value_predict', 'value_user', 'used_flag')
    actions = None

    def user_report(self, obj):
        if obj.age_user == -1:
            return ""
        return str(obj.age_user)

    user_report.admin_order_field = 'value_user'

    def img_show(self, obj):
        s = u'<img src="{}face/{}.jpg" style="width:2em;height:2em">'
        return format_html(s, django.conf.settings.MEDIA_URL, str(obj.original_face.id))

    img_show.admin_order_field = 'image'


admin.site.register(RecordAge, RecordAgeAdmin)


class RecordSmileAdmin(admin.ModelAdmin):
    fields = ['value_user', 'used_flag']
    list_filter = ['used_flag']
    list_display = ('img_show', 'value_predict', 'value_user', 'used_flag')
    actions = None

    def user_report(self, obj):
        if obj.smile_user == -1:
            return ""
        return str(obj.smile_user)

    user_report.admin_order_field = 'value_user'

    def img_show(self, obj):
        s = u'<img src="{}face/{}.jpg" style="width:2em;height:2em">'
        return format_html(s, django.conf.settings.MEDIA_URL, str(obj.original_face.id))

    img_show.admin_order_field = 'image'


admin.site.register(RecordSmile, RecordSmileAdmin)


# Model

def __model_reload(sample):
    # Get the estimator class
    model_name = sample.__class__.__name__
    model_name = model_name.replace('Model', '')
    estimator_name = 'HowOldWebsite.estimators.estimator_{}.Estimator{}'.format(model_name.lower(),
                                                                                model_name.capitalize())
    estimator_obj = reflect_get_class(estimator_name)

    # Reload
    estimator_obj.estimator_load(force=True)


def model_make_active(modeladmin, request, queryset):
    queryset.update(used_flag=1)
    __model_reload(queryset[0])


model_make_active.short_description = "Active Selected Model"


def model_make_disactive(modeladmin, request, queryset):
    queryset.update(used_flag=0)
    __model_reload(queryset[0])


model_make_disactive.short_description = "Disactive Selected Model"


def model_delete(modeladmin, request, queryset):
    # Get the estimator class
    sample = queryset[0]
    model_name = sample.__class__.__name__
    model_name = model_name.replace('Model', '')
    estimator_name = 'HowOldWebsite.estimators.estimator_{}.Estimator{}'.format(model_name.lower(),
                                                                                model_name.capitalize())
    estimator_obj = reflect_get_class(estimator_name)

    # Delete from disk
    for item in queryset:
        estimator_obj.database_model_delete(item.id)

    # Delete from database
    queryset.delete()

    # Reload
    estimator_obj.estimator_load(force=True)


model_delete.short_description = "Delete Selected Model [Danger]"


class ModelSexAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time', 'used_flag']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')
    actions = [model_make_active, model_make_disactive, model_delete]

    def get_actions(self, request):
        # Disable delete
        actions = super(ModelSexAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(ModelSex, ModelSexAdmin)


class ModelAgeAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time', 'used_flag']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')
    actions = [model_make_active, model_make_disactive, model_delete]

    def get_actions(self, request):
        # Disable delete
        actions = super(ModelAgeAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(ModelAge, ModelAgeAdmin)


class ModelSmileAdmin(admin.ModelAdmin):
    fields = ['used_flag']
    list_filter = ['gen_time', 'used_flag']
    list_display = ('id', 'gen_time', 'accuracy', 'used_flag')
    actions = [model_make_active, model_make_disactive, model_delete]

    def get_actions(self, request):
        # Disable delete
        actions = super(ModelSmileAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(ModelSmile, ModelSmileAdmin)
