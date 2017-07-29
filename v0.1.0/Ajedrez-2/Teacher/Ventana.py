# -*- coding: cp1252 -*-

import gtk
import cv2
import random
import re
import threading

import Listas, Instrucciones
from Functions import *


class Ventana:
    global antes, ahora, pieza_corona

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def make_button(self, text, func, box):
        new_button = gtk.Button(text)
        new_button.connect('clicked', func)
        eval('self.%s.pack_start(new_button)' % box)
        return new_button

    def jugando_B(self, widget):
        lista = "Blancas\n\n"
        for i in Listas.PiezasMayores_B + Listas.PiezasMenores_B:
            lista = lista + "%s\n" % i
        return lista

    def jugando_N(self, widget):
        lista = "Negras\n\n"
        for i in Listas.PiezasMayores_N + Listas.PiezasMenores_N:
            lista = lista + "%s\n" % i
        return lista

    def comer_1(self, widget):
        a = Listas.PiezasMenores_N[random.randint(0, len(Listas.PiezasMenores_N) - 1)]
        Listas.PiezasMenores_N.remove(a)
        text = self.jugando_n.get_text()
        text = re.sub(a, "", text)
        self.jugando_n.set_text(text)

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

        self.image = gtk.Image()

        self.box4.pack_start(self.jugando_b)
        self.box4.pack_start(self.jugando_n)

        self.moves = gtk.Label("")
        self.box7.pack_start(self.moves)

        self.button1 = self.make_button('Empezar', self.destroy, 'box5')

        self.button4 = self.make_button('Movmiento Manual', self.movimiento, 'box5')
        self.button3 = self.make_button('Comer', self.comer_1, 'box5')

        self.button2 = self.make_button('Salir', lambda (widget): exit(11), 'box5')

        self.window.add(self.main_box)

        self.window.show_all()
        self.window.connect('delete-event', self.destroy)

    def main(self):
        gtk.main()

    def refresh_playing(self):
        text_b = self.jugando_b.get_text()
        text_n = self.jugando_n.get_text()

        for i in text_b[7:].split("\n"):
            if i not in (Listas.PiezasMayores_B + Listas.PiezasMenores_B) and i != "":
                text_b = re.sub(i, "", text_b)
                self.jugando_b.set_text(text_b)

        for j in text_n[6:].split("\n"):
            if j not in (Listas.PiezasMenores_N + Listas.PiezasMayores_N) and j != "":
                text_n = re.sub(j, "", text_n)
                self.jugando_n.set_text(text_n)

    def video(self, img):
        pix = gtk.gdk.pixbuf_new_from_file(img)
        pix = pix.scale_simple(430, 370, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pix)

        self.box6.pack_start(self.image)

        self.window.show_all()

    def calibration_instructions(self):
        label = gtk.Label(Instrucciones.calibration())
        label.set_justify(0)
        self.box1.pack_start(label)
        label.set_alignment(0.5, 0.04)
        self.window.show_all()

    def print_move(self, move):
        self.moves.set_alignment(0.1, 0.004)
        texto = self.moves.get_text()
        a = texto.split("\n")
        if len(a) >= 21:
            texto = ""
        texto = texto + "%s\n" % move
        self.moves.set_text(texto)
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
            global antes, ahora
            antes = text1.get_text()
            ahora = text2.get_text()
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

        global antes, ahora
        return inv_cambio_posicion(antes), inv_cambio_posicion(ahora)


class OpenCV:
    def __init__(self):
        pass

    @staticmethod
    def ventana(winName, x, y, width, height):
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        cv2.moveWindow(winName, x, y)
        cv2.resizeWindow(winName, width, height)

if __name__ == '__main__':
    ventana = Ventana()
    ventana.main()
