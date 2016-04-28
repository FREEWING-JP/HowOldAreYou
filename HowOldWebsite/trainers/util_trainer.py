# -*- coding: UTF-8 -*-

import os
import threading

import django.conf

from HowOldWebsite.models import RecordFace
from HowOldWebsite.utils.image import do_imread
from HowOldWebsite.utils.image import do_rgb2gray
from HowOldWebsite.utils.language import reflect_get_class

__author__ = 'Hao Yu'


class UtilTrainer:
    __busy = False

    # __threads = []

    @classmethod
    def is_busy(cls):
        return cls.__busy

    @classmethod
    def train(cls, request):
        if cls.is_busy():
            return False

        cls.__busy = True

        # Is it OK?
        th = threading.Thread(target=UtilTrainer.__train_main, args=(request,))
        th.start()

        return True

    @classmethod
    def __train_main(cls, model_names):
        model_names = [m.lower() for m in model_names]

        print("=" * 10 + " Train Start " + "=" * 10)

        try:
            faces = RecordFace.objects.filter(used_flag=1)
            if not django.conf.settings.DEBUG:
                if len(faces) < 100:
                    print("Error: The training set is too small.")
                    print("\t Skip the training!")
                    raise Exception()

            image_jar = dict()
            feature_jar = dict()
            target_jar = dict()
            estimator_jar = dict()
            threads = list()

            # Get estimator class
            for m in model_names:
                class_estimator = 'HowOldWebsite.estimators.estimator_{}.Estimator{}'.format(
                    m, m.capitalize()
                )
                estimator_jar[m] = reflect_get_class(class_estimator)

            for face in faces:
                face_id = face.id

                # Get image
                face_filename_color = os.path.join(
                    django.conf.settings.SAVE_DIR['FACE'],
                    str(face_id) + '.jpg'
                )
                # face_filename_gray = os.path.join(SAVE_DIR['FACE_GRAY'], str(face_id) + '.jpg')
                cv_face_image = do_imread(face_filename_color)
                cv_face_gray = do_rgb2gray(cv_face_image)
                if 'rgb' not in image_jar.keys():
                    image_jar['rgb'] = list()
                image_jar['rgb'].append(cv_face_image)
                if 'gray' not in image_jar.keys():
                    image_jar['gray'] = list()
                image_jar['gray'].append(cv_face_gray)

                # Get target
                if 'sex' not in target_jar.keys():
                    target_jar['sex'] = list()
                target_jar['sex'].append((face.recordsex_set.first()).value_user)

                if 'age' not in target_jar.keys():
                    target_jar['age'] = list()
                target_jar['age'].append((face.recordage_set.first()).value_user)

                if 'smile' not in target_jar.keys():
                    target_jar['smile'] = list()
                target_jar['smile'].append((face.recordsmile_set.first()).value_user)

            # Extract features
            for m in model_names:
                feature_jar = estimator_jar[m].feature_extract(feature_jar, image_jar)

            # Train
            for m in model_names:
                th = threading.Thread(target=cls.__do_thread_train,
                                      args=(m,
                                            estimator_jar[m],
                                            feature_jar,
                                            target_jar[m])
                                      )
                threads.append(th)
                th.start()

            for item in threads:
                item.join()

            # Change the used flag
            if not django.conf.settings.DEBUG:
                faces.update(used_flag=2)

        except Exception as e:
            # print(e)
            print("Error occurred while training")
            pass

        print("=" * 10 + " Train Finish " + "=" * 10)

        # Set the busy flag
        UtilTrainer.__busy = False

    @classmethod
    def __do_thread_train(cls, model_name, estimator, feature_jar, target):
        print("{} Start".format(model_name.capitalize()))

        try:
            class_worker = 'HowOldWebsite.trainers.trainer_{}.Trainer{}'.format(
                model_name, model_name.capitalize()
            )
            obj_worker = reflect_get_class(class_worker)
            worker = obj_worker(estimator)
            worker.train(feature_jar, target)
        except Exception as e:
            print(e)
            pass

        print("{} OK".format(model_name.capitalize()))
