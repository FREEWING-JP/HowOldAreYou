# -*- coding: UTF-8 -*-

import copy
import os
import uuid

import django.conf
from sklearn.externals import joblib

from HowOldWebsite.kernel.predictor import get_predictor
from HowOldWebsite.models import ModelSex
from .base_trainer import BaseTrainer

__author__ = 'Hao Yu'


class TrainerSex(BaseTrainer):
    def __init__(self):
        BaseTrainer.__init__(self)
        self.model_name = 'sex'
        self.model_id = uuid.uuid4()
        self.model_path = os.path.join(django.conf.settings.SAVE_DIR['MODEL'],
                                       'model_' + self.model_name.lower(),
                                       str(self.model_id))
        self.model_file_path = os.path.join(self.model_path,
                                            self.model_name.lower() + '.pkl')
        # Deep copy here
        self.model = copy.deepcopy(get_predictor(self.model_name.upper()))

    def do_save_to_database(self, accuracy):
        model = ModelSex(id=self.model_id, accuracy=accuracy)
        os.mkdir(self.model_path)
        joblib.dump(self.model, self.model_file_path)

        model.save()
