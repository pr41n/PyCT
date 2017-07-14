# -*- coding: cp1252 -*-

import sys, cv2, serial

import Listas
import Piezas

from Ventana import OpenCV, Ventana
from Video import Calibration, Detection, Camera
from Audios import Spanish
from Cleaner import Clean
from Functions import cambio_listas, cambio_posicion, cambio_ficha, inv_cambio_posicion
from Sintetizador import Sts


# Choosing the camera

camera = Camera()
cam_chosen = camera.choose()
cam = cv2.VideoCapture(cam_chosen)


# Calling the cleaner of cache

clean = Clean()


# Calling the audio

audio = Spanish()
consejos = audio.Consejo()
sts = Sts('spanish')

audio.intro()

# Calibrating the camera

audio.calibration(1)
ventana = OpenCV.ventana('Coloca el tablero', 1100, -100, 500, 400)

while True:

    k = cv2.waitKey(1) & 0xFF

    ret, frame = cam.read()
    cv2.imshow('Coloca el tablero', frame)

    if k == 10:
        cv2.destroyWindow('Coloca el tablero')
        audio.calibration(2)
        cv2.imwrite('PythonCache/Tablero.jpg', frame)
        calibration = Calibration('PythonCache/Tablero.jpg')
        cv2.destroyWindow('Calibrate')
        break

    if k == ord('q') or k == 27:
        break

clean.images()


# Proofing the connection with Arduino and setting it up

try:
    from Connection import Arduino
    arduino = Arduino(2)

    audio.arduino(True)
    delay = 0

    def bien():
        arduino.write('a', delay)

    def mal():
        arduino.write('b', delay)

    def jaque_mate():
        arduino.write('c', delay)

except OSError:
    """
    Esto no debería ocurrir si Arduino está conectado. Pero si sucede, las funciones
    definidas acontinuación (bien, mal y jaque_mate) evitan un futuro error.
    """
    print u"No hay conexión con Arduino"
    audio.arduino(False)

    def bien():
        pass

    def mal():
        pass

    def jaque_mate():
        pass


# Starting

turno = 1
jugador = 1
partida = True

audio.partida()

advice = False
n_peones_1 = 0
n_peones_2 = 0
n_caballo = 0

# Reading the play

while partida:

    try:
        move = False
        OpenCV.ventana('PyCT', 1100, -100, 400, 400)
        while True:
            k = cv2.waitKey(1)

            ret, frame = cam.read()
            img = calibration.rectify_image(frame)
            cv2.imshow('PyCT', img)

            if k == 32 and not move:
                move = True
                cv2.imwrite('PythonCache/origin.jpg', frame)
                original = 'PythonCache/origin.jpg'

            elif k == 32 and move:
                cv2.imwrite('PythonCache/now.jpg', frame)
                now = 'PythonCache/now.jpg'

                detection = Detection(original, now, jugador)
                antes, ahora = detection.Tablero()

                break

            if k == 27:
                antes = tuple
                ahora = tuple
                break

            if k == 227:
                clean.images()
                clean.pyc()
                exit(11)

    except cv2.error:
        print u"Error de detección"

    try:
        # Asigna las coordenadas del movimiento.

        antes_X = antes[0]
        antes_Y = antes[1]
        ahora_X = ahora[0]
        ahora_Y = ahora[1]

    except TypeError or NameError:
        # Permite introducir los movimientos por terminal en caso de salida de la calibración o error.

        try:

            antes = raw_input("Antes: ")
            ahora = raw_input("Ahora: ")

        except KeyboardInterrupt:
            clean.images()
            clean.pyc()
            sys.exit(11)

        antes = inv_cambio_posicion(antes)
        ahora = inv_cambio_posicion(ahora)

        antes_X = antes[0]
        antes_Y = antes[1]
        ahora_X = ahora[0]
        ahora_Y = ahora[1]

    piece = str
    movimiento = bool
    ficha = str

    try:
        """
        Se compara la posición inicial con las casillas ocupadas
        para reconocer qué pieza se ha movido.
        """
        casillas_ocupadas = Listas.casillas_ocupadas()
        piece = casillas_ocupadas[antes]
        #

        if piece == "Pawn":
            from Piezas import Pawn
            movimiento = Pawn()
            ficha = "Pawn"

            n_peones_1 += 1
            if turno <= 15 and n_peones_1 == 9:
                advice = True
                consejo = consejos.peones_1

        elif piece == "Rock":
            from Piezas import Rock
            movimiento = Rock()
            ficha = "Rock"
            n_peones_2 += 1

        elif piece == "Knight":
            from Piezas import Knight
            movimiento = Knight()
            ficha = "Knight"
            n_peones_2 += 1

            if ahora_Y == 1 or ahora_Y == 8 or ahora_X == 1 or ahora_X == 8:
                n_caballo += 1
                if n_caballo < 3:
                    advice = True
                    consejo = consejos.caballo

        elif piece == "Bishop":
            from Piezas import Bishop
            movimiento = Bishop()
            ficha = "Bishop"
            n_peones_2 += 1

        elif piece == "Queen":
            from Piezas import Queen
            movimiento = Queen()
            ficha = "Queen"
            n_peones_2 += 1

        elif piece == "King":
            from Piezas import King
            movimiento = King()
            ficha = "King"
            n_peones_2 += 1

        if n_peones_2 == 6:
            consejo = consejos.peones_2
            n_peones_2 += 1

        #
        #

        Piezas.jugador = jugador

        if movimiento.movimiento(antes_X, antes_Y, ahora_X, ahora_Y):

            # Movimiento correcto

            bien()

            #
            #

            if ficha == "King" and antes_X == 5 and ahora_Y-antes_Y == 0 and abs(ahora_X-antes_X) == 2:

                if ahora_X == 3:

                    print "Turno %s  Jugador %s  Enroque largo" % (turno, jugador)
                    sts.say('Enroque largo.')

                elif ahora_X == 7:

                    print "Turno %s  Jugador %s  Enroque corto" % (turno, jugador)
                    sts.say('Enroque corto.')
            #

            elif ahora in casillas_ocupadas:

                print "Turno %s  Jugador %s  %s por %s" % \
                      (turno, jugador, cambio_ficha(ficha), cambio_posicion(ahora))
                audio.jugada(cambio_ficha(ficha), cambio_posicion(ahora), comida=True)

            #

            else:

                print "Turno %s  Jugador %s  %s a %s" % \
                      (turno, jugador, cambio_ficha(ficha), cambio_posicion(ahora))
                audio.jugada(cambio_ficha(ficha), cambio_posicion(ahora), comida=False)
            #
            #

            if advice:
                sts.say(consejo)
                advice = False
            cambio_listas(ficha, antes, ahora, jugador)

            #
            #

            if jugador == 1:
                if "King" not in Listas.PiezasMayores_N:
                    partida = False
                else:
                    jugador = 2

            elif jugador == 2:
                if "King" not in Listas.PiezasMayores_B:
                    partida = False
                else:
                    jugador = 1

            #
            #

            turno += 1

        else:

            mal()

        print

    #

    except antes == ahora or KeyError or AttributeError:
        print u"Error: Fallo de detección"


jaque_mate()

if jugador == 1:
    jugador = "blancas"

elif jugador == 2:
    jugador = "negras"

print "Jaque mate, ganan %s en el turno %s" % (jugador, turno - 1)
audio.jaque_mate(jugador, turno - 1)

clean.images()
clean.pyc()

if __name__ != '__main__':
    Ventana()
