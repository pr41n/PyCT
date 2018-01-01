#!/usr/bin/python
import cv2
import sys

sys.path.append('..')
from chess_2 import video


cam = cv2.VideoCapture(1)

while True:
    frame = cam.read()[1]
    cv2.imshow('Coloca', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 10:
        chessboard = video.Calibration(frame)
        cv2.destroyAllWindows()
        break

n = True
jugador = 1
rectified = False
while True:
    frame = cam.read()[1]

    if n:
        origin = frame
        n = False

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break

    if k == ord('r'):
        if rectified:
            rectified = False
        else:
            rectified = True

    if k == ord('a'):
        origin = frame

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.namedWindow('resta', cv2.WINDOW_NORMAL)
    cv2.namedWindow('umbral', cv2.WINDOW_NORMAL)

    if rectified:
        contornos, umbral, resta = video.Detection.diff(chessboard.rectify_image(origin), chessboard.rectify_image(frame))
        frame = chessboard.rectify_image(frame)
        hist1 = cv2.calcHist([chessboard.rectify_image(cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY, True))], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([chessboard.rectify_image(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, True))], [0], None, [256], [0, 256])

    else:
        contornos, umbral, resta = video.Detection.diff(origin, frame)
        hist1 = cv2.calcHist([cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])

    try:
        areas = []
        for c in contornos:
            if cv2.contourArea(c) > 1000:
                areas.append(cv2.contourArea(c))

        if len(areas) == 2:
            max_areas = areas
        else:
            areas.sort()
            max_areas = [areas[-1], areas[-2]]

        max_contours = []
        for c in contornos:
            for a in max_areas:
                if cv2.contourArea(c) == a:
                    max_contours.append(c)

        for c in max_contours:
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = ((2 * x + w) / 2, (2 * y + h) / 2)
            cv2.circle(frame, center, 3, (255, 0, 0))
    except IndexError:
        pass

    l = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    cv2.imshow('resta', resta)
    cv2.imshow('umbral', umbral)

    cv2.putText(frame, str(l), (300, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=1, thickness=2)
    cv2.imshow('frame', frame)

    if k == ord('w'):
        cv2.waitKey(0)
