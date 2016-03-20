# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    # favicon.ico
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    # the index page
    url(r'^$', views.index, name='index'),
    # the main processor
    url(r'^fisher$', views.fisher, name='fisher'),
]
