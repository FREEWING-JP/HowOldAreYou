# -*- coding: UTF-8 -*-

import os
import threading

import django.conf
import numpy as np

from HowOldWebsite.kernel import get_feature_extractor
from HowOldWebsite.models import RecordFace
from HowOldWebsite.utils import do_imread
from HowOldWebsite.utils import do_rgb2gray
from .trainer_age import TrainerAge
from .trainer_sex import TrainerSex
from .trainer_smile import TrainerSmile

__author__ = 'haoyu'


class Trainer:
    __busy = False

    # __threads = []

    @classmethod
    def is_busy(cls):
        return Trainer.__busy

    @classmethod
    def train(cls, request):
        if Trainer.is_busy():
            return False

        Trainer.__busy = True

        # Is it OK?
        th = threading.Thread(target=Trainer.__train_main, args=(request,))
        th.start()

        return True

    @classmethod
    def __train_main(cls, request):
        SAVE_DIR = django.conf.settings.SAVE_DIR
        if_train_sex = False
        if_train_age = False
        if_train_smile = False
        if "POST" == request.method:
            if_train_sex = request.POST.get('sex', '')
            if_train_age = request.POST.get('age', '')
            if_train_smile = request.POST.get('smile', '')

        if "GET" == request.method:
            if_train_sex = request.GET.get('sex', '')
            if_train_age = request.GET.get('age', '')
            if_train_smile = request.GET.get('smile', '')

        print("=" * 10 + " Train Start " + "=" * 10)

        try:
            faces = RecordFace.objects.filter(used_flag=1)
            n_faces = len(faces)
            if not django.conf.settings.DEBUG:
                if (n_faces < 100):
                    print("Error: The training set is too small.")
                    print("\t Skip the training!")
                    raise Exception()

            # The result array
            features = {
                'landmark': [],
                'rbm': [],
                'hog': [],
                'lbp': [],
                'lbp_hog': [],
            }
            target_sex = []
            target_age = []
            target_smile = []

            # Get the feature extractors
            extractor_landmark = get_feature_extractor('LANDMARK')
            extractor_rbm = get_feature_extractor('RBM')
            extractor_hog = get_feature_extractor('HOG')
            extractor_lbp = get_feature_extractor('LBP')
            extractor_lbp_hog = get_feature_extractor('LBP_HOG')

            # Extract feature
            for face in faces:
                face_id = face.id

                # Get image
                face_filename_color = os.path.join(SAVE_DIR['FACE'], str(face_id) + '.jpg')
                # face_filename_gray = os.path.join(SAVE_DIR['FACE_GRAY'], str(face_id) + '.jpg')
                cv_face_image = do_imread(face_filename_color)
                face_gray = do_rgb2gray(cv_face_image)

                # Get features
                f_landmark = extractor_landmark(face_gray)
                f_rbm = extractor_rbm(cv_face_image)
                f_hog = extractor_hog(face_gray)
                f_lbp = extractor_lbp(face_gray)
                f_lbp_hog = extractor_lbp_hog(face_gray)

                # Save features
                features['landmark'].append(f_landmark)
                features['rbm'].append(f_rbm)
                features['hog'].append(f_hog)
                features['lbp'].append(f_lbp)
                features['lbp_hog'].append(f_lbp_hog)

                # Get targets
                t_sex = (face.recordsex_set.first()).sex_user
                t_age = (face.recordage_set.first()).age_user
                t_smile = (face.recordsmile_set.first()).smile_user
                target_sex.append(t_sex)
                target_age.append(t_age)
                target_smile.append(t_smile)

            target_sex = np.array(target_sex)
            target_age = np.array(target_age)
            target_smile = np.array(target_smile)

            # Train
            if if_train_sex in [True, 'true', '1']:
                try:
                    worker = TrainerSex()
                    worker.train(n_faces, features, target_sex)
                except Exception as e:
                    # print(e)
                    pass

            if if_train_age in [True, 'true', '1']:
                try:
                    worker = TrainerAge()
                    worker.train(n_faces, features, target_age)
                except Exception as e:
                    # print(e)
                    pass

            if if_train_smile in [True, 'true', '1']:
                try:
                    worker = TrainerSmile()
                    worker.train(n_faces, features, target_smile)
                except Exception as e:
                    # print(e)
                    pass

            # Change the used flag
            if not django.conf.settings.DEBUG:
                faces.update(used_flag=2)

        except Exception as e:
            # print(e)
            print("Error occurred while training")
            pass

        print("=" * 10 + " Train Finish " + "=" * 10)

        # Set the busy flag
        Trainer.__busy = False
