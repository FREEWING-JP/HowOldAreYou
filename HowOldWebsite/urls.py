# -*- coding: UTF-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^fisher$', views.result, name='result'),
]
