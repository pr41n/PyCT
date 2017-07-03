# -*- coding: cp1252 -*-

import cv2
import sys

import Calibration
import Piezas
import Detection
from Listas import Listas
import Ventana
from Cleaner import Clean
from Sintetizador import Sts

# Set up

camera = 1
inicio = True

# Calling modules

clean = Clean()
sts = Sts(inicio)
sts.say('Empecemos.')


# Definig functions


def cambio_ficha(a):
    """
    Traducción inglés-español.

    :param a: pieza en inglés
    :return: pieza en español
    """
    if a == "Pawn":
        a = u"Peón"
    elif a == "Rock":
        a = "Torre"
    elif a == "Knight":
        a = "Caballo"
    elif a == "Bishop":
        a = "Alfil"
    elif a == "Queen":
        a = "Reina"
    elif a == "King":
        a = "Rey"

    return a


def inv_cambio_ficha(a):
    """
    Traducción español-inglés.
    Solo se usa en la coronación, por lo que no se traducen ni el peón ni el rey

    :param a: pieza en español
    :return: pieza en inglés
    """
    if a == "Torre":
        a = "Rock"
    elif a == "Caballo":
        a = "Knight"
    elif a == "Alfil":
        a = "Bishop"
    elif a == "Reina":
        a = "Queen"

    return a


def cambio_posicion(position):
    """
    Traducción de la posición de las piezas máquina-humano.
    Sirve para que que el movimiento se identifique mejor porlas personas.
    El objetivo de usar coordenadas es facilitar las operaciones de movimiento.

    :param position: posición coordenadas
    :return: posición columna-fila
    """
    posicion = ""

    if position[0] == 1:
        posicion = "A"
    elif position[0] == 2:
        posicion = "B"
    elif position[0] == 3:
        posicion = "C"
    elif position[0] == 4:
        posicion = "D"
    elif position[0] == 5:
        posicion = "E"
    elif position[0] == 6:
        posicion = "F"
    elif position[0] == 7:
        posicion = "G"
    elif position[0] == 8:
        posicion = "H"

    posicion = posicion + str(position[1])
    return posicion


def inv_cambio_posicion(position):
    """
    Traducción de la posición de las piezas humano-máquina.
    Sirve para insertar los movimientos a mano.
    Mismo objetivo que la función anterior.

    :param position: posición columna-fila
    :return: posición coordenadas
    """
    x = ""

    if position[0].upper() == "A":
        x = "1"
    elif position[0].upper() == "B":
        x = "2"
    elif position[0].upper() == "C":
        x = "3"
    elif position[0].upper() == "D":
        x = "4"
    elif position[0].upper() == "E":
        x = "5"
    elif position[0].upper() == "F":
        x = "6"
    elif position[0].upper() == "G":
        x = "7"
    elif position[0].upper() == "H":
        x = "8"

    posicion = "(%s,%s)" % (x, position[1])

    return eval(posicion)


def cambio_listas(which, e0, ef):
    """
    Se llama cuando la jugada es correcta.

    :param which: pieza que se ha movido
    :param e0: posición inicial de la pieza
    :param ef: posición final de la pieza
    :return: cambio de listas
    """

    if jugador == 1:
        del Listas.casillasOcupadas_B[e0]

        if which == "Pawn" and ef[1] == 8:
            p = raw_input("Pieza: ")
            p = p[0].upper() + p[1:].lower()
            p = inv_cambio_ficha(p)
            Listas.casillasOcupadas_B[ef] = p
            Listas.PiezasMayores_B.append(p)

            for i in range(9):

                j = "Pawn_%s" % i
                if j in Listas.PiezasMenores_B:

                    Listas.PiezasMenores_B.remove(j)
                    break

        else:
            Listas.casillasOcupadas_B[ef] = which

        if ef in Listas.casillasOcupadas_N:

            pieza_c = Listas.casillasOcupadas_N[ef]
            del Listas.casillasOcupadas_N[ef]

            if pieza_c == "Pawn":

                for i in range(9):

                    j = "Pawn_%s" % i
                    if j in Listas.PiezasMenores_N:

                        Listas.PiezasMenores_N.remove(j)
                        break

            elif pieza_c == "Rock":
                if ef[0] < 4:
                    Listas.PiezasMayores_N.remove("Rock_2")

                elif ef[0] >= 4:
                    Listas.PiezasMayores_N.remove("Rock_1")

            elif pieza_c == "Knight":
                if ef[0] < 4:
                    Listas.PiezasMayores_N.remove("Knight_2")

                elif ef[0] >= 4:
                    Listas.PiezasMayores_N.remove("Knight_1")

            elif pieza_c == "Bishop":
                if ef[0] < 4:
                    Listas.PiezasMayores_N.remove("Bishop_2")

                elif ef[0] >= 4:
                    Listas.PiezasMayores_N.remove("Bishop_1")

            elif pieza_c == "Queen":
                Listas.PiezasMayores_N.remove("Queen")

            elif pieza_c == "King":
                Listas.PiezasMayores_N.remove("King")
            else:
                print "error"
                print pieza_c
                print Listas.casillasOcupadas_N

    elif jugador == 2:
        del Listas.casillasOcupadas_N[e0]

        if which == "Pawn" and ef[1] == 1:
            p = raw_input("Pieza: ")
            p = p[0].upper() + p[1:].lower()
            p = inv_cambio_ficha(p)
            Listas.casillasOcupadas_N[ef] = p

            for i in range(9):

                j = "Pawn_%s" % i
                if j in Listas.PiezasMenores_N:

                    Listas.PiezasMenores_N.remove(j)
                    break

            Listas.PiezasMenores_B.append(p)

        else:
            Listas.casillasOcupadas_N[ef] = which

        if ef in Listas.casillasOcupadas_B:

            pieza_c = Listas.casillasOcupadas_B[ef]
            del Listas.casillasOcupadas_B[ef]

            if pieza_c == "Pawn":
                for i in range(9):

                    j = "Pawn_%s" % i
                    if j in Listas.PiezasMenores_B:

                        Listas.PiezasMenores_B.remove(j)
                        break

            elif pieza_c == "Rock":
                if ef[0] > 4:
                    Listas.PiezasMayores_B.remove("Rock_2")

                elif ef[0] < 4:
                    Listas.PiezasMayores_B.remove("Rock_1")

            elif pieza_c == "Knight":
                if ef[0] > 4:
                    Listas.PiezasMayores_B.remove("Knight_2")

                elif ef[0] < 4:
                    Listas.PiezasMayores_B.remove("Knight_1")

            elif pieza_c == "Bishop":
                if ef[0] > 4:
                    Listas.PiezasMayores_B.remove("Bishop_2")

                elif ef[0] < 4:
                    Listas.PiezasMayores_B.remove("Bishop_1")

            elif pieza_c == "Queen":
                Listas.PiezasMayores_B.remove("Queen")

            elif pieza_c == "King":
                Listas.PiezasMayores_B.remove("King")
            else:
                print "error"
                print pieza_c
                print Listas.casillasOcupadas_B


cam = cv2.VideoCapture(camera)


# Calibrating the camera

sts.say(u'Comencemos calibrando la cámara.')
sts.say(u'Primero, coloca el tablero de modo que yo pueda '
        u'ver las cuatro esquinas, cuando lo hayas hecho, presiona énter.')
while True:

    k = cv2.waitKey(1) & 0xFF

    calibration = Calibration.Calibrate('Coloca el tablero', 1100, -100, 500, 400, cam)
    ret, frame = cam.read()
    cv2.imshow('Coloca el tablero', frame)

    if k == 10:
        sts.say(u'Muy bien. Ahora, señala las cuatro esquinas siguiendo mis instrucciones.')

        calibration.esquinas('Coloca el tablero')
        calibration.casillas()
        break

    if k == ord('q'):
        break

cam.release()

try:
    pass

except cv2.error:
    print u"Fallo de detección"

clean.images()
cv2.destroyWindow('Calibrate')


# Proofing the connection with Arduino and setting it up

try:
    from Connection import Arduino
    arduino = Arduino()
    arduino.inicio(0)

    delay = 0

    def bien():
        arduino.write('a', delay)

    def mal():
        arduino.write('b', delay)

    def jaque_mate():
        arduino.write('c', delay)

except OSError:
    """
    Esto no debería ocurrir si Arduino está conectado,
    es decir, en todos los casos. Pero si sucede, las funciones
    definidas acontinuación (bien, mal y jaque_mate) evitan un futuro error.
    """

    sts.say(u'Vaya, parece que no hay conexión con Arduino.')

    sts.say(u'Si deseas que la haya, por favor, conecta la placa de Arduino al ordenador, '
            u'sigue las instrucciones de conexión y reinicia el programa')

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
mover_peones = 0
mover_caballo = 0


# Reading the play

while partida:

    try:
        """
        if jugador == 1:
            Detection.Blancas()
        elif jugador == 2:
            Detection.Negras()
        """
        antes = Detection.antes()       # Se recogen las coordenadas de inicio
        ahora = Detection.ahora()       # Se recogen las coordenadas de destino

    except cv2.error:
        print u"Error de detección"

    try:
        # Asigna las coordenadas del movimiento.

        antes_X = antes[0]
        antes_Y = antes[1]
        ahora_X = ahora[0]
        ahora_Y = ahora[1]

    except TypeError or NameError:
        # Esto es una prueba, pero si ocurre permite introducir los movimientos por terminal.
        try:
            antes = raw_input("Antes: ")
            ahora = raw_input("Ahora: ")

        except KeyboardInterrupt:
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

        if jugador == 1:
            piece = Listas.casillasOcupadas_B[antes]

        elif jugador == 2:
            piece = Listas.casillasOcupadas_N[antes]

        #

        if piece == "Pawn":
            from Piezas import Pawn
            movimiento = Pawn()
            ficha = "Pawn"
            mover_peones += 1

            if turno <= 15 and mover_peones == 10:
                sts.say(u'No muevas tanto los peones, intenta mover más las piezas mayores')

        elif piece == "Rock":
            from Piezas import Rock
            movimiento = Rock()
            ficha = "Rock"

        elif piece == "Knight":
            from Piezas import Knight
            movimiento = Knight()
            ficha = "Knight"

            mal_1 = ahora_X == 1 or ahora_X == 8
            mal_2 = ahora_Y == 1 or ahora_Y == 8

            if mover_caballo == 0 and (mal_1 or mal_2):
                sts.say(u'Intenta no mover los caballos a los lados, tienen menos movilidad.'
                        u'Mejor, intenta que estén por el centro del tablero.')
                mover_caballo += 1

        elif piece == "Bishop":
            from Piezas import Bishop
            movimiento = Bishop()
            ficha = "Bishop"

        elif piece == "Queen":
            from Piezas import Queen
            movimiento = Queen()
            ficha = "Queen"

        elif piece == "King":
            from Piezas import King
            movimiento = King()
            ficha = "King"

        #
        #

        Piezas.jugador = jugador

        if movimiento.movimiento(antes_X, antes_Y, ahora_X, ahora_Y):

            # Se reconoce si el movimiento es correcto

            bien()
            print

            #
            #

            if ficha == "King" and antes_X == 5 and ahora_Y-antes_Y == 0 and abs(ahora_X-antes_X) == 2:

                if Listas.casillasOcupadas_B[(4, 1)] == "Rock" or Listas.casillasOcupadas_N[(4, 8)] == "Rock":

                    print "Turno%s  Jugador %s  Enroque largo" % (turno, jugador)
                    sts.say('Enroque largo.')

                elif Listas.casillasOcupadas_B[(6, 1)] == "Rock" or Listas.casillasOcupadas_N[(6, 8)] == "Rock":

                    print "Turno%s  Jugador %s  Enroque corto" % (turno, jugador)
                sts.say('Enroque corto.')

            #

            elif (ahora in Listas.casillasOcupadas_N) or \
                    (ahora in Listas.casillasOcupadas_B):

                print "Turno %s  Jugador %s  %s por %s" % \
                      (turno, jugador, cambio_ficha(ficha), cambio_posicion(ahora))
                sts.say(u'%s por %s.' % (cambio_ficha(ficha), cambio_posicion(ahora)))

            #

            else:
                print "Turno %s  Jugador %s  %s a %s" % \
                      (turno, jugador, cambio_ficha(ficha), cambio_posicion(ahora))
                sts.say(u'%s a %s.' % (cambio_ficha(ficha), cambio_posicion(ahora)))

            #
            #

            cambio_listas(ficha, antes, ahora)

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

    except KeyError or AttributeError or antes == ahora:
        print u"Error: Fallo de detección"
        sts.say(u'Ha habido un error en la detección. Si por casualidad '
                u'ha movido el tablero sin querer, tendrá que reiniciar el programa.'
                u'Si no ha sido así, por favor, vuelva a hacer el movimiento.')
        sts.say(u'Lo siento, pero doy para lo que doy.')


jaque_mate()
turno -= 1

if jugador == 1:
    jugador = "blancas"

elif jugador == 2:
    jugador = "negras"

print "Jaque mate, ganan %s en el turno %s" % (jugador, turno)
sts.say("Jaque mate, ganan %s en el turno %s. Felicidades." % (jugador, turno))

# clean.pyc()

if __name__ != '__main__':
    Ventana.Ventana()
