# -*- coding: UTF-8 -*-

__author__ = 'haoyu'

import cv2
import skimage
import skimage.color
import skimage.io


def do_rgb2gray(image):
    if 3 == image.ndim:
        return skimage.color.rgb2gray(rgb=image)
    else:
        return image


def do_rgb2gray_cv(cv_image):
    if 3 == cv_image.ndim:
        return cv2.cvtColor(src=cv_image, code=cv2.COLOR_BGR2GRAY)
    else:
        return cv_image


def do_imread(path):
    return skimage.io.imread(fname=path)


def do_imread_cv(path):
    return cv2.imread(fname=path)
