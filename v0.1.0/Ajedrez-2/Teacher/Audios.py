# -*- coding: utf-8 -*-

from Sintetizador import Sts
import Instrucciones


class Spanish:
    def __init__(self):
        self.sts = Sts('spanish')
        self.say = self.sts.say

    def intro(self):
        self.say(u'Hola, soy Pict.')
        # self.say(u'Perdón por mi voz, pero creéme, me molesta más a mi que a ti.')
        # self.say(u'Empecemos.')

    def calibration(self, moment):
        if moment == 1:
            self.say(u'Comencemos calibrando la cámara.')
            self.say(u'Primero, coloca el tablero de modo que pueda ver las cuatro esquinas.')
            self.say(u'Cuando lo hayas hecho, pulsa énter')
        elif moment == 2:
            self.say(u'Ahora haz click en las cuatro esquinas siguiendo las instrucciones.')
            Instrucciones.calibration()

    def arduino(self, signal):
        if signal:
            self.say(u'Hay conexión con Arduino.')
        else:
            self.say(u'No hay conexión con Arduino.')

    def partida(self):
        self.say(u'Recuerda que los reyes van en la columna E.')
        self.say(u'Comienzan las blancas.')

    def jugada(self, pieza, posicion, comida):
        if comida:
            self.say(u'%s por %s' % (pieza, posicion))
        else:
            self.say(u'%s a %s' % (pieza, posicion))

    class Consejo:
        def __init__(self):
            self.peones_1 = u'No muevas tanto los peones, no tengas miedo a usar las figuras.'
            self.peones_2 = u'Usa más los peones.'
            self.caballo = u'Para que los caballos tengan más movilidad, intenta mantenerlos en el \n' \
                           u'centro del tablero y no llevarlos a los lados.'

    def jaque_mate(self, jugador, turno):
        self.say('Jaque mate, ganan %s en el turno %s, felicidades.' % (jugador, turno))
