# -*- coding: cp1252 -*-

from time import sleep

import Listas
from Sintetizador import Sts

jugador = int
inicio = False

sts = Sts(inicio)


def incorrecta(respuesta):
    print
    print "Jugada incorrecta:"
    print respuesta
    sts.say("Jugada incorrecta")
    sts.say(respuesta)


def salto(antes_x, antes_y, ahora_x, ahora_y):
    casillas_ocupadas = Listas.casillas_ocupadas()

    if abs(ahora_x - antes_x) == 1 or abs(ahora_y-antes_y) == 1:
        return False

    elif antes_x == ahora_x:
        a = min(antes_y, ahora_y) + 1
        b = max(antes_y, ahora_y)

        for i in range(a, b):
            j = (antes_x, i)
            if j in casillas_ocupadas:
                return True

    elif antes_y == ahora_y:
        a = min(antes_x, ahora_x) + 1
        b = max(antes_x, ahora_x)

        for i in range(a, b):
            j = (i, antes_y)
            if j in casillas_ocupadas:
                return True

    elif abs(ahora_x-antes_x) == abs(ahora_y-antes_y):
        h = abs(ahora_x-antes_x)

        if antes_x < ahora_x and antes_y > ahora_y or antes_x > ahora_x and antes_y < ahora_y:
            a = max(antes_x, ahora_x)
            b = min(antes_y, ahora_y)

            for i in range(1, h):
                j = (a-i, b+i)
                if j in casillas_ocupadas:
                    return True

        else:
            a = min(antes_x, ahora_x)
            b = min(antes_y, ahora_y)

            for i in range(1, h):
                j = (a+i, b+i)
                if j in casillas_ocupadas:
                    return True


class Pawn:
    def movimiento(self, antes_x, antes_y, ahora_x, ahora_y):
        ahora = (ahora_x, ahora_y)

        lista_b = Listas.casillasOcupadas['Blancas']
        lista_n = Listas.casillasOcupadas['Negras']

        avance_x = ahora_x-antes_x
        avance_y = ahora_y-antes_y

        def comida():
            if (ahora in lista_b) or (ahora in lista_n):
                return True

            else:
                return False

        move_1 = (avance_y == 1 or avance_y == 2 and antes_y == 2) and jugador == 1
        move_2 = (avance_y == -1 or avance_y == -2 and antes_y == 7) and jugador == 2

        respuesta = u"El peón avanza en línea recta y solo una fila por movimiento y\n" \
                    u"come en diagonal y avanzando una fila. Si es la primera vez que\n" \
                    u"mueves al peón, este puede avanzar dos casillas en línea recta"

        if move_1 or move_2:
            if not salto(antes_x, antes_y, ahora_x, ahora_y):

                if avance_x == 0 and not comida() or abs(avance_x) == 1 and comida():
                    return True

                else:
                    incorrecta(respuesta)
                    return False
            else:
                incorrecta(u"La única pieza que puede saltar a otras es el caballo")
        else:
            if salto(antes_x, antes_y, ahora_x, ahora_y):
                pass
            else:
                incorrecta(respuesta)
            return False


class Rock:
    def movimiento(self, antes_x, antes_y, ahora_x, ahora_y):
        move_1 = abs(ahora_y-antes_y) > 0 and ahora_x-antes_x == 0
        move_2 = abs(ahora_x-antes_x) > 0 and ahora_y-antes_y == 0

        if move_1 or move_2:
            if not salto(antes_x, antes_y, ahora_x, ahora_y):

                return True
            else:
                incorrecta(u"La única pieza que puede saltar a otras es el caballo")

        else:
            respuesta = u"La torre se mueve en línea recta"
            incorrecta(respuesta)
            return False


class Knight:
    def movimiento(self, antes_x, antes_y, ahora_x, ahora_y):

        move_1 = abs(ahora_y-antes_y) == 1 and abs(ahora_x-antes_x) == 2
        move_2 = abs(ahora_y-antes_y) == 2 and abs(ahora_x-antes_x) == 1

        if move_1 or move_2:

            return True
        else:
            respuesta = u"El caballo se mueve dos casillas horizontalmente y una vertical o viceversa, \n" \
                        u"de modo que forme una L"
            incorrecta(respuesta)
            return False


class Bishop:
    def movimiento(self, antes_x, antes_y, ahora_x, ahora_y):
        move = abs(ahora_x-antes_x) == abs(ahora_y-antes_y)

        if move:
            if not salto(antes_x, antes_y, ahora_x, ahora_y):

                return True
            else:
                incorrecta(u"La única pieza que puede saltar a otras es el caballo")

        else:
            respuesta = u"El alfil se mueve en diagonal"
            incorrecta(respuesta)
            return False


class Queen:
    def movimiento(self, antes_x, antes_y, ahora_x, ahora_y):
        move_1 = abs(ahora_y - antes_y) > 0 and ahora_x - antes_x == 0
        move_2 = abs(ahora_x - antes_x) > 0 and ahora_y - antes_y == 0
        move_3 = abs(ahora_x - antes_x) == abs(ahora_y - antes_y)

        if move_1 or move_2 or move_3:
            if not salto(antes_x, antes_y, ahora_x, ahora_y):

                return True
            else:
                incorrecta(u"La única pieza que puede saltar a otras es el caballo")

        else:
            respuesta = u"La reina se mueve como un alfil y una torre a la vez, es decir,\nrecto o en diagonal"
            incorrecta(respuesta)
            return False


class King:
    def movimiento(self, antes_x, antes_y, ahora_x, ahora_y):
        """
        El enroque solo toma el movimiento del rey, 
        el programa se duerme un tiempo para permitir al jugador mover la torre
        """
        move_1 = abs(ahora_x-antes_x)
        move_2 = abs(ahora_y-antes_y)

        if (move_1 == 1 or move_1 == 0) and (move_2 == 1 or move_2 == 0):

            return True

        elif move_1 == 2 and move_2 == 0:

            if antes_x == 5 and not salto(antes_x, antes_y, ahora_x, ahora_y):

                if jugador == 1:

                    if ahora_x == 7 and Listas.casillasOcupadas['Blancas'][(8, 1)] == "Rock":

                        del Listas.casillasOcupadas['Blancas'][(8, 1)]
                        Listas.casillasOcupadas['Blancas'][(6, 1)] = "Rock"

                    elif ahora_x == 3 and Listas.casillasOcupadas['Blancas'][(1, 1)] == "Rock":

                        del Listas.casillasOcupadas['Blancas'][(1, 1)]
                        Listas.casillasOcupadas['Blancas'][(4, 1)] = "Rock"

                #

                elif jugador == 2:

                    if ahora_x == 7 and Listas.casillasOcupadas['Negras'][(8, 8)] == "Rock":

                        del Listas.casillasOcupadas['Negras'][(8, 8)]
                        Listas.casillasOcupadas['Negras'][(6, 8)] = "Rock"

                    elif ahora_x == 3 and Listas.casillasOcupadas['Negras'][(1, 8)] == "Rock":

                        del Listas.casillasOcupadas['Negras'][(1, 8)]
                        Listas.casillasOcupadas['Negras'][(4, 8)] = "Rock"

                sleep(2)

                return True

            else:
                respuesta = u"El rey solo puede enrocar si ni él ni la torre del lado en el que se va a enrocar" \
                            u" se han movido antes,\npor lo que es en la misma fila. Además, no debe\n" \
                            u"haber ninguna pieza entre la torre y el rey. Existen dos enroques:\n" \
                            u"   Enroque corto: el rey se mueve a la columna G y la torre a la F \n" \
                            u"   Enroque largo: el rey se mueve a la columna C y la torre a la D"
                if salto(antes_x, antes_y, ahora_x, ahora_y):
                    pass
                else:
                    incorrecta(respuesta)
                return False

        else:
            respuesta = u"El rey puede avanzar una casilla en todas direcciones"
            incorrecta(respuesta)
            return False
