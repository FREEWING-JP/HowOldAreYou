# -*- coding: UTF-8 -*-

__author__ = 'haoyu'

import os
import uuid

import cv2

from HowOldAreYou.settings import SAVE_DIR
from .models import RecordFace


def face_detect(original_image, cv_image):
    try:
        # change rgb image to gray image
        cv_image_gray = do_rgb2gray(cv_image)

        # face detection
        cv_faces = do_detect(cv_image_gray)

        # show me the detection result
        # do_show_face(cv_faces,cv_image)

        # save the faces
        face_detected = do_save_face(original_image, cv_image, cv_faces);
        return True, face_detected
    except:
        return False


def do_rgb2gray(cv_image):
    if cv_image.ndim == 3:
        return cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    else:
        return cv_image


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
    face_detected = []
    for (x, y, width, height) in cv_faces:
        try:
            face_id = uuid.uuid4()
            face_filename_color = os.path.join(SAVE_DIR['FACE'], str(face_id) + '.jpg')
            # face_filename_gray = os.path.join(SAVE_DIR['FACE_GRAY'], str(face_id) + '.jpg')

            # A new database record
            record_face = RecordFace(id=face_id,
                                     original_image=original_image,
                                     location_x1=x,
                                     location_x2=x + width,
                                     location_y1=y,
                                     location_y2=y + height)

            cv_face_image = cv_image[record_face.location_y1:record_face.location_y2,
                            record_face.location_x1:record_face.location_x2]
            cv2.imwrite(face_filename_color, cv_face_image)

            # Save to database
            record_face.save()

            # Append to record
            face_detected.append(record_face)
        except Exception as e:
            # print(e)
            pass

    return face_detected


def do_show_face(cv_faces, cv_image):
    print("Found {0} faces!" % (len(cv_faces)))
    for (x, y, w, h) in cv_faces:
        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Faces found", cv_image)
