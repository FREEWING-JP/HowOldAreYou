# -*- coding: UTF-8 -*-

import os
import threading

import django.conf
import numpy as np

from HowOldWebsite.kernel.feature import do_collect_feature
from HowOldWebsite.kernel.feature import feature_extract_all
from HowOldWebsite.models import RecordFace
from HowOldWebsite.utils.image import do_imread
from .trainer_age import TrainerAge
from .trainer_sex import TrainerSex
from .trainer_smile import TrainerSmile

__author__ = 'Hao Yu'


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
    def __train_main(cls, model_names):
        SAVE_DIR = django.conf.settings.SAVE_DIR

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
            features = {}
            targets = {}
            threads = {}
            for m in model_names:
                features[m] = []
                targets[m] = []
                threads[m] = None

            trainers = {
                'sex': Trainer.__do_thread_train_sex,
                'age': Trainer.__do_thread_train_age,
                'smile': Trainer.__do_thread_train_smile,
            }

            # Extract feature
            for face in faces:
                face_id = face.id

                # Get image
                face_filename_color = os.path.join(SAVE_DIR['FACE'], str(face_id) + '.jpg')
                # face_filename_gray = os.path.join(SAVE_DIR['FACE_GRAY'], str(face_id) + '.jpg')
                cv_face_image = do_imread(face_filename_color)
                # face_gray = do_rgb2gray(cv_face_image)

                # Get features
                feature_single = feature_extract_all(cv_face_image)

                # Save features
                features = do_collect_feature(features, feature_single)

                # Get targets
                t = {}
                t['sex'] = (face.recordsex_set.first()).sex_user
                t['age'] = (face.recordage_set.first()).age_user
                t['smile'] = (face.recordsmile_set.first()).smile_user
                for m in model_names:
                    targets[m].append(t[m])
                    # targets['sex'].append(t_sex)
                    # targets['age'].append(t_age)
                    # targets['smile'].append(t_smile)

            for m in model_names:
                targets[m] = np.array(targets[m])
                # targets['sex'] = np.array(targets['sex'])
                # targets['age'] = np.array(targets['age'])
                # targets['smile'] = np.array(targets['smile'])

            # Train
            for m in model_names:
                threads[m] = threading.Thread(target=trainers[m],
                                              args=(n_faces, features, targets[m]))
                threads[m].start()
            for m in model_names:
                threads[m].join()

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

    @classmethod
    def __do_thread_train_sex(cls, n_faces, features, target):
        print("Sex Start")
        try:
            worker = TrainerSex()
            worker.train(n_faces, features, target)
        except Exception as e:
            print(e)
            pass
        print("Sex OK")

    @classmethod
    def __do_thread_train_age(cls, n_faces, features, target):
        print("Age Start")
        try:
            worker = TrainerAge()
            worker.train(n_faces, features, target)
        except Exception as e:
            print(e)
            pass
        print("Age OK")

    @classmethod
    def __do_thread_train_smile(cls, n_faces, features, target):
        print("Smile Start")
        try:
            worker = TrainerSmile()
            worker.train(n_faces, features, target)
        except Exception as e:
            print(e)
            pass
        print("Smile OK")
