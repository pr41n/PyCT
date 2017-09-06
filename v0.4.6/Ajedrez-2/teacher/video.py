# -*- coding: utf-8 -*-

import cv2
import numpy as np

import audio
import lists
from window import OpenCV
from func import thread_starter, inv_change_position, give_values, \
                 prevent_auido_error, video_exit


sts = audio.sts
calibrated = False


class ChessBoard:
    def __init__(self, img, calibrate=True, esq=list, size=8):
        global calibrated
        self.patternSize = size + 1

        self.points_chessboard = np.ones((self.patternSize * self.patternSize, 3))
        self.points_chessboard[:, :2] = np.mgrid[0:self.patternSize, 0:self.patternSize].T.reshape(-1, 2)*100

        self.image = cv2.imread(img)

        self.points_image = np.zeros((2, self.patternSize * self.patternSize))

        if not calibrate:
            self.points_roi = esq
            self.transform = self.compute_warp(self.points_roi)

        else:
            win_name = audio.language.open_cv_2
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
            cv2.moveWindow(win_name, 1100, -100)
            cv2.resizeWindow(win_name, 600, 500)
            self.points_roi = []
            cv2.setMouseCallback(win_name, self.mouse_click, self)
            cv2.imshow(win_name, self.image)

            cv2.waitKey(0)

            self.transform = self.compute_warp(self.points_roi)

            points_image = np.matmul(self.transform, self.points_chessboard.transpose())

            self.points_image[0, :] = points_image[0, :] / points_image[2, :]
            self.points_image[1, :] = points_image[1, :] / points_image[2, :]
            self.points_image = self.points_image.transpose()

            #
            # n = 0
            for point in self.points_image:
                cv2.circle(self.image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
                lists.points.append(point)
                # cv2.putText(self.image, str(n), tuple(point.astype(int)),
                #             fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=1)
                # n += 1

            #

            cv2.imshow(win_name, self.image)
            thread_starter(sts.say, [audio.language.calibration_2])

            k = cv2.waitKey(0) & 0xFF

            calibrated = True if k == 10 else False

            if not calibrated:
                return

            n = 0
            for y in range(1, 9):
                for x in range(1, 9):
                    lists.squares[(x, y)] = [list(lists.points[n].astype(int)),
                                             list(lists.points[n + 1].astype(int)),
                                             list(lists.points[n + 9].astype(int)),
                                             list(lists.points[n + 10].astype(int))]
                    n += 1
                n += 1

    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            self.points_roi.append((float(x), float(y)))
            lists.corners.append((float(x), float(y)))

            cv2.circle(self.image, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow(audio.language.open_cv_2, self.image)

    def compute_warp(self, points_roi):

        index_bl = 0
        index_br = self.patternSize - 1
        index_tr = (self.patternSize * self.patternSize) - 1
        index_tl = index_tr - self.patternSize + 1

        points_corners = self.points_chessboard[[index_bl, index_br, index_tr, index_tl], 0:2]

        points_roi = np.float32(points_roi)
        points_corners = np.float32(points_corners)

        H, status = cv2.findHomography(points_corners, points_roi)

        return H

    def rectify_crop(self, img_src, corners):

        status, trf = cv2.invert(self.transform)
        img_dst = cv2.warpPerspective(img_src, trf, (800, 800))

        corners_hom = np.ones((4, 3))
        corners_hom[:, 0:2] = corners
        corners_transformed = np.matmul(trf, corners_hom.transpose())
        corners_result = np.zeros((2, 4))

        corners_result[0, :] = corners_transformed[0, :] / corners_transformed[2, :]
        corners_result[1, :] = corners_transformed[1, :] / corners_transformed[2, :]

        corners_result[corners_result < 0] = 0
        corners_result = np.rint(corners_result)

        r0 = (corners_result[0, 0] + corners_result[0, 2])/2
        r1 = (corners_result[0, 1] + corners_result[0, 3])/2
        c0 = (corners_result[1, 0] + corners_result[1, 1])/2
        c1 = (corners_result[1, 2] + corners_result[1, 3])/2

        patchSize = (int(r1-r0), int(c1-c0))
        center = (int((r1+r0)/2), int((c1+c0)/2))

        return cv2.getRectSubPix(img_dst, patchSize, center)

    #
    #
    #

    def rectify_chessboard(self, img):          # Image is not a file

        image = img

        points_image = np.zeros((2, self.patternSize * self.patternSize))

        points_roi = [(0, 800), (800, 800), (800, 0), (0, 0)]

        transform = self.compute_warp(points_roi)

        sub_points_image = np.matmul(transform, self.points_chessboard.transpose())

        points_image[0, :] = sub_points_image[0, :] / sub_points_image[2, :]
        points_image[1, :] = sub_points_image[1, :] / sub_points_image[2, :]
        points_image = points_image.transpose()

        #

        # n = 0
        for point in points_image:
            cv2.circle(image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
            lists.rectified_points.append(point)
            # cv2.putText(image, str(n), tuple(point.astype(int)),
            #            fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=0.5)
            # n += 1
        #

        n = 0
        for y in range(1, 9):
            for x in range(1, 9):
                lists.rectified_squares[(x, y)] = [list(lists.rectified_points[n].astype(int)),
                                                   list(lists.rectified_points[n + 1].astype(int)),
                                                   list(lists.rectified_points[n + 9].astype(int)),
                                                   list(lists.rectified_points[n + 10].astype(int))]
                n += 1
            n += 1

        # self.select(image)

    def rectify_image(self, img_src):
        status, trf = cv2.invert(self.transform)
        img_dst = cv2.warpPerspective(img_src, trf, (800, 800))

        M = cv2.getRotationMatrix2D((400, 400), 180, 1)

        img_dst = cv2.warpAffine(img_dst, M, (800, 800))
        img_dst = cv2.flip(img_dst, 1)

        return img_dst

    @staticmethod
    def select(image):
        sub_img = image
        while True:

            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                cv2.destroyAllWindows()
                break

            if k == ord('c'):
                square = inv_change_position(raw_input("Casilla: "))

                for j in lists.rectified_squares[square]:
                    cv2.circle(sub_img, tuple(j), 5, (0, 0, 255), -1)

            cv2.namedWindow('select',  cv2.WINDOW_NORMAL)
            cv2.imshow('selct', sub_img)


class Calibration:
    def __init__(self, img):        # Image is a file
        self.chessboard = ChessBoard(img)
        self.rectified_image = self.chessboard.rectify_image(cv2.imread(img))
        self.chessboard.rectify_chessboard(self.rectified_image)

    def rectify_image(self, img):       # Image is not a file
        self.rectified_image = self.chessboard.rectify_image(img)
        return self.rectified_image

    @staticmethod
    def value():
        return calibrated


class Detection:
    def __init__(self, patch1, patch2, player):        # Images are files
        self.chessboard = ChessBoard(patch1, False, lists.corners)

        self.patch1 = patch1
        self.patch2 = patch2

        self.lista = lists.OccupiedSquares['White'] if player == 1 else lists.OccupiedSquares['Black']

    def Board(self):
        img_1 = self.chessboard.rectify_image(cv2.imread(self.patch1))
        img_2 = self.chessboard.rectify_image(cv2.imread(self.patch2))

        contours, threshold, diff = self.Diff(img_1, img_2)
        """
        cv2.imshow('threshold', threshold)
        cv2.imshow('diff', diff)

        k = cv2.waitKey(0)

        if k == 27:
            cv2.destroyAllWindows()
            exit(11)

        cv2.destroyWindow('threshold')
        cv2.destroyWindow('diff')
        """

        areas = []
        for c in contours:
            if cv2.contourArea(c) > 1000:
                areas.append(cv2.contourArea(c))

        if len(areas) == 2:
            max_areas = areas

        elif len(areas) < 2:
            return self.Squares()

        else:
            areas.sort()
            max_areas = [areas[len(areas) - 1], areas[len(areas) - 2]]

        max_contours = []
        for c in contours:
            for a in max_areas:
                if cv2.contourArea(c) == a:
                    max_contours.append(c)

        squares = []
        pts = []

        for c in max_contours:
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            center = ((2 * x + w) / 2, (2 * y + h) / 2)

            pts.append(center)
            cv2.circle(img_2, center, 3, (255, 0, 0))

            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                exit(11)

            for p in pts:
                for i in lists.rectified_squares:
                    j = lists.rectified_squares[i]

                    left_bottom = tuple(j[2])
                    right_top = tuple(j[1])

                    if left_bottom[0] < p[0] and left_bottom[1] < p[1] and \
                       right_top[0] > p[0] and right_top[1] > p[1]:

                        if i not in squares:
                            squares.append(i)
        """
        cv2.imshow('%s' % img_2, img_2)
        cv2.imshow('threshold', threshold)
        cv2.imshow('diff', diff)

        k = cv2.waitKey(0)

        if k == 27:
            cv2.destroyAllWindows()
            exit(11)

        cv2.destroyWindow('%s' % img_2)
        cv2.destroyWindow('threshold')
        cv2.destroyWindow('diff')
        """
        if len(squares) == 2:
            pos0, pos1 = give_values(tuple, 2)

            for square in squares:
                if square in self.lista:
                    pos0 = square
                else:
                    pos1 = square

            try:
                print pos0[0], pos0[1], pos1[0], pos1[1]
                return pos0, pos1

            except TypeError:
                return self.Squares()

        else:
            return self.Squares()

    def Squares(self):
        print "casillas"
        squares = {}
        for y in range(1, 9):
            for x in range(1, 9):
                thread = thread_starter(self.__squareProcess, [x, y, squares])

                if (x, y) == (8, 8):
                    thread.join()
        areas = []
        for square in squares:
            areas.append(squares[square])

        areas.sort()
        max_areas = [areas[len(areas) - 1], areas[len(areas) - 2]]

        pos0, pos1 = give_values(tuple, 2)

        for square in squares:
            if squares[square] in max_areas:
                if square in self.lista:
                    pos0 = square
                else:
                    pos1 = square

        try:
            print pos0[0], pos0[1], pos1[0], pos1[1]
            return pos0, pos1

        except TypeError:
            print squares
            print pos0, pos1
            return None, None

    def __squareProcess(self, x, y, dic):
        corners = np.array(lists.squares[(x, y)], np.float32)

        square_1 = self.chessboard.rectify_crop(cv2.imread(self.patch1), corners)
        square_2 = self.chessboard.rectify_crop(cv2.imread(self.patch2), corners)

        contours = self.Diff(square_1, square_2)[0]

        for c in contours:
            if cv2.contourArea(c) > 400:
                if (x, y) not in dic:
                    dic[(x, y)] = cv2.contourArea(c)

                elif cv2.contourArea(c) > dic[(x, y)]:
                    dic[(x, y)] = cv2.contourArea(c)

    @staticmethod
    def Diff(img_1, img_2):
        kernel = np.ones((5, 5), np.uint8)

        grey_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        grey_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(grey_1, grey_2)

        threshold = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        threshold = cv2.dilate(threshold, kernel, iterations=2)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

        img_contour = threshold.copy()
        im, contours, hierarchy = cv2.findContours(img_contour, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours, threshold, diff


class Camera:
    def __init__(self):
        self.choosing = True
        self.election = 0

        self.cam_1 = cv2.VideoCapture(0)

        self.second_camera = False
        if cv2.VideoCapture(1).isOpened():

            thread_starter(prevent_auido_error, [sts.say, audio.language.camera_choosing])

            OpenCV('cam 1', 200, 100, 500, 500)
            OpenCV('cam 2', 700, 100, 500, 500)

            self.cam_2 = cv2.VideoCapture(1)
            self.second_camera = True

    def choose(self):
        while True:
            if self.second_camera:
                ret_1, frame_1 = self.cam_1.read()
                ret_2, frame_2 = self.cam_2.read()

                cv2.imshow('cam 1', frame_1)
                cv2.imshow('cam 2', frame_2)

                cv2.setMouseCallback('cam 1', self.election_1)
                cv2.setMouseCallback('cam 2', self.election_2)

                k = cv2.waitKey(1) & 0xFF
                video_exit(k)

            else:
                self.choosing = False

            if not self.choosing:
                cv2.destroyAllWindows()
                self.cam_1.release()
                return self.election

    def election_1(self, event, x, y, flags, param):
        self.sub_election(event, 0)

    def election_2(self, event, x, y, flags, param):
        self.sub_election(event, 1)

    def sub_election(self, event, num):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.choosing = False
            self.election = num
            self.cam_1.release()
            self.cam_2.release()
