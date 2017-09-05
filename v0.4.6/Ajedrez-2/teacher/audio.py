# -*- coding: utf-8 -*-

from synth import Sts
from languages import Spanish as Sp, English as En, Italian as It
from func import prevent_auido_error, give_values

language = 'spanish'
sts = Sts(language)
instructions = Sp


class Language:
    aud_001, aud_002, aud_003, aud_004, aud_005, aud_006, aud_007, \
        aud_008, aud_009, aud_010, aud_011, aud_012, aud_013, aud_014, \
        aud_015, aud_016, aud_017, aud_018, aud_019, aud_020, aud_021, \
        aud_022, aud_023, aud_024, aud_025, aud_026, aud_027 = give_values(None, 27)

    def __init__(self):
        global language
        self.say = sts.say

    def intro(self):
        self.say(self.aud_001)
        # self.say(self.aud_002)

    def calibration(self, moment):
        if moment == 1:
            self.say(self.aud_003)
            self.say(self.aud_004)
            self.say(self.aud_005)
            self.say(self.aud_006)
        elif moment == 2:
            self.say(self.aud_007)
            self.say(self.aud_008)

    def arduino(self, signal):
        if signal:
            self.say(self.aud_009)
        else:
            self.say(self.aud_010)

    def match(self):
        prevent_auido_error(self.aud_011)
        prevent_auido_error(self.aud_012)
        prevent_auido_error(self.aud_013)

    def play(self, piece, position, eaten):
        if eaten:
            self.say(self.aud_014 % (piece, position))
        else:
            self.say(self.aud_015 % (piece, position))

    def error_1(self):
        self.say(self.aud_019)
        self.say(self.aud_020)

    def error_2(self):
        self.say(self.aud_021)

    def check_mate(self, player, turn):
        prevent_auido_error(self.aud_022 % (player, turn - 1))

    def promotion(self, piece):
        self.say(self.aud_023 % piece)

    def castling(self, side):
        if side.lower() == 'kingside':
            self.say(self.aud_024)

        elif side.lower() == 'queenside':
            self.say(self.aud_025)

    def repeat_move(self, first_time):
        self.say(self.aud_026)

        if first_time:
            self.say(self.aud_027)


class English(Language):
    @staticmethod
    def main():
        global language, sts, instructions
        language = 'english'
        sts = Sts(language)
        instructions = En

    aud_001 = "Hello, I'm Pyct."
    aud_002 = "I apologise for my voice."
    aud_003 = "Let's start calibrating the camera."
    aud_004 = "Set the chessboard in a way I can see the four inside corners."
    aud_005 = "I recommend you to move forward the furthest rooks."
    aud_006 = "When you have done it, press enter."
    aud_007 = "Now, click on the four corners following the instructions."
    aud_008 = "You can enlarge the window if you need to."
    aud_009 = "There is connection with Arduino."
    aud_010 = "There is no connection with Arduino."
    aud_011 = "The order is rook, knight and bishop."
    aud_012 = "Remember kings must be in the E column."
    aud_013 = "Whites start."
    aud_014 = "%s by %s"
    aud_015 = "%s to %s"
    aud_016 = "Don't move too many times the pawns, try moving other pieces."
    aud_017 = "Try using more the pawns."
    aud_018 = "To achieve a better mobility of the knights, try placing them in the center of the chessboard."
    aud_019 = "Detection error. Press any key when you have placed again the pieces."
    aud_020 = "If you prefer to input manually the move, press escape."
    aud_021 = "Detection error. Input the move manually."
    aud_022 = "Checkmate, %s has won at turn %s, congratulations!."
    aud_023 = "%s promotes."
    aud_024 = "Kingside castling."
    aud_025 = "Queenside castling."
    aud_026 = "Repeat the move."
    aud_027 = "When you have placed again the pieces, press any key."


class Spanish(Language):
    @staticmethod
    def main():
        global language, sts, instructions
        language = 'spanish'
        sts = Sts(language)
        instructions = Sp

    aud_001 = u"Hola, soy Pict."
    aud_002 = u"Lo siento por mi voz."
    aud_003 = u"Empecemos calibrando la cámara."
    aud_004 = u"Coloca el tablero de modo que pueda ver las cuatro esquinas interiores."
    aud_005 = u"Te recomiendo mover hacia delante las torres más alejadas."
    aud_006 = u"Cuando lo hayas hecho, pulsa énter."
    aud_007 = u"Ahora, haz click en las cuatro esquinas siguiendo las instrucciones."
    aud_008 = u"Puedes ampliar la ventana si lo necesitas."
    aud_009 = u"Hay conexión con Arduino."
    aud_010 = u"No hay conexión con Arduino."
    aud_011 = u"El orden es torre, caballo y alfil."
    aud_012 = u"Recuerda que los reyes van en la columna E."
    aud_013 = u"Empiezan las blancas."
    aud_014 = u"%s por %s"
    aud_015 = u"%s a %s"
    aud_016 = u"No muevas tanto los peones."
    aud_017 = u"Usa más los peones."
    aud_018 = u"Para conseguir una mejor movilidad de los caballos, evita llevarlos a los lados."
    aud_019 = u"Error en la detección. Pulse cualquier tecla cuando haya  vuelto a colocar las piezas."
    aud_020 = u"Si prefieres introducir el movimiento manualmente, pulsa escape."
    aud_021 = u"Error de detección, introduzca el movimiento manulamente."
    aud_022 = u"Jaque mate, ganan %s en el turno %s, ¡felicidades!."
    aud_023 = u"%s corona."
    aud_024 = u"Enroque corto."
    aud_025 = u"Enroque largo."
    aud_026 = u"Repite el movimiento."
    aud_027 = u"Cuando hayas devuelto las piezas a su posición inicial, pulsa cualquier tecla para continuar."


class Italian(Language):
    @staticmethod
    def main():
        global language, sts, instructions
        language = 'italian'
        sts = Sts(language)
        instructions = It

    aud_001 = "Ciao, sono Pyct."
    aud_002 = "Chiedo scusa per la mia voce."
    aud_003 = "Cominciamo a calibrare la camera."
    aud_004 = "Posiziona la scacchiera in tal modo che possa vedere i quattro angoli interni."
    aud_005 = "Ti consiglio di muovere le torri in avanti."
    aud_006 = "Una volta finito, premi enter."
    aud_007 = "Ora, fai click nei quattro angoli interni seguendo le instruzioni."
    aud_008 = "Se preferisci puoi ingrandire la finestra."
    aud_009 = u"C'è connessione con Arduino."
    aud_010 = u"Non c'è connessione con Arduino."
    aud_011 = u"L'ordine è torre, cavallo e alfiere."
    aud_012 = "Ricorda, il re si trova nella colonna E."
    aud_013 = "Cominciano i bianchi."
    aud_014 = "%s per %s"
    aud_015 = "%s a %s"
    aud_016 = "Non usare sempre i pedoni, cerca di muovere altre figure."
    aud_017 = u"Cerca di muovere di più i pedoni."
    aud_018 = u"Per avere più mobilità con i cavalli, cerca di non posizionarli ai lati."
    aud_019 = "Errore rilevato. Premi qualsiasi tasto dopo aver riposto tutte le figure."
    aud_020 = "Se preferisci introdurre il movimento manualmente, premi esc."
    aud_021 = "Errore rilevato. Inserisci manualmente il movimento."
    aud_022 = "Scacco matto, %s vince nel turno %s. Congratulazioni!."
    aud_023 = "%s promossi."
    aud_024 = "Arrocco corto."
    aud_025 = "Arrocco lungo."
    aud_026 = "Ripeti il movimento."
    aud_027 = "Dopo aver riposto tutte le figure, premi qualsiasi tasto."


class Advice(Language):
    pawn_1, pawn_2, knight = give_values(None, 3)

    def main(self):
        global language
        self.pawn_1 = eval('%s.aud_016' % language.capitalize())
        self.pawn_2 = eval('%s.aud_017' % language.capitalize())
        self.knight = eval('%s.aud_018' % language.capitalize())

selected_idiom = Spanish()
