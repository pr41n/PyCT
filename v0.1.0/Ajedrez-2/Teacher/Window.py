# -*- coding: cp1252 -*-

import gtk
import re

import cv2

import Pieces
from Functions import *
from Instructions import Calibration

sts = Pieces.sts


class Ventana:
    global pos0, pos1, pieza_corona

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def translate(self, lista, to):
        if to == 'spanish':
            lista = re.sub("King", u"Rey", lista)
            lista = re.sub("Queen", u"Reina", lista)
            lista = re.sub("Bishop", u"Alfil", lista)
            lista = re.sub("Knight", u"Caballo", lista)
            lista = re.sub("Rock", u"Torre", lista)
            lista = re.sub("Pawn", r"Peon", lista)

        elif to == 'english':
            lista = re.sub(u"Rey", "King", lista)
            lista = re.sub(u"Reina", "Queen", lista)
            lista = re.sub(u"Alfil", "Bishop", lista)
            lista = re.sub(u"Caballo", "Knight", lista)
            lista = re.sub(u"Torre", "Rock", lista)
            lista = re.sub(r"Peon", "Pawn", lista)

        return lista

    def make_button(self, text, func, box):
        new_button = gtk.Button(text)
        new_button.connect('clicked', func)
        eval('self.%s.pack_start(new_button)' % box)
        return new_button

    def jugando_B(self, widget):
        lista = "Blancas\n\n"
        for i in Lists.PiezasMayores_B + Lists.PiezasMenores_B:
            lista = lista + "%s\n" % i

        return self.translate(lista, 'spanish') # re.sub("Peon", u"Peón", self.translate(lista, 'spanish'))

    def jugando_N(self, widget):
        lista = "Negras\n\n"
        for i in Lists.PiezasMayores_N + Lists.PiezasMenores_N:
            lista = lista + "%s\n" % i

        return self.translate(lista, 'spanish') # re.sub("Peon", u"Peón", self.translate(lista, 'spanish'))

    def __init__(self):
        self.window = gtk.Window()
        self.window.maximize()
        self.window.set_title("PyCT")

        self.main_box = gtk.HBox()

        self.box1 = gtk.VBox()
        self.box2 = gtk.VBox()
        self.box3 = gtk.VBox()
        self.box4 = gtk.HBox()
        self.box5 = gtk.VBox()
        self.box6 = gtk.HBox()
        self.box7 = gtk.HBox()

        self.main_box.pack_start(self.box1)
        self.main_box.pack_start(self.box2)
        self.main_box.pack_start(self.box3)
        self.box2.pack_start(self.box4)
        self.box2.pack_start(self.box5)
        self.box3.pack_start(self.box6)
        self.box3.pack_start(self.box7)

        self.main_box.set_homogeneous(10)
        self.box3.set_homogeneous(10)
        self.box2.set_homogeneous(10)

        self.jugando_b = gtk.Label(self.jugando_B(None))
        self.jugando_n = gtk.Label(self.jugando_N(None))
        self.label = gtk.Label()

        self.image = gtk.Image()

        self.box4.pack_start(self.jugando_b)
        self.box4.pack_start(self.jugando_n)

        self.turn = gtk.Label("")
        self.player = gtk.Label("")
        self.move = gtk.Label("")

        self.box7.pack_start(self.turn)
        self.box7.pack_start(self.player)
        self.box7.pack_start(self.move)

        self.box7.set_homogeneous(10)

        self.button1 = self.make_button('Empezar', self.destroy, 'box5')

        self.button4 = self.make_button('Movmiento Manual', self.movimiento, 'box5')
        self.button3 = self.make_button('Comer', lambda (widget): exit(11), 'box5')

        self.button2 = self.make_button('Salir', lambda (widget): exit(11), 'box5')

        self.window.add(self.main_box)

        self.window.show_all()
        self.window.connect('delete-event', self.destroy)

    def main(self):
        gtk.main()

    def refresh_playing(self, K, jugador):
        text_b = self.jugando_b.get_text()
        text_n = self.jugando_n.get_text()

        text_b = self.translate(text_b, 'english')
        text_n = self.translate(text_n, 'english')

        for i in text_b[7:].split("\n"):
            if i != "":
                if i not in (Lists.PiezasMayores_B + Lists.PiezasMenores_B):
                    if type(K) == str and jugador == 1:
                        text_b = re.sub(i, cambio_ficha(K), text_b)
                        K = None
                    else:
                        text_b = re.sub(i, "", text_b)

                elif len(re.findall(i, text_b)) > len(re.findall(i, str(Lists.PiezasMayores_B + Lists.PiezasMenores_B))):
                    text_b = re.sub(i, "", text_b, 1)

                else:
                    continue

        for j in text_n[6:].split("\n"):
            if j != "":
                if j not in (Lists.PiezasMenores_N + Lists.PiezasMayores_N):
                    if type(K) == str and jugador == 2:
                        text_n = re.sub(j, cambio_ficha(K), text_n)
                        K = None
                    else:
                        text_n = re.sub(j, "", text_n)

                elif len(re.findall(i, text_n)) > len(re.findall(i, str(Lists.PiezasMayores_N + Lists.PiezasMenores_N))):
                    text_n = re.sub(i, "", text_n, 1)

                else:
                    continue

        # text_b = re.sub(r"Peon", u"Peón", self.translate(text_b, 'spanish'))
        # text_n = re.sub(r"Peon", u"Peón", self.translate(text_n, 'spanish'))

        self.jugando_b.set_text(self.translate(text_b, 'spanish'))
        self.jugando_n.set_text(self.translate(text_n, 'spanish'))

    def video(self, img):
        pix = gtk.gdk.pixbuf_new_from_file(img)
        pix = pix.scale_simple(430, 370, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pix)

        self.box6.pack_start(self.image)

        self.window.show_all()

    def calibration_instructions(self):
        self.label.set_text(Calibration.calibration())
        self.label.set_justify(0)
        self.box1.pack_start(self.label)
        self.label.set_alignment(0.5, 0.04)
        self.window.show_all()

    def print_move(self, turno, jugador, mov):
        self.turn.set_alignment(0.1, 0.004)
        self.player.set_alignment(0.1, 0.004)
        self.move.set_alignment(0.1, 0.004)

        texto_1 = self.turn.get_text()
        texto_2 = self.player.get_text()
        texto_3 = self.move.get_text()

        a = texto_1.split("\n")

        if len(a) >= 21:
            texto_1 = ""
            texto_2 = ""
            texto_3 = ""

        texto_1 = texto_1 + "%s\n" % turno
        texto_2 = texto_2 + "%s\n" % jugador
        texto_3 = texto_3 + "%s\n" % mov

        self.turn.set_text(texto_1)
        self.player.set_text(texto_2)
        self.move.set_text(texto_3)

        self.window.show_all()

    def print_incorrect_move(self):
        self.label.set_text(self.label.get_text() + Pieces.answer)
        self.label.set_justify(0)
        self.label.set_alignment(0.01, 0.04)
        self.window.show_all()

    @staticmethod
    def corona():
        global pieza_corona

        def end(widget):
            global pieza_corona
            pieza_corona = text.get_text()
            win.hide()
            gtk.main_quit()

        win = gtk.Window()
        win.set_size_request(500, 40)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_title('Pieza en la que corona')

        box = gtk.HBox()
        label = gtk.Label('Pieza: ')
        text = gtk.Entry()

        button = gtk.Button('OK')
        button.connect('clicked', end)
        box.pack_start(label)
        box.pack_start(text)
        box.pack_start(button)

        win.add(box)
        win.show_all()
        gtk.main()

        return inv_cambio_ficha(pieza_corona)

    @staticmethod
    def movimiento(widget):
        def end(w):
            global pos0, pos1
            pos0 = text1.get_text()
            pos1 = text2.get_text()
            win.hide()
            gtk.main_quit()

        win = gtk.Window()
        win.set_size_request(500, 40)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_title('Escriba las casillas respectivas')

        box = gtk.HBox()
        label1 = gtk.Label('Antes: ')
        label2 = gtk.Label('Ahora: ')
        text1 = gtk.Entry()
        text2 = gtk.Entry()

        button = gtk.Button('OK')
        button.connect('clicked', end)
        box.pack_start(label1)
        box.pack_start(text1)
        box.pack_start(label2)
        box.pack_start(text2)
        box.pack_start(button)

        win.add(box)
        win.show_all()
        gtk.main()

        global pos0, pos1
        return inv_cambio_posicion(pos0), inv_cambio_posicion(pos1)


def OpenCV(winName, x, y, width, height):
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        cv2.moveWindow(winName, x, y)
        cv2.resizeWindow(winName, width, height)

if __name__ == '__main__':
    ventana = Ventana()
    ventana.main()
    Lists.PiezasMenores_B.remove("Pawn_1")
    ventana.refresh_playing("Torre")
    ventana.main()
