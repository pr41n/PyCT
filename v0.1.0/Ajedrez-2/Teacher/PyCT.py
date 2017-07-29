# -*- coding: cp1252 -*-

import cv2

import Piezas
from Functions import *
from Sintetizador import Sts
from Ventana import OpenCV, Ventana
from Video import Detection, Calibration, Camera

clean = Clean()
calibration = 0


class PyCT:
    global calibration

    def __init__(self, probando=False):

        self.win = Ventana()
        self.win.main()

        if probando:
            self.prueba()

        self.audio = Spanish()
        self.consejos = self.audio.Consejo()
        self.sts = Sts('spanish')

        intro = thread_starter(self.audio.intro)
        intro.join()

        camera = Camera()
        cam_chosen = camera.choose()
        self.cam = cv2.VideoCapture(cam_chosen)

        thread_starter(self.audio.calibration, [1])

        attempt1 = True
        while True:
            if self.calibrated(attempt1):
                break
            attempt1 = False

        clean.images()

        self.bien, self.mal, self.jaque_mate = self.arduino_conection()

        self.jugador = 1
        self.turno = 1
        self.partida = True

        self.advice = False
        self.n_peones_1 = 0
        self.n_peones_2 = 0
        self.n_caballo = 0
        self.consejo = str

        thread_starter(self.audio.partida)

        global antes, ahora

        while self.partida:
            antes, ahora = self.detect_move()

            try:
                ficha, movimiento, casillasOcupadas = self.detect_piece(antes, ahora)
                self.check_move(ficha, movimiento, casillasOcupadas)

            except KeyError or AttributeError as err:
                print u"Error en la detección: {}".format(err)
                self.sts.say(u"Ha habido un error en la detección")

    def calibrated(self, first_attempt=True):
        global calibration
        ventana = OpenCV.ventana('Coloca el tablero', 1100, -100, 440, 350)

        while True:
            k = cv2.waitKey(1) & 0xFF

            ret, frame = self.cam.read()
            cv2.imshow('Coloca el tablero', frame)
            # cv2.imshow('Coloca el tablero', cv2.imread('foto.jpg'))
            cv2.imwrite('PythonCache/frame.jpg', frame)
            self.win.video('PythonCache/frame.jpg')

            if k == 10:
                cv2.destroyWindow('Coloca el tablero')
                if first_attempt:
                    thread_starter(audio.calibration, [2])
                    self.win.calibration_instructions()

                cv2.imwrite('PythonCache/Tablero.jpg', frame)
                calibration = Calibration('PythonCache/Tablero.jpg')
                cv2.destroyWindow('Calibrate')
                break

            video_exit(k)

        return calibration.value()

    def arduino_conection(self):
        try:
            from Connection import Arduino
            arduino = Arduino(2)

            thread_starter(self.audio.arduino(True))
            delay = 0

            return 'arduino.write(\'a\', %s)' % delay, \
                   'arduino.write(\'b\', %s)' % delay, \
                   'arduino.write(\'c\', %s)' % delay

        except OSError:
            return 'None', 'None', 'None'

    def detect_move(self):
        global antes, ahora, calibration
        try:
            move = False
            OpenCV.ventana('PyCT', 1100, -100, 440, 350)
            while True:
                k = cv2.waitKey(1)

                ret, frame = self.cam.read()
                img = calibration.rectify_image(frame)
                cv2.imshow('PyCT', img)
                cv2.imwrite('PythonCache/frame.jpg', img)
                self.win.video('PythonCache/frame.jpg')

                video_exit(k)

                if k == 32 and not move:
                    move = True
                    cv2.imwrite('PythonCache/origin.jpg', frame)
                    original = 'PythonCache/origin.jpg'

                elif k == 32 and move:
                    cv2.imwrite('PythonCache/now.jpg', frame)
                    now = 'PythonCache/now.jpg'

                    detection = Detection(original, now, self.jugador)
                    antes, ahora = detection.Tablero()
                    return antes, ahora

                elif k == 27:
                    antes, ahora = self.win.movimiento(None)
                    return antes, ahora

        except cv2.error:
            thread_starter(sts.say, [u"Error de detección, introduzca el movimiento manulamente"])
            antes, ahora = self.win.movimiento(None)
            return antes, ahora

    def detect_piece(self, antes, ahora):
        movimiento = bool
        ficha = str

        try:
            """Se compara la posición inicial con las casillas ocupadas
            para reconocer qué pieza se ha movido.
            """
            casillas_ocupadas = Listas.casillas_ocupadas()
            piece = casillas_ocupadas[antes]
            #

            if piece == "Pawn":
                from Piezas import Pawn
                movimiento = Pawn()
                ficha = "Pawn"

                self.n_peones_1 += 1
                if self.turno <= 15 and self.n_peones_1 == 9:
                    self.advice = True
                    self.consejo = consejos.peones_1

            elif piece == "Rock":
                from Piezas import Rock
                movimiento = Rock()
                ficha = "Rock"
                self.n_peones_2 += 1

            elif piece == "Knight":
                from Piezas import Knight
                movimiento = Knight()
                ficha = "Knight"
                self.n_peones_2 += 1

                if ahora[0] == 1 or ahora[0] == 8or ahora[1] == 1 or ahora[1] == 8:
                    self.n_caballo += 1
                    if self.n_caballo < 3:
                        self.advice = True
                        self.consejo = consejos.caballo

            elif piece == "Bishop":
                from Piezas import Bishop
                movimiento = Bishop()
                ficha = "Bishop"
                self.n_peones_2 += 1

            elif piece == "Queen":
                from Piezas import Queen
                movimiento = Queen()
                ficha = "Queen"
                self.n_peones_2 += 1

            elif piece == "King":
                from Piezas import King
                movimiento = King()
                ficha = "King"
                self.n_peones_2 += 1

            if self.n_peones_2 == 6:
                self.consejo = consejos.peones_2
                self.n_peones_2 += 1

            return ficha, movimiento, casillas_ocupadas

        except KeyError or AttributeError:
            print u"Error: Fallo de detección"
            self.sts.say(u'Ha habido un error en la detección')

    def check_move(self, ficha, movimiento, casillas_ocupadas):
        global antes, ahora
        Piezas.jugador = self.jugador

        if movimiento.movimiento(antes[0], antes[1], ahora[0], ahora[1]):

            H = str
            J = int

            if ficha == "King" and antes[0] == 5 and ahora[1] - antes[1] == 0 and abs(ahora[0] - antes[0]) == 2:
                if ahora[0] == 3:
                    J = thread_starter(self.sts.say, ['Enroque largo.'])
                    H = u"Turno %s          Jugador %s          Enroque largo" % (self.turno, self.jugador)

                elif ahora[0] == 7:
                    J = thread_starter(self.sts.say, ['Enroque corto.'])
                    H = u"Turno %s          Jugador %s          Enroque corto" % (self.turno, self.jugador)

            elif ahora in casillas_ocupadas:
                J = thread_starter(audio.jugada, [cambio_ficha(ficha), cambio_posicion(ahora), True])
                H = u"Turno %s          Jugador %s          %s por %s" % \
                    (self.turno, self.jugador, cambio_ficha(ficha), cambio_posicion(ahora))

            else:
                J = thread_starter(self.audio.jugada, [cambio_ficha(ficha), cambio_posicion(ahora), False])
                H = u"Turno %s          Jugador %s          %s a %s" % \
                    (self.turno, self.jugador, cambio_ficha(ficha), cambio_posicion(ahora))

            self.win.print_move(H)

            # J.join()
            if self.advice:
                self.sts.say(self.consejo)
                self.advice = False

            #

            cambio_listas(ficha, antes, ahora, self.jugador)
            self.win.refresh_playing()
            self.turno += 1

            #

            if self.jugador == 1:
                if "King" not in Listas.PiezasMayores_N:
                    self.partida = False
                else:
                    self.jugador = 2

            elif self.jugador == 2:
                if "King" not in Listas.PiezasMayores_B:
                    self.partida = False
                else:
                    self.jugador = 1

            eval(self.bien)

        else:
            self.sts.say(u'Repite el movimiento')
            eval(self.mal)

    def prueba(self):
        camera = Camera()
        cam_chosen = camera.choose()
        self.cam = cv2.VideoCapture(cam_chosen)
        self.jugador = 1

        self.calibrated(False)

        antes, ahora = self.detect_move()
        print antes, ahora
        exit(11)

if __name__ == '__main__':
    pyct = PyCT()
