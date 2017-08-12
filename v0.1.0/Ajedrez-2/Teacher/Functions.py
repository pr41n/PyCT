# -*- coding: cp1252 -*-

import threading
import time

import Lists
import Memory
from Audios import Spanish
from Cleaner import Clean
from Synthesizer import Sts

audio = Spanish()
consejos = audio.Consejo()
sts = Sts('spanish')


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
    if a.lower() == "torre":
        a = "Rock"
    elif a.lower() == "caballo":
        a = "Knight"
    elif a.lower() == "alfil":
        a = "Bishop"
    elif a.lower() == "reina":
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
    columna = str
    fila = str(position[1])

    if position[0] == 1:
        columna = "A"
    elif position[0] == 2:
        columna = "B"
    elif position[0] == 3:
        columna = "C"
    elif position[0] == 4:
        columna = "D"
    elif position[0] == 5:
        columna = "E"
    elif position[0] == 6:
        columna = "F"
    elif position[0] == 7:
        columna = "G"
    elif position[0] == 8:
        columna = "H"

    return columna + fila


def inv_cambio_posicion(position):
    """
    Traducción de la posición de las piezas humano-máquina.
    Sirve para insertar los movimientos a mano.
    Mismo objetivo que la función anterior.

    :param position: posición columna-fila
    :return: posición coordenadas
    """
    x = int
    y = eval(position[1])

    if position[0].upper() == "A":
        x = 1
    elif position[0].upper() == "B":
        x = 2
    elif position[0].upper() == "C":
        x = 3
    elif position[0].upper() == "D":
        x = 4
    elif position[0].upper() == "E":
        x = 5
    elif position[0].upper() == "F":
        x = 6
    elif position[0].upper() == "G":
        x = 7
    elif position[0].upper() == "H":
        x = 8

    return tuple([x, y])


def cambio_listas(which, e0, ef, jugador, p):
    """
    Se llama cuando la jugada es correcta.

    :param jugador:
    :param which: pieza que se ha movido
    :param e0: posición inicial de la pieza
    :param ef: posición final de la pieza
    :param p: en caso de coronación la pieza que se escoge
    :return: cambio de listas
    """

    mayores_1, menores_1, mayores_2, menores_2 = give_values(list, 4)
    lista_1, lista_2 = give_values(dict, 2)
    compar_1, compar_2 = give_values(str, 2)

    #

    if jugador == 1:
        lista_1 = Lists.casillasOcupadas['Blancas']
        lista_2 = Lists.casillasOcupadas['Negras']

        mayores_1 = Lists.PiezasMayores_B
        menores_1 = Lists.PiezasMenores_B

        mayores_2 = Lists.PiezasMayores_N
        menores_2 = Lists.PiezasMenores_N

        compar_1 = "ef[0] <= 4"
        compar_2 = "ef[0] > 4"

    elif jugador == 2:
        lista_1 = Lists.casillasOcupadas['Negras']
        lista_2 = Lists.casillasOcupadas['Blancas']

        mayores_1 = Lists.PiezasMayores_N
        menores_1 = Lists.PiezasMenores_N

        mayores_2 = Lists.PiezasMayores_B
        menores_2 = Lists.PiezasMenores_B

        compar_1 = "ef[0] >= 4"
        compar_2 = "ef[0] < 4"

    #

    del lista_1[e0]

    if which == "Pawn" and (ef[1] == 1 or ef[1] == 8):
        p = inv_cambio_ficha(p)

        lista_1[ef] = p
        mayores_1.append(p)

        if "Pawn_%s" % ef[0] in menores_1:
            menores_1.remove("Pawn_%s" % ef[0])

        else:
            for i in range(1, 9):

                j = "Pawn_%s" % i
                if j in menores_1:

                    menores_1.remove(j)
                    break

    else:
        lista_1[ef] = which

    if ef in lista_2:
        pieza_comida = lista_2[ef]
        del lista_2[ef]

        if pieza_comida == "Pawn":

            if "Pawn_%s" % ef[0] in menores_2:
                menores_2.remove("Pawn_%s" % ef[0])

            else:
                for i in range(1, 9):

                    j = "Pawn_%s" % i
                    if j in menores_2:
                        menores_2.remove(j)
                        break

        elif pieza_comida == "Rock":
            if eval(compar_1):
                mayores_2.remove("Rock_2")

            elif eval(compar_2):
                mayores_2.remove("Rock_1")

        elif pieza_comida == "Knight":
            if eval(compar_1):
                mayores_2.remove("Knight_2")

            elif eval(compar_2):
                mayores_2.remove("Knight_1")

        elif pieza_comida == "Bishop":
            if eval(compar_1):
                mayores_2.remove("Bishop_2")

            elif eval(compar_2):
                mayores_2.remove("Bishop_1")

        elif pieza_comida == "Queen":
            mayores_2.remove("Queen")

        elif pieza_comida == "King":
            mayores_2.remove("King")
        else:
            print "error"
            print pieza_comida
            print lista_2


def thread_starter(to_thread, args=()):
    thread = threading.Thread(target=to_thread, args=args)
    thread.setDaemon(True)
    thread.start()
    return thread


def video_exit(k):
    if k == ord('m'):
        Memory.main()

    elif k == 227:
        Clean.images()
        Clean.pyc()
        exit(11)

    elif k == ord('t'):
        print threading.activeCount()


def prevent_auido_error(texto):
    try:
        sts.say(texto)
    except RuntimeError:
        time.sleep(0.1)
        prevent_auido_error(texto)


def give_values(value, num):
    A = []
    for x in range(num):
        A.append(value)
    return A
