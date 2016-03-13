# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def fisher(request):
    print('Save The Image ...')
    print('Detect Face ...')
    print('Predict Sex ...')
    print('Predict Age ...')
    print('Predict Smile ...')
    return HttpResponse("Hello Index!")
