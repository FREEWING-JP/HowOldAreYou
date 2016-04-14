# -*- coding: UTF-8 -*-

import copy
import os
import uuid

from sklearn.externals import joblib

from HowOldAreYou.settings import SAVE_DIR
from HowOldWebsite.kernel import get_predictor
from HowOldWebsite.models import ModelAge
from .trainer_base import TrainerBase

__author__ = 'haoyu'


class TrainerAge(TrainerBase):
    def __init__(self):
        TrainerBase.__init__(self)
        self.model_name = 'age'
        self.model_id = uuid.uuid4()
        self.model_path = os.path.join(SAVE_DIR['MODEL'],
                                       'model_' + self.model_name.lower(),
                                       str(self.model_id))
        self.model_file_path = os.path.join(self.model_path,
                                            self.model_name.lower() + '.pkl')
        # Deep copy here
        self.model = copy.deepcopy(get_predictor(self.model_name.upper()))

    def do_save_to_database(self, accuracy):
        model = ModelAge(id=self.model_id,
                         accuracy=accuracy)
        os.mkdir(self.model_path)
        joblib.dump(self.model, self.model_file_path)

        model.save()
