# -*- coding: utf-8 -*-

from Synthesizer import Sts
from Instructions import Spanish as Sp, English as En, Italian as It
from Functions import prevent_auido_error, give_values

language = 'spanish'
sts = Sts(language)
instructions = Sp


class Language:
    text_001, text_002, text_003, text_004, text_005, text_006, text_007, \
        text_008, text_009, text_010, text_011, text_012, text_013, text_014, \
        text_015, text_016, text_017, text_018, text_019, text_020, text_021, \
        text_022, text_023, text_024, text_025, text_026, text_027 = give_values(None, 27)

    def __init__(self):
        global language
        self.say = sts.say

    def intro(self):
        self.say(self.text_001)
        # self.say(self.text_002)

    def calibration(self, moment):
        if moment == 1:
            self.say(self.text_003)
            self.say(self.text_004)
            self.say(self.text_005)
            self.say(self.text_006)
        elif moment == 2:
            self.say(self.text_007)
            self.say(self.text_008)

    def arduino(self, signal):
        if signal:
            self.say(self.text_009)
        else:
            self.say(self.text_010)

    def match(self):
        prevent_auido_error(self.text_011)
        prevent_auido_error(self.text_012)
        prevent_auido_error(self.text_013)

    def play(self, piece, position, eaten):
        if eaten:
            self.say(self.text_014 % (piece, position))
        else:
            self.say(self.text_015 % (piece, position))

    def error_1(self):
        self.say(self.text_019)
        self.say(self.text_020)

    def error_2(self):
        self.say(self.text_021)

    def check_mate(self, player, turn):
        prevent_auido_error(self.text_022 % (player, turn - 1))

    def promotion(self, piece):
        self.say(self.text_023 % piece)

    def castling(self, side):
        if side.lower() == 'kingside':
            self.say(self.text_024)

        elif side.lower() == 'queenside':
            self.say(self.text_025)

    def repeat_move(self, first_time):
        self.say(self.text_026)

        if first_time:
            self.say(self.text_027)


class English(Language):
    @staticmethod
    def main():
        global language, sts, instructions
        language = 'english'
        sts = Sts(language)
        instructions = En

    text_001 = "Hello, I'm Pyct."
    text_002 = "I apologise for my voice."
    text_003 = "Let's start calibrating the camera."
    text_004 = "Set the chessboard in a way I can see the four inside corners."
    text_005 = "I recommend you to move forward the furthest rooks."
    text_006 = "When you have done it, press enter."
    text_007 = "Now, click on the four corners following the instructions."
    text_008 = "You can enlarge the window if you need to."
    text_009 = "There is connection with Arduino."
    text_010 = "There is no connection with Arduino."
    text_011 = "The order is rook, knight and bishop."
    text_012 = "Remember kings must be in the E column."
    text_013 = "Whites start."
    text_014 = "%s by %s"
    text_015 = "%s to %s"
    text_016 = "Don't move too many times the pawns, try to move other pieces."
    text_017 = "Try to use more the pawns."
    text_018 = "To achieve a better mobility of the knights, try to place them in the center of the chessboard."
    text_019 = "Detection error. Press any key when you have placed again the pieces."
    text_020 = "If you prefer to input manually the move, press escape."
    text_021 = "Detection error. Input the move manually."
    text_022 = "Checkmate, %s has won at turn %s, congratulations!."
    text_023 = "%s promotes."
    text_024 = "Kingside castling."
    text_025 = "Queenside castling."
    text_026 = "Repeat the move."
    text_027 = "When you have placed again the pieces, press any key."


class Spanish(Language):
    @staticmethod
    def main():
        global language, sts, instructions
        language = 'spanish'
        sts = Sts(language)
        instructions = Sp

    text_001 = u"Hola, soy Pict."
    text_002 = u"Lo siento por mi voz."
    text_003 = u"Empecemos calibrando la cámara."
    text_004 = u"Coloca el tablero de modo que pueda ver las cuatro esquinas interiores."
    text_005 = u"Te recomiendo mover hacia delante las torres más alejadas."
    text_006 = u"Cuando lo hayas hecho, pulsa énter."
    text_007 = u"Ahora, haz click en las cuatro esquinas siguiendo las instrucciones."
    text_008 = u"Puedes ampliar la ventana si lo necesitas."
    text_009 = u"Hay conexión con Arduino."
    text_010 = u"No hay conexión con Arduino."
    text_011 = u"El orden es torre, caballo y alfil."
    text_012 = u"Recuerda que los reyes van en la columna E."
    text_013 = u"Empiezan las blancas."
    text_014 = u"%s por %s"
    text_015 = u"%s a %s"
    text_016 = u"No muevas tanto los peones."
    text_017 = u"Usa más los peones."
    text_018 = u"Para conseguir una mejor movilidad de los caballos, evita llevarlos a los lados."
    text_019 = u"Error en la detección. Pulse cualquier tecla cuando haya  vuelto a colocar las piezas."
    text_020 = u"Si prefieres introducir el movimiento manualmente, pulsa escape."
    text_021 = u"Error de detección, introduzca el movimiento manulamente."
    text_022 = u"Jaque mate, ganan %s en el turno %s, ¡felicidades!."
    text_023 = u"%s corona."
    text_024 = u"Enroque corto."
    text_025 = u"Enroque largo."
    text_026 = u"Repite el movimiento."
    text_027 = u"Cuando hayas devuelto las piezas a su posición inicial, pulsa cualquier tecla para continuar."


class Italian(Language):
    @staticmethod
    def main():
        global language, sts, instructions
        language = 'italian'
        sts = Sts(language)
        instructions = It

    text_001 = "Ciao, sono Pyct."
    text_002 = "Chiedo scusa per la mia voce."
    text_003 = "Cominciamo a calibrare la camera."
    text_004 = "Posiziona la scacchiera in tal modo che possa vedere i quattro angoli interni."
    text_005 = "Ti consiglio di muovere le torri in avanti."
    text_006 = "Una volta finito, premi enter."
    text_007 = "Ora, fai click nei quattro angoli interni seguendo le instruzioni."
    text_008 = "Se preferisci puoi ingrandire la finestra."
    text_009 = u"C'è connessione con Arduino."
    text_010 = u"Non c'è connessione con Arduino."
    text_011 = u"L'ordine è torre, cavallo e alfiere."
    text_012 = "Ricorda, il re si trova nella colonna E."
    text_013 = "Cominciano i bianchi."
    text_014 = "%s per %s"
    text_015 = "%s a %s"
    text_016 = "Non usare sempre i pedoni, cerca di muovere altre figure."
    text_017 = u"Cerca di muovere di più i pedoni."
    text_018 = u"Per avere più mobilità con i cavalli, cerca di non posizionarli ai lati."
    text_019 = "Errore rilevato. Premi qualsiasi tasto dopo aver riposto tutte le figure."  # no seguro
    text_020 = "Se preferisci introdurre il movimento manualmente, premi esc."
    text_021 = "Errore rilevato. Inserisci manualmente il movimento."
    text_022 = "Scacco matto, %s vince nel turno %s. Congratulazioni!."
    text_023 = "%s promossi."
    text_024 = "Arrocco corto."
    text_025 = "Arrocco lungo."
    text_026 = "Ripeti il movimento."
    text_027 = "Dopo aver riposto tutte le figure, premi qualsiasi tasto."


class Advice(Language):
    pawn_1, pawn_2, knight = give_values(None, 3)

    def main(self):
        global language
        self.pawn_1 = eval('%s.text_016' % language.capitalize())
        self.pawn_2 = eval('%s.text_017' % language.capitalize())
        self.knight = eval('%s.text_018' % language.capitalize())

selected_idiom = Spanish()
