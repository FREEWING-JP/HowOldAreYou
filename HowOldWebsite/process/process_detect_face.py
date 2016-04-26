# -*- coding: UTF-8 -*-

import os
import uuid

import django.conf
import dlib
import skimage.io
import skimage.transform

from HowOldWebsite.features.util_feature import FeatureUtil
from HowOldWebsite.models import RecordFace
from HowOldWebsite.utils.image import do_rgb2gray

__author__ = 'Hao Yu'


def face_detect(database_original_image, image):
    success = False
    database_record = None
    feature_extracted = None

    try:
        # Face detection
        faces = __do_detect(image)

        # Save the faces
        database_record, face_jar = \
            __do_save_face(database_original_image, image, faces)

        # Extract feature
        feature_extracted = __do_feature_extract(face_jar)
        success = True
    except Exception as e:
        # print(e)
        pass

    return success, database_record, feature_extracted


def __do_detect(image):
    # Get the detector
    detector = dlib.get_frontal_face_detector()
    # Detect it!
    faces_detected = detector(image, 1)
    return faces_detected


def __do_save_face(database_original_image, image, faces):
    database_face = []
    face_jar = {
        'rgb': [],
        'gray': [],
    }

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
            cv_face_image_gray = do_rgb2gray(cv_face_image)

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
            # database_record_face.save()

            # Append to record
            face_jar['rgb'].append(cv_face_image)
            face_jar['gray'].append(cv_face_image_gray)
            database_face.append(database_record_face)
        except Exception as e:
            # print(e)
            pass

    return database_face, face_jar


def __do_feature_extract(image_faces):
    # The result array
    features = {}
    try:
        for fe in ['lbp', 'hog', 'lbp_hog', 'landmark', 'rbm']:
            features[fe] = FeatureUtil.extract_all(fe, image_faces)
    except Exception as e:
        # print(e)
        pass
    return features
