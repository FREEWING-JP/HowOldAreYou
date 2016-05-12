# -*- coding: UTF-8 -*-

import os
from time import clock

import django.conf
from django.core.management.base import BaseCommand
from sklearn.externals import joblib

from HowOldWebsite.features.util_feature import UtilFeature
from HowOldWebsite.utils.image import do_imread
from HowOldWebsite.utils.image import do_rgb2gray

__author__ = 'Hao Yu'


class Command(BaseCommand):
    help = 'Refresh the STD files.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # django.setup()
        time_start = clock()
        print("=" * 10 + " We are refreshing the STD data " + '=' * 10)

        # The directories
        description_file_path = os.path.join(
            django.conf.settings.SAVE_DIR['STD_FACE_DESCRIPTION'], "how_old_data.pkl")
        mat_file_path = django.conf.settings.SAVE_DIR['STD_FACE_MAT']
        face_file_path = django.conf.settings.SAVE_DIR['STD_FACE_IMAGE']

        # Load the description file
        description_file = joblib.load(description_file_path)

        # The counter
        success_counter = 0
        # Read each image, extra features and save
        for item in description_file:
            try:
                # Ready
                image_filename = item[0]
                image_path = os.path.join(face_file_path, image_filename)
                image_feature_path = os.path.join(mat_file_path, image_filename + '.pkl')

                # Go
                cv_face_image = do_imread(image_path)
                cv_face_image_gray = do_rgb2gray(cv_face_image)

                face_jar = {
                    'rgb': [],
                    'gray': [],
                }

                face_jar['rgb'].append(cv_face_image)
                face_jar['gray'].append(cv_face_image_gray)

                feature = dict()
                for fe in ['lbp', 'hog', 'lbp_hog', 'landmark', 'rbm']:
                    feature[fe] = UtilFeature.extract_all(fe, face_jar)

                image_info = dict()
                image_info["feature"] = feature
                image_info["target"] = dict()
                if 'male' == item[3].lower():
                    image_info["target"]["sex"] = [1]
                else:
                    image_info["target"]["sex"] = [0]
                image_info["target"]["age"] = [int(item[1])]
                image_info["target"]["age_lambda"] = [float(item[2])]
                image_info["target"]["smile"] = [float(item[5])]

                # Save to disk
                # scipy.io.savemat(image_feature_path, image_info)
                joblib.dump(image_info, image_feature_path)

                # Print it
                print("Success: {}".format(image_filename))
                success_counter += 1
            except Exception as e:
                print(e)
                pass

        print("=" * 10 + " Refresh STD data success " + '=' * 10)
        time_end = clock()
        print("File: {}\t\tTime: {}".format(success_counter, (time_end - time_start)))
