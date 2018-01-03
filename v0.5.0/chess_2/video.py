#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
from time import sleep

import lists
sys.path.append('..')
import audio
from func import thread_starter, video_exit, opencv_win

sts = audio.sts
"""
self.points and self.squares in Calibration may are dispensable
look the similarity between self.points and self.points_image
"""


class Camera:
    def __init__(self):
        self.cameras = self._seek_cameras()

    class CameraError(Exception):
        pass

    def choose(self):
        if len(self.cameras) == 0:
            raise self.CameraError

        elif len(self.cameras) == 1:
            cam = self.cameras[0]

        else:
            thread_starter(sts.say, [audio.language.aud_017])
            cam = self._select_cam(self.cameras)

        return cam

    def _select_cam(self, cams):
        new_cams = []
        if len(cams) > 2:
            new_cams.extend(cams[2:])
            cams = cams[:2]
        cam = cams[0]
        cv2.namedWindow('cam')
        while True:
            frame = cam.read()[1]
            k = cv2.waitKey(1) & 0xFF
            video_exit(k)

            if k == 10:
                cv2.destroyWindow('cam')
                return cam
            if k == 32:
                if len(cams) == 1:
                    return
                elif len(new_cams) > 0:
                    cams[0].release()
                    cams[1].release()

                    self._select_cam(new_cams)
                    for i in new_cams:
                        i.release()

                    self._select_cam(self._seek_cameras())
                    return
                cam = cams[cams.index(cam) - 1]
            cv2.imshow('cam', frame)

    @staticmethod
    def _seek_cameras():
        cameras = [i for i in range(100) if cv2.VideoCapture(i).isOpened()]
        for i in cameras:
            cameras[i] = cv2.VideoCapture(i)
        return cameras


class Calibration:
    def __init__(self, img):
        o_image = img if type(img) == np.ndarray else cv2.imread(img)
        self.image = o_image.copy()

        self.corners = []
        self.points = []
        self.rectified_points = np.mgrid[0:9, 0:9].T.reshape(-1, 2)*100
        self.squares = {}
        self.rectified_squares = {}

        self.points_image = np.zeros((2, 9*9))
        self.points_chessboard = np.ones((9*9, 3))
        self.points_chessboard[:, :2] = self.rectified_points

        while True:
            # Set points
            try:
                self.win_name = audio.language.open_cv_2
                opencv_win(self.win_name, 1100, -100, 600, 500)
            except UnicodeEncodeError:      # For testing as a script
                self.win_name = 'test'
                opencv_win(self.win_name, 1100, -100, 600, 500)

            cv2.setMouseCallback(self.win_name, self.mouse_click, self)
            cv2.imshow(self.win_name, self.image)

            cv2.waitKey(0)

            # Calculate homography
            model_corners = self.points_chessboard[[0, 8, 80, 72], 0:2]
            self.transform = cv2.findHomography(np.float32(model_corners), np.float32(self.corners))[0]

            points = np.matmul(self.transform, self.points_chessboard.transpose())

            self.points_image[0, :] = points[0, :] / points[2, :]
            self.points_image[1, :] = points[1, :] / points[2, :]
            self.points_image = self.points_image.transpose()

            # Show points to the user
            for point in self.points_image:
                cv2.circle(self.image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
                self.points.append(point)

            cv2.imshow(self.win_name, self.image)
            thread_starter(sts.say, [audio.language.aud_016])

            if cv2.waitKey(0) & 0xFF == 10:     # The user is agree
                break
            else:
                self.image = o_image.copy()
                self.corners = []
                self.points_image = np.zeros((2, 9 * 9))
                self.points_chessboard = np.ones((9 * 9, 3))
                self.points_chessboard[:, :2] = self.rectified_points

        self.allocate_squares(self.squares, self.points)
        self.allocate_squares(self.rectified_squares, self.rectified_points)

    class CalibrationError(Exception):
        pass

    def mouse_click(self, *args):
        event, x, y = args[0], args[1], args[2]

        if event == cv2.EVENT_LBUTTONDOWN:
            self.corners.append((float(x), float(y)))

            cv2.circle(self.image, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow(self.win_name, self.image)

    def rectify_image(self, img, rotate=False):
        trf = cv2.invert(self.transform)[1]
        img_dst = cv2.warpPerspective(img, trf, (800, 800))

        if rotate:
            center = cv2.getRotationMatrix2D((400, 400), 180, 1)
            img_dst = cv2.warpAffine(img_dst, center, (800, 800))
            img_dst = cv2.flip(img_dst, 1)

        return img_dst

    def rectify_crop(self, img, corners):       # img is not rectified
        status, trf = cv2.invert(self.transform)
        img_dst = cv2.warpPerspective(img, trf, (800, 800))

        corners_hom = np.ones((4, 3))
        corners_hom[:, 0:2] = corners
        corners_transformed = np.matmul(trf, corners_hom.transpose())
        corners_result = np.zeros((2, 4))

        corners_result[0, :] = corners_transformed[0, :] / corners_transformed[2, :]
        corners_result[1, :] = corners_transformed[1, :] / corners_transformed[2, :]

        corners_result[corners_result < 0] = 0
        corners_result = np.rint(corners_result)

        r0 = (corners_result[0, 0] + corners_result[0, 2]) / 2
        r1 = (corners_result[0, 1] + corners_result[0, 3]) / 2
        c0 = (corners_result[1, 0] + corners_result[1, 1]) / 2
        c1 = (corners_result[1, 2] + corners_result[1, 3]) / 2

        patch_size = (int(r1 - r0), int(c1 - c0))
        center = (int((r1 + r0) / 2), int((c1 + c0) / 2))

        return cv2.getRectSubPix(img_dst, patch_size, center)

    @staticmethod
    def allocate_squares(dic, points):
        n = 0
        for y in range(1, 9):
            for x in range(1, 9):
                dic[(x, y)] = [list(points[n].astype(int)),
                               list(points[n + 1].astype(int)),
                               list(points[n + 9].astype(int)),
                               list(points[n + 10].astype(int))]
                n += 1
            n += 1


class Detection:
    def __init__(self, calibration_class):
        self.__chessboard = calibration_class
        self.__patch1, self.__patch2 = None, None

    class DetectionError(Exception):
        pass

    def board(self, patch1, patch2, player):    # player must be 'White' or 'Black'
        img_1 = self.__chessboard.rectify_image(patch1)
        img_2 = self.__chessboard.rectify_image(patch2)

        contours, threshold, diff = self.diff(img_1, img_2)

        areas = []
        max_contours = []
        squares = []

        for c in contours:
            if cv2.contourArea(c) > 1000:
                areas.append(cv2.contourArea(c))

        if len(areas) == 0:
            raise EnvironmentError

        elif len(areas) == 1:
            return self._squares(patch1, patch2, player)

        else:
            areas.sort()
            max_areas = [areas[-1], areas[-2]]

        for c in contours:
            for a in max_areas:
                if cv2.contourArea(c) == a:
                    max_contours.append(c)

        for c in max_contours:
            x, y, w, h = cv2.boundingRect(c)
            center = ((x + w/2), (y + h/2))

            cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(img_2, center, 3, (255, 0, 0))

            for i in self.__chessboard.rectified_squares:
                j = self.__chessboard.rectified_squares[i]

                right_bottom = tuple(j[0])      # The 0, 0 point is at the top-left window's corner
                left_top = tuple(j[3])

                if right_bottom[0] < center[0] and right_bottom[1] < center[1] and \
                   left_top[0] > center[0] and left_top[1] > center[1]:

                    if i not in squares:
                        squares.append(i)

        # self.__check_images(img_2, threshold, diff)

        pos0 = squares[0] if squares[0] in lists.OccupiedSquares[player] else squares[1]
        pos1 = squares[0] if squares[0] not in lists.OccupiedSquares[player] else squares[1]

        if len(squares) != 2 or pos0 == pos1:
            return self._squares(patch1, patch2, player)

        else:
            print pos0[0], pos0[1], ">>", pos1[0], pos1[1]
            return pos0, pos1

    def _squares(self, patch1, patch2, player):
        print "squares"
        pos0, pos1 = [tuple]*2
        self.__patch1 = patch1
        self.__patch2 = patch2
        squares = {}

        for y in xrange(1, 9):
            for x in xrange(1, 9):
                thread = thread_starter(self.__subprocess, [x, y, squares])
                if (x, y) == (8, 8):
                    thread.join()

        areas = squares.values()
        areas.sort()
        max_areas = [areas[len(areas) - 1], areas[len(areas) - 2]]

        for square in squares:
            if squares[square] in max_areas:
                if square in lists.OccupiedSquares[player]:
                    pos0 = square
                else:
                    pos1 = square

        try:
            print pos0[0], pos0[1], ">>", pos1[0], pos1[1]
            return pos0, pos1
        except UnboundLocalError:
            print pos0, pos1
            raise self.DetectionError

    def __subprocess(self, x, y, dic):
        corners = np.array(self.__chessboard.squares[(x, y)], np.float32)

        square_1 = self.__chessboard.rectify_crop(self.__patch1, corners)
        square_2 = self.__chessboard.rectify_crop(self.__patch2, corners)

        contours = self.diff(square_1, square_2)[0]

        for c in contours:
            if cv2.contourArea(c) > 400:
                if (x, y) not in dic:
                    dic[(x, y)] = cv2.contourArea(c)

                elif cv2.contourArea(c) > dic[(x, y)]:
                    dic[(x, y)] = cv2.contourArea(c)
        return

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
