# -*- coding: UTF-8 -*-

from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

__author__ = 'Hao Yu'

urlpatterns = [
    # The favicon.ico file
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    # The index page
    url(r'^$', views.index, name='index'),
    # The main processor
    url(r'^fisher$', views.fisher, name='fisher'),
    # The feedback page
    url(r'^feedback$', views.feedback, name='feedback'),
    # The review page
    url(r'^review$', views.review, name='review'),
    # The review data page
    url(r'^review_data$', views.review_data, name='review_data'),

    # Example: the online training
    url(r'^train$', views.train, name='train')
]
