# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    # The favicon.ico file
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    # The index page
    url(r'^$', views.index, name='index'),
    # The main processor
    url(r'^fisher$', views.fisher, name='fisher'),
    # The feedback page
    url(r'^feedback$', views.feedback, name='feedback'),
]
