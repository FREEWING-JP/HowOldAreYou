# -*- coding: UTF-8 -*-

import os

import django.conf
from sklearn.externals import joblib

from HowOldWebsite.models import ModelAge
from HowOldWebsite.models import ModelSex
from HowOldWebsite.models import ModelSmile

__author__ = 'Hao Yu'

# The paths
__paths = {
    'MODEL_AGE': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'model_age'),
    'MODEL_SEX': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'model_sex'),
    'MODEL_SMILE': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'model_smile'),
    'FEATURE_LANDMARK': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'feature_landmark'),
    'FEATURE_RBM': os.path.join(django.conf.settings.SAVE_DIR['MODEL'], 'feature_rbm'),
}

# The predictors

__map_predictor = {
    'SEX': None,
    'AGE': None,
    'SMILE': None,
}


def get_predictor(name, reload=False):
    name = name.upper()
    try:
        if (__map_predictor[name] is None) or (reload is True):
            __map_predictor[name] = load_predictor(name)
        return __map_predictor[name]
    except Exception as e:
        # print(e)
        return None


def load_predictor(model_name, model_id=None):
    '''
    If the id is not specified, we will find the model which is bing used or the
    newest, and read the id. Then we will load `/model/model_NAME/ID/NAME.pkl`.
    The default model will be load if there is no model on using.
    '''
    __model_classes = {
        'sex': ModelSex,
        'age': ModelAge,
        'smile': ModelSmile,
    }
    predictor = None

    try:
        if model_id is None:
            model_class = __model_classes[model_name.lower()]
            model_obj = model_class.objects.filter(used_flag=1).order_by('-gen_time').first()
            if model_obj is None:
                model_id = 'default'
            else:
                model_id = model_obj.id

        # Load the model
        path = os.path.join(__paths['MODEL_' + model_name.upper()], str(model_id), model_name.lower() + '.pkl')
        predictor = joblib.load(path)
    except Exception as e:
        # print(e)
        pass

    return predictor
