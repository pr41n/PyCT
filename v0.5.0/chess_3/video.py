#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from time import sleep

import audio
import lists
from func import thread_starter, prevent_auido_error, video_exit, opencv_win


sts = audio.sts


class Camera:
    def __init__(self):
        pass

    def choose(self):
        pass

    def next_cam(self):
        pass


class Calibration:
    def __init__(self, img):
        pass

    class CalibrationError(Exception):
        pass

    def mouse_click(self, *args):
        pass

    def rectify_image(self, img, rotation=False):
        pass

    def rectify_crop(self, img, corners):       # img is not rectified
        pass

    @staticmethod
    def allocate_squares(dic, points):
        pass


class Detection:
    def __init__(self, calibration_class):
        self.chessboard = calibration_class
        self.patch1, self.patch2 = None, None

    class DetectionError(Exception):
        pass

    def board(self, patch1, patch2, player):
        img_1 = self.chessboard.rectify_image(patch1)
        img_2 = self.chessboard.rectify_image(patch2)

        contours, threshold, diff = self.diff(img_1, img_2)

        pass

    def squares(self, patch1, patch2, player):
        pass

    def __subprocess(self, x, y, dic):
        pass

    @staticmethod
    def diff(img_1, img_2):
        kernel = np.ones((5, 5), np.uint8)

        grey_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        grey_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(grey_1, grey_2)

        threshold = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        threshold = cv2.dilate(threshold, kernel, iterations=2)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

        contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

        return contours, threshold, diff

    @staticmethod
    def __check_images(img, threshold, diff):
        cv2.imshow('%s' % img, img)
        cv2.imshow('threshold', threshold)
        cv2.imshow('diff', diff)

        if cv2.waitKey(0) & 0xFF == 27:
            cv2.destroyAllWindows()
            exit(11)

        cv2.destroyWindow('%s' % img)
        cv2.destroyWindow('threshold')
        cv2.destroyWindow('diff')
