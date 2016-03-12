# -*- coding: UTF-8 -*-
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello Index!")


def result(request):
    return HttpResponse("Hello Result!")
