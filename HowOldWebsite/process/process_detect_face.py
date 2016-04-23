# -*- coding: UTF-8 -*-

import os
import uuid

import django.conf
import dlib
import skimage.io
import skimage.transform

from HowOldWebsite.kernel.feature import do_collect_feature
from HowOldWebsite.kernel.feature import feature_extract_all
from HowOldWebsite.models import RecordFace

__author__ = 'Hao Yu'


def face_detect(database_original_image, image):
    try:
        # Change rgb image to gray image
        # cv_image_gray = do_rgb2gray(image)

        # Face detection
        faces = __do_detect(image)

        # Save the faces
        database_face_detected, feature_extracted = \
            __do_save_faces_and_extract_feature(database_original_image, image, faces);
        return True, database_face_detected, feature_extracted
    except Exception as e:
        # print(e)
        return False, None, None


def __do_detect(image):
    # Get the detector
    detector = dlib.get_frontal_face_detector()
    # Detect it!
    faces_detected = detector(image, 1)
    return faces_detected


def __do_save_faces_and_extract_feature(database_original_image, image, faces):
    database_face_detected, image_face_detected = \
        __do_save_face(database_original_image, image, faces)
    feature_extracted = __do_feature_extract(image_face_detected)
    return database_face_detected, feature_extracted


def __do_save_face(database_original_image, image, faces):
    database_face = []
    image_face = []

    for ith, face in enumerate(faces):
        try:
            # Generate the id
            face_id = uuid.uuid4()

            # Make the filename
            face_filename_color = os.path.join(django.conf.settings.SAVE_DIR['FACE'], str(face_id) + '.jpg')
            # face_filename_gray = os.path.join(SAVE_DIR['FACE_GRAY'], str(face_id) + '.jpg')

            # Get the face range
            cv_face_image = image[face.top():face.bottom(), face.left():face.right(), :]

            # Resize to 256*256
            cv_face_image = skimage.transform.resize(cv_face_image, (256, 256))
            cv_face_image = skimage.img_as_ubyte(cv_face_image)

            # Change image to gray
            # cv_face_image_gray = skimage.color.rgb2gray(cv_face_image)

            # Save to disk
            skimage.io.imsave(face_filename_color, cv_face_image)

            # A new database record
            database_record_face = RecordFace(id=face_id,
                                              original_image=database_original_image,
                                              location_left=face.left(),
                                              location_right=face.right(),
                                              location_top=face.top(),
                                              location_bottom=face.bottom())

            # Save to database
            database_record_face.save()

            # Append to record
            image_face.append(cv_face_image)
            database_face.append(database_record_face)
        except Exception as e:
            # print(e)
            pass

    return database_face, image_face


def __do_feature_extract(image_faces):
    # The result array
    features = {}

    # For each face, extract the feature
    for face in image_faces:
        feature_single = feature_extract_all(face)
        features = do_collect_feature(features, feature_single)

    return features
