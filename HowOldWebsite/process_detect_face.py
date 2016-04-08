# -*- coding: UTF-8 -*-

__author__ = 'haoyu'

import os
import uuid

import cv2

from HowOldAreYou.settings import SAVE_DIR
from .models import RecordFace
from .utils import do_rgb2gray_cv


def face_detect(original_image, cv_image):
    try:
        # change rgb image to gray image
        cv_image_gray = do_rgb2gray_cv(cv_image)

        # face detection
        cv_faces = do_detect(cv_image_gray)

        # show me the detection result
        # do_show_face(cv_faces,cv_image)

        # save the faces
        database_face_detected = do_save_face(original_image, cv_image, cv_faces);
        return True, database_face_detected
    except:
        return False


def do_detect(cv_image_gray):
    # load the harr cascade
    face_cascade = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")

    cv_faces = face_cascade.detectMultiScale(
        cv_image_gray,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # The results are (x,y,height,width)
    return cv_faces


def do_save_face(original_image, cv_image, cv_faces):
    database_result = []
    for (x, y, width, height) in cv_faces:
        try:
            face_id = uuid.uuid4()
            face_filename_color = os.path.join(SAVE_DIR['FACE'], str(face_id) + '.jpg')
            # face_filename_gray = os.path.join(SAVE_DIR['FACE_GRAY'], str(face_id) + '.jpg')

            # A new database record
            database_record_face = RecordFace(id=face_id,
                                              original_image=original_image,
                                              location_x1=x,
                                              location_x2=x + width,
                                              location_y1=y,
                                              location_y2=y + height)

            # The picture of face
            cv_face_image = cv_image[database_record_face.location_y1:database_record_face.location_y2,
                            database_record_face.location_x1:database_record_face.location_x2]

            # Change the face size to 256*256
            cv_face_256 = cv2.resize(cv_face_image, (256, 256), interpolation=cv2.INTER_CUBIC)

            # Save face to disk
            # cv2.imwrite(face_filename_color, cv_face_image)
            cv2.imwrite(face_filename_color, cv_face_256)

            # Save to database
            database_record_face.save()

            # Append to record
            database_result.append(database_record_face)
        except Exception as e:
            # print(e)
            pass

    return database_result


def do_show_face(cv_faces, cv_image):
    print("Found {0} faces!" % (len(cv_faces)))
    for (x, y, w, h) in cv_faces:
        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Faces found", cv_image)
