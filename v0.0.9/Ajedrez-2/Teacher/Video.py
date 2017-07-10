import cv2
import numpy as np
import Listas
from Functions import inv_cambio_posicion

puntos = []
rectify_points = []
esquinas = list


class ChessBoard:
    def __init__(self, img, calibrate=True, esq=list, size=8):
        self.patternSize = size + 1

        self.points_chessboard = np.ones((self.patternSize * self.patternSize, 3))
        self.points_chessboard[:, :2] = np.mgrid[0:self.patternSize, 0:self.patternSize].T.reshape(-1, 2)*100

        self.image = cv2.imread(img)

        self.points_image = np.zeros((2, self.patternSize * self.patternSize))

        if not calibrate:
            self.points_roi = esq

            self.transform = self.compute_warp(self.points_roi)

        else:

            cv2.namedWindow('Calibrate', cv2.WINDOW_NORMAL)
            cv2.moveWindow('Calibrate', 1100, -100)
            cv2.resizeWindow('Calibrate', 600, 500)
            self.points_roi = []
            cv2.setMouseCallback('Calibrate', self.mouse_click, self)
            cv2.imshow('Calibrate', self.image)

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
                puntos.append(point)
                # cv2.putText(self.image, str(n), tuple(point.astype(int)),
                #             fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=1)
                # n += 1

            #

            cv2.imshow('Calibrate', self.image)
            cv2.waitKey(0)

            n = 0
            for y in range(1, 9):
                for x in range(1, 9):
                    Listas.casillas[(x, y)] = [list(puntos[n].astype(int)),
                                               list(puntos[n + 1].astype(int)),
                                               list(puntos[n + 9].astype(int)),
                                               list(puntos[n + 10].astype(int))]
                    n += 1
                n += 1

    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            self.points_roi.append((float(x), float(y)))
            Listas.esquinas.append((float(x), float(y)))

            cv2.circle(self.image, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow('Calibrate', self.image)

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
        #
        status, trf = cv2.invert(self.transform)
        #
        img_dst = cv2.warpPerspective(img_src, trf, (800, 800))
        # cv2.imshow('Warped', img_dst)
        # cv2.waitKey(0)
        #
        corners_hom = np.ones((4, 3))
        corners_hom[:, 0:2] = corners
        #
        corners_transformed = np.matmul(trf, corners_hom.transpose())
        #
        corners_result = np.zeros((2, 4))
        #
        corners_result[0, :] = corners_transformed[0, :] / corners_transformed[2, :]
        corners_result[1, :] = corners_transformed[1, :] / corners_transformed[2, :]
        #
        corners_result[corners_result < 0] = 0
        #
        corners_result = np.rint(corners_result)
        #
        r0 = (corners_result[0, 0] + corners_result[0, 2])/2
        r1 = (corners_result[0, 1] + corners_result[0, 3])/2
        c0 = (corners_result[1, 0] + corners_result[1, 1])/2
        c1 = (corners_result[1, 2] + corners_result[1, 3])/2
        #
        patchSize = (int(r1-r0), int(c1-c0))
        center = (int((r1+r0)/2), int((c1+c0)/2))
        #
        return cv2.getRectSubPix(img_dst, patchSize, center)

    #
    #
    #

    def rectify_chessboard(self, img):          # Image is not a file

        image = img

        points_image = np.zeros((2, self.patternSize * self.patternSize))

        points_roi = [(800, 800), (0, 800), (0, 0), (800, 0)]

        transform = self.compute_warp(points_roi)

        sub_points_image = np.matmul(transform, self.points_chessboard.transpose())

        points_image[0, :] = sub_points_image[0, :] / sub_points_image[2, :]
        points_image[1, :] = sub_points_image[1, :] / sub_points_image[2, :]
        points_image = points_image.transpose()

        #

        # n = 0
        for point in points_image:
            cv2.circle(image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
            rectify_points.append(point)
            # cv2.putText(image, str(n), tuple(point.astype(int)),
            #            fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=0.5)
            # n += 1
        #

        # cv2.namedWindow('Calibrate', cv2.WINDOW_NORMAL)
        # cv2.imshow('Calibrate', image)
        # cv2.waitKey(0)
        # cv2.imwrite('Cache/Image.jpg', image)

        n = 80
        for y in range(1, 9):
            for x in range(1, 9):
                Listas.rectify_squares[(x, y)] = [list(rectify_points[n].astype(int)),
                                                  list(rectify_points[n - 1].astype(int)),
                                                  list(rectify_points[n - 9].astype(int)),
                                                  list(rectify_points[n - 10].astype(int))]
                n -= 1
            n -= 1

        # self.seleccionar(image)
        # return image

    def rectify_image(self, img_src):
        status, trf = cv2.invert(self.transform)
        img_dst = cv2.warpPerspective(img_src, trf, (800, 800))
        # cv2.imshow('Warped', img_dst)
        # cv2.waitKey(0)
        return img_dst

    def seleccionar(self, image):
        sub_img = image
        while True:

            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                cv2.destroyAllWindows()
                break

            if k == ord('c'):

                casilla = inv_cambio_posicion(raw_input("Casilla: "))

                for j in Listas.rectify_squares[casilla]:
                    cv2.circle(sub_img, tuple(j), 5, (0, 0, 255), -1)

            cv2.namedWindow('main',  cv2.WINDOW_NORMAL)
            cv2.imshow('main', sub_img)


class Calibration:
    def __init__(self, img):        # Image is a file
        self.tablero = ChessBoard(img)
        self.rectified_image = self.tablero.rectify_image(cv2.imread(img))
        self.tablero.rectify_chessboard(self.rectified_image)

    def rectify_image(self, img):       # Image is not a file
        self.rectified_image = self.tablero.rectify_image(img)
        return self.rectified_image


class Detection:
    def __init__(self, patch1, patch2, jugador):        # Images are files
        self.tablero = ChessBoard(patch1, False, Listas.esquinas)

        self.patch1 = patch1
        self.patch2 = patch2

        self.jugador = jugador

    def Tablero(self):
        pts = []

        img_1 = self.tablero.rectify_image(cv2.imread(self.patch1))
        img_2 = self.tablero.rectify_image(cv2.imread(self.patch2))

        contornos, umbral, resta = self.Resta(img_1, img_2)

        areas = []

        for c in contornos:
            if cv2.contourArea(c) > 1000:
                areas.append(cv2.contourArea(c))

        try:
            max_areas = [max(areas), max(areas[0:areas.index(max(areas))])]

        except ValueError:
            if len(areas) == 2:
                max_areas = areas

            elif len(areas) == 1:
                return self.Casillas()

            else:
                areas.sort()
                max_areas = [areas[len(areas) - 1], areas[len(areas) - 2]]

        max_contornos = []

        for c in contornos:
            for a in max_areas:
                if cv2.contourArea(c) == a:
                    max_contornos.append(c)

        casillas = []

        for c in max_contornos:
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            centro = ((2 * x + w) / 2, (2 * y + h) / 2)
            pts.append(centro)

            cv2.circle(img_2, centro, 3, (255, 0, 0))

            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                exit(11)

            for punto in pts:
                for i in Listas.rectify_squares:
                    j = Listas.rectify_squares[i]

                    inf_izq = tuple(j[0])
                    sup_der = tuple(j[3])

                    if inf_izq[0] < punto[0] and inf_izq[1] < punto[1] and \
                       sup_der[0] > punto[0] and sup_der[1] > punto[1]:

                        if i not in casillas:
                            casillas.append(i)
        """
        cv2.imshow('%s' % img_2, img_2)
        cv2.imshow('umbral', umbral)
        cv2.imshow('resta', resta)

        k = cv2.waitKey(0)

        if k == 27:
            cv2.destroyAllWindows()
            exit(11)

        cv2.destroyWindow('%s' % img_2)
        cv2.destroyWindow('umbral')
        cv2.destroyWindow('resta')
        """
        lista = dict

        if len(casillas) == 1:
            return self.Casillas()

        if self.jugador == 1:
            lista = Listas.casillasOcupadas['Blancas']
        elif self.jugador == 2:
            lista = Listas.casillasOcupadas['Negras']

        if len(casillas) == 2:
            antes = tuple
            ahora = tuple

            for casilla in casillas:
                if casilla in lista:
                    antes = casilla
                elif casilla not in lista:
                    ahora = casilla
                else:
                    print "Error"

            try:
                return antes, ahora
            except KeyError:
                print casillas
                # exit(11)

        else:
            print len(casillas), casillas

    def Casillas(self):
        pass

    @staticmethod
    def Resta(img_1, img_2):
        kernel = np.ones((5, 5), np.uint8)

        gris_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        gris_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

        resta = cv2.absdiff(gris_1, gris_2)

        umbral = cv2.threshold(resta, 20, 255, cv2.THRESH_BINARY)[1]
        umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel)
        umbral = cv2.dilate(umbral, kernel, iterations=2)
        umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)

        contornos_img = umbral.copy()
        im, contornos, hierarchy = cv2.findContours(contornos_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contornos, umbral, resta
