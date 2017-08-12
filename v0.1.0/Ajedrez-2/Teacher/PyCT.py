# -*- coding: cp1252 -*-

import cv2

import Pieces
from Functions import *
from Synthesizer import Sts
from Window import OpenCV, Ventana
from Video import Detection, Calibration, Camera

clean = Clean()
calibration, pos0, pos1 = give_values(None, 3)
rectified = False
z = True


class PyCT:
    def __init__(self, probando=False):

        self.win = Ventana()
        self.win.main()

        if probando:
            self.prueba()
            exit(12)

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

        self.win.label.set_text("")

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

        global pos0, pos1, rectified

        while self.partida:
            pos0, pos1 = self.detect_move()

            try:
                ficha, movimiento, casillasOcupadas = self.detect_piece()
                self.check_move(ficha, movimiento, casillasOcupadas)

            except KeyError as err:
                print u"Error en la detección: {}".format(err)
                self.sts.say(u"Error en la detección. Pulse cualquier tecla cuando haya  vuelto a colocar las piezas.")
                self.sts.say(u"Si prefieres introducir el movimiento manualmente, pulsa escape.")
                if cv2.waitKey(0) & 0xFF == 27:
                    pos0, pos1 = self.win.movimiento(None)
                    ficha, movimiento, casillasOcupadas = self.detect_piece()
                    self.check_move(ficha, movimiento, casillasOcupadas)

            except AttributeError as err:
                print u"Error en la detección: {}".format(err)
                self.sts.say(u"Error en la detección. Pulse cualquier tecla cuando haya  vuelto a colocar las piezas")
                self.sts.say(u"Si prefieres introducir el movimiento manualmente, pulsa escape.")
                if cv2.waitKey(0) & 0xFF == 27:
                    pos0, pos1 = self.win.movimiento(None)
                    ficha, movimiento, casillasOcupadas = self.detect_piece()
                    self.check_move(ficha, movimiento, casillasOcupadas)

            except TypeError as err:
                print u"Error en la detección: {}".format(err)
                self.sts.say(u"Error en la detección. Pulse cualquier tecla cuando haya  vuelto a colocar las piezas")
                self.sts.say(u"Si prefieres introducir el movimiento manualmente, pulsa escape.")
                if cv2.waitKey(0) & 0xFF == 27:
                    pos0, pos1 = self.win.movimiento(None)
                    ficha, movimiento, casillasOcupadas = self.detect_piece()
                    self.check_move(ficha, movimiento, casillasOcupadas)
        if self.jugador == 1: jugador = 'blancas'
        else: jugador = 'negras'

        thread_starter(prevent_auido_error, ['Jaque mate, ganan %s en el turno %s, felicidades.' %
                                             (jugador, self.turno - 1)])
        time.sleep(2)
        prevent_auido_error(" ")

        video_exit(227)

    def calibrated(self, first_attempt=True):
        global calibration
        OpenCV('Coloca el tablero', 1100, -100, 440, 350)

        while True:
            k = cv2.waitKey(1) & 0xFF

            ret, frame = self.cam.read()
            cv2.imshow('Coloca el tablero', frame)
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
        global pos0, pos1, calibration, rectified
        instructions = cv2.imread('Instructions/Video.png')
        try:
            move = False
            OpenCV('Sobre esta ventana pulsa:', 490, 485, 435, 170)
            while True:
                k = cv2.waitKey(1)

                ret, frame = self.cam.read()
                if k == ord('r'):
                    if rectified:
                        rectified = False
                    else:
                        rectified = True

                if rectified:
                    img = calibration.rectify_image(frame)
                else:
                    img = frame

                cv2.imshow('Sobre esta ventana pulsa:', instructions)
                cv2.imwrite('PythonCache/frame.jpg', img)
                self.win.video('PythonCache/frame.jpg')

                video_exit(k)

                if not move:
                    move = True
                    cv2.imwrite('PythonCache/origin.jpg', frame)
                    original = 'PythonCache/origin.jpg'

                elif k == 32 and move:
                    cv2.imwrite('PythonCache/now.jpg', frame)
                    now = 'PythonCache/now.jpg'

                    detection = Detection(original, now, self.jugador)
                    pos0, pos1 = detection.Tablero()
                    return pos0, pos1

                elif k == 27:
                    pos0, pos1 = self.win.movimiento(None)
                    return pos0, pos1

        except cv2.error:
            thread_starter(sts.say, [u"Error de detección, introduzca el movimiento manulamente"])
            pos0, pos1 = self.win.movimiento(None)
            return pos0, pos1

        except IndexError:
            thread_starter(sts.say, [u"Error de detección, introduzca el movimiento manulamente"])
            pos0, pos1 = self.win.movimiento(None)
            return pos0, pos1

    def detect_piece(self):
        movimiento = bool
        ficha = str

        try:
            """Se compara la posición inicial con las casillas ocupadas
            para reconocer qué pieza se ha movido.
            """
            casillas_ocupadas = Lists.casillas_ocupadas()
            piece = casillas_ocupadas[pos0]
            #

            if piece == "Pawn":
                from Pieces import Pawn
                movimiento = Pawn()
                ficha = "Pawn"

                self.n_peones_1 += 1
                if self.turno <= 15 and self.n_peones_1 == 9:
                    self.advice = True
                    self.consejo = consejos.peones_1

            elif piece == "Rock":
                from Pieces import Rock
                movimiento = Rock()
                ficha = "Rock"
                self.n_peones_2 += 1

            elif piece == "Knight":
                from Pieces import Knight
                movimiento = Knight()
                ficha = "Knight"
                self.n_peones_2 += 1

                if pos1[0] == 1 or pos1[0] == 8or pos1[1] == 1 or pos1[1] == 8:
                    self.n_caballo += 1
                    if self.n_caballo < 3:
                        self.advice = True
                        self.consejo = consejos.caballo

            elif piece == "Bishop":
                from Pieces import Bishop
                movimiento = Bishop()
                ficha = "Bishop"
                self.n_peones_2 += 1

            elif piece == "Queen":
                from Pieces import Queen
                movimiento = Queen()
                ficha = "Queen"
                self.n_peones_2 += 1

            elif piece == "King":
                from Pieces import King
                movimiento = King()
                ficha = "King"
                self.n_peones_2 += 1

            if self.n_peones_2 == 6:
                self.consejo = consejos.peones_2
                self.n_peones_2 += 1

            return ficha, movimiento, casillas_ocupadas

        except KeyError or AttributeError:
            print u"Error: Fallo de detección"

    def check_move(self, ficha, movimiento, casillas_ocupadas):
        global pos0, pos1
        Pieces.jugador = self.jugador

        if movimiento.movimiento_correcto(pos0[0], pos0[1], pos1[0], pos1[1]):

            H = "Turno %s" % self.turno, "Jugador %s" % self.jugador
            J = int
            K = None

            if ficha == "King" and pos0[0] == 5 and pos1[1] - pos0[1] == 0 and abs(pos1[0] - pos0[0]) == 2:
                if pos1[0] == 3:
                    J = thread_starter(self.sts.say, ['Enroque largo.'])
                    H = H, u"Enroque largo"

                elif pos1[0] == 7:
                    J = thread_starter(self.sts.say, ['Enroque corto.'])
                    H = H, u"Enroque corto"

            elif ficha == "Pawn" and (pos1[1] == 8 or pos1[1] == 1):
                K = self.win.corona()
                K = K.capitalize()
                J = thread_starter(self.sts.say, [u"%s corona" % cambio_ficha(K)])
                H = H, u"%s corona" % cambio_ficha(K)

            elif pos1 in casillas_ocupadas:
                J = thread_starter(audio.jugada, [cambio_ficha(ficha), cambio_posicion(pos1), True])
                H = H, u"%s por %s" % (cambio_ficha(ficha), cambio_posicion(pos1))

            else:
                J = thread_starter(self.audio.jugada, [cambio_ficha(ficha), cambio_posicion(pos1), False])
                H = H, u"%s a %s" % (cambio_ficha(ficha), cambio_posicion(pos1))

            self.win.print_move(H[0][0], H[0][1], H[1])

            if self.advice:
                J.join()
                thread_starter(self.sts.say, [self.consejo])
                self.advice = False

            #

            cambio_listas(ficha, pos0, pos1, self.jugador, K)
            self.win.refresh_playing(K, self.jugador)
            self.turno += 1

            #

            if self.jugador == 1:
                if "King" not in Lists.PiezasMayores_N:
                    self.partida = False
                else:
                    self.jugador = 2

            elif self.jugador == 2:
                if "King" not in Lists.PiezasMayores_B:
                    self.partida = False
                else:
                    self.jugador = 1

            eval(self.bien)

        else:
            global z
            self.win.print_incorrect_move()
            thread_starter(sts.say, [u'Repite el movimiento'])
            if z:
                z = False
                thread_starter(sts.say, [u'Cuando hayas devuelto las piezas a su posición inicial, '
                                         u'pulsa cualquier tecla para continuar'])
            cv2.waitKey(0)
            eval(self.mal)

    def prueba(self):
        import Pieces
        for i in range(4):
            Pieces.answer = "Prueba\n\n"
            self.win.print_incorrect_move()
            self.win.main()

if __name__ == '__main__':
    pyct = PyCT()
