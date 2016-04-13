# -*- coding: UTF-8 -*-

import os
from time import clock

import scipy.io
from django.core.management.base import BaseCommand
from sklearn.externals import joblib

from HowOldAreYou.settings import SAVE_DIR
from HowOldWebsite.kernel import get_feature_extractor
from HowOldWebsite.utils import do_imread
from HowOldWebsite.utils import do_rgb2gray

__author__ = 'haoyu'


class Command(BaseCommand):
    help = 'Refresh the STD files'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # django.setup()
        time_start = clock()
        print("=" * 10 + " We are refreshing the STD data " + '=' * 10)

        # The directories
        description_file_path = os.path.join(
            SAVE_DIR['STD_FACE_DESCRIPTION'], "how_old_data.pkl")
        mat_file_path = SAVE_DIR['STD_FACE_MAT']
        face_file_path = SAVE_DIR['STD_FACE_IMAGE']

        # Load the description file
        description_file = joblib.load(description_file_path)

        # Load the extractors
        extractor_landmark = get_feature_extractor('LANDMARK')
        extractor_rbm = get_feature_extractor('RBM')
        extractor_hog = get_feature_extractor('HOG')
        extractor_lbp = get_feature_extractor('LBP')
        extractor_lbp_hog = get_feature_extractor('LBP_HOG')

        # The counter
        success_counter = 0
        # Read each image, extra features and save
        for item in description_file:
            try:
                # Ready
                feature = {}
                image_filename = item[0]
                image_path = os.path.join(face_file_path, image_filename)
                image_feature_path = os.path.join(mat_file_path, image_filename + '.mat')

                # Go
                cv_face_image = do_imread(image_path)
                face_gray = do_rgb2gray(cv_face_image)

                # Get features
                f_landmark = extractor_landmark(face_gray)
                f_rbm = extractor_rbm(cv_face_image)
                f_hog = extractor_hog(face_gray)
                f_lbp = extractor_lbp(face_gray)
                f_lbp_hog = extractor_lbp_hog(face_gray)

                # Save features
                feature['landmark'] = f_landmark
                feature['rbm'] = f_rbm
                feature['hog'] = f_hog
                feature['lbp'] = f_lbp
                feature['lbp_hog'] = f_lbp_hog

                # Save to disk
                scipy.io.savemat(image_feature_path, feature)

                # Print it
                print("Success: {}".format(image_filename))
                success_counter += 1
            except Exception as e:
                print(e)
                pass

        print("=" * 10 + " Refresh STD data success " + '=' * 10)
        time_end = clock()
        print("File: {}\t\tTime: {}".format(success_counter, (time_end - time_start)))
