import cv2
import numpy as np

from Listas import Listas

puntos = []


class ChessBoard:
    def __init__(self, img, size=8):
        self.patternSize = size + 1

        self.points_chessboard = np.ones((self.patternSize * self.patternSize, 3))
        self.points_chessboard[:, :2] = np.mgrid[0:self.patternSize, 0:self.patternSize].T.reshape(-1, 2)

        self.image = cv2.imread(img)

        self.points_roi = []
        self.points_image = np.zeros((2, self.patternSize * self.patternSize))

        cv2.namedWindow('Calibrate', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Calibrate', 1100, -100)
        cv2.resizeWindow('Calibrate', 600, 500)

        cv2.setMouseCallback('Calibrate', self.mouse_click, self)
        cv2.imshow('Calibrate', self.image)

        cv2.waitKey(0)

        #

        H = self.compute_warp()

        points_image = np.matmul(H, self.points_chessboard.transpose())

        self.points_image[0, :] = points_image[0, :] / points_image[2, :]
        self.points_image[1, :] = points_image[1, :] / points_image[2, :]
        self.points_image = self.points_image.transpose()

        #

        # n = 0
        for point in self.points_image:
            cv2.circle(self.image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
            puntos.append(point)
            # cv2.putText(self.image, str(n), tuple(point.astype(int)), \
            # fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=1)
            # n += 1

        #

        cv2.imshow('Calibrate', self.image)

        cv2.waitKey(0)

        cv2.imwrite('PythonCache/Image.jpg', self.image)

    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            self.points_roi.append((float(x), float(y)))

            cv2.circle(self.image, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow('Calibrate', self.image)

    def compute_warp(self):

        index_bl = 0
        index_br = self.patternSize - 1
        index_tr = (self.patternSize * self.patternSize) - 1
        index_tl = index_tr - self.patternSize + 1

        points_corners = self.points_chessboard[[index_bl, index_br, index_tr, index_tl], 0:2]

        points_roi = np.float32(self.points_roi)

        H, status = cv2.findHomography(points_corners, points_roi)
        return H


class Calibrate:
    def __init__(self, winName, x, y, width, height, cam):

        cv2.namedWindow(winName)
        cv2.moveWindow(winName, x, y)
        cv2.resizeWindow(winName, width, height)

        self.cam = cam

    def esquinas(self, winName):

        camera_capture = self.get_image()

        cv2.imwrite('PythonCache/Image.jpg', camera_capture)
        cv2.destroyWindow(winName)

        tablero = ChessBoard('PythonCache/Image.jpg')

    def casillas(self):
        n = 0
        for i in range(1, 9):

            for j in range(1, 9):

                Listas.casillas[(i, j)] = [puntos[n], puntos[n+9], puntos[n+10], puntos[n+1]]
                n += 1
            n += 1
        # print Listas.casillas

    def get_image(self):

        retval, im = self.cam.read()
        return im

    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            pass
