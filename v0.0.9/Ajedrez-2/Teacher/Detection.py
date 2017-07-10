import cv2
import numpy as np


def detection(cam):

    cv2.namedWindow('original', cv2.WINDOW_NORMAL)
    cv2.moveWindow('original', 1100, -100)
    cv2.resizeWindow('original', 500, 400)

    lista = []

    b = False
    n = False

    while True:

        ret, frame = cam.read()
        # gris = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        blanco = cv2.cvtColor(frame, cv2.COLORMAP_WINTER)
        negro = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('original', frame)
        # cv2.imshow('gris', gris)

        k = cv2.waitKey(1)

        if b:
            cv2.imshow('Tablero Blanco', blanco)
            if k == ord('v'):
                b = False
                cv2.destroyWindow('Tablero Blanco')
        if n:
            cv2.imshow('Tablero Negro', negro)
            if k == ord('m'):
                n = False
                cv2.destroyWindow('Tablero Negro')

        if k == ord('b'):
            b = True

        elif k == ord('n'):
            n = True

        elif k == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


class Blancas:
    def __init__(self):
        detection()


class Negras:
    def __init__(self):
        detection()


from Listas import Listas


def antes():
    pass


def ahora():
    pass
