# -*- coding: cp1252 -*-

import gtk
import re

import cv2

import Pieces
from Functions import *
import Audio

pos0, pos1, who_promote = give_values(None, 3)


class Window:
    global pos0, pos1, who_promote

    @staticmethod
    def destroy(widget, data=None):
        gtk.main_quit()

    @staticmethod
    def translate(string, to):
        if to == 'spanish':
            string = re.sub("King", u"Rey", string)
            string = re.sub("Queen", u"Reina", string)
            string = re.sub("Bishop", u"Alfil", string)
            string = re.sub("Knight", u"Caballo", string)
            string = re.sub("Rock", u"Torre", string)
            string = re.sub("Pawn", u"Peon", string)

        elif to == 'english':
            string = re.sub(u"Rey", "King", string)
            string = re.sub(u"Reina", "Queen", string)
            string = re.sub(u"Alfil", "Bishop", string)
            string = re.sub(u"Caballo", "Knight", string)
            string = re.sub(u"Torre", "Rock", string)
            string = re.sub(r"Peon", "Pawn", string)

        return string

    @staticmethod
    def make_button(text, func, box):
        new_button = gtk.Button(text)
        new_button.connect('clicked', func)
        box.pack_start(new_button)
        return new_button

    def playing(self, player, lists):
        string = "%s\n\n" % player
        for i in lists[0] + lists[1]:
            string = string + "%s\n" % i

        return self.translate(string, 'spanish')

    def change_idiom(self, idiom):
        if idiom == 'spanish':
            Audio.selected_idiom = Audio.Spanish()

        elif idiom == 'english':
            Audio.selected_idiom = Audio.English()

        elif idiom == 'italian':
            Audio.selected_idiom = Audio.Italian()

        Audio.selected_idiom.main()

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
        self.box8 = gtk.HBox()

        self.main_box.pack_start(self.box1)
        self.main_box.pack_start(self.box2)
        self.main_box.pack_start(self.box3)
        self.box2.pack_start(self.box4)
        self.box2.pack_start(self.box5)
        self.box3.pack_start(self.box6)
        self.box3.pack_start(self.box7)
        self.box5.pack_start(self.box8)

        self.main_box.set_homogeneous(10)
        self.box3.set_homogeneous(10)
        self.box2.set_homogeneous(10)

        self.playing_w = gtk.Label(self.playing("Blancas", [Lists.WhiteHighPieces, Lists.WhiteLowPieces]))
        self.playing_b = gtk.Label(self.playing("Negras", [Lists.BlackHighPieces, Lists.BlackLowPieces]))
        self.label = gtk.Label()

        self.image = gtk.Image()

        self.box4.pack_start(self.playing_w)
        self.box4.pack_start(self.playing_b)

        self.turn = gtk.Label("")
        self.player = gtk.Label("")
        self.move = gtk.Label("")

        self.box7.pack_start(self.turn)
        self.box7.pack_start(self.player)
        self.box7.pack_start(self.move)

        self.box7.set_homogeneous(10)

        self.start = self.make_button('Empezar', lambda (widget): gtk.main_quit(), self.box5)

        self.spanish = self.make_button(u'Español', lambda (widget): self.change_idiom('spanish'), self.box8)
        self.english = self.make_button('English', lambda (widget): self.change_idiom('english'), self.box8)
        self.italian = self.make_button('Italiano', lambda (widget): self.change_idiom('italian'), self.box8)

        self.record = self.make_button('Grabar partida\n(no disponible)', lambda (widget): None, self.box5)

        self.exit = self.make_button('Salir', lambda (widget): exit(11), self.box5)

        self.window.add(self.main_box)

        self.window.show_all()
        self.window.connect('delete-event', self.destroy)

    @staticmethod
    def main():
        gtk.main()

    def refresh_playing(self, K, player):
        text_w = self.playing_w.get_text()
        text_b = self.playing_b.get_text()

        text_w = self.translate(text_w, 'english')
        text_b = self.translate(text_b, 'english')

        for i in text_w[7:].split("\n"):
            if i != "":
                if i not in (Lists.WhiteHighPieces + Lists.WhiteLowPieces):
                    if type(K) == str and player == 1:
                        text_w = re.sub(i, change_piece(K), text_w)
                        K = None
                    else:
                        text_w = re.sub(i, "", text_w)

                elif len(re.findall(i, text_w)) > len(re.findall(i, str(Lists.WhiteHighPieces + Lists.WhiteLowPieces))):
                    text_w = re.sub(i, "", text_w, 1)

                else:
                    continue

        for j in text_b[6:].split("\n"):
            if j != "":
                if j not in (Lists.BlackLowPieces + Lists.BlackHighPieces):
                    if type(K) == str and player == 2:
                        text_b = re.sub(j, change_piece(K), text_b)
                        K = None
                    else:
                        text_b = re.sub(j, "", text_b)

                elif len(re.findall(i, text_b)) > len(re.findall(i, str(Lists.BlackHighPieces + Lists.BlackLowPieces))):
                    text_b = re.sub(i, "", text_b, 1)

                else:
                    continue

        # text_w = re.sub(r"Peon", u"Peón", self.translate(text_w, 'spanish'))
        # text_b = re.sub(r"Peon", u"Peón", self.translate(text_b, 'spanish'))

        self.playing_w.set_text(self.translate(text_w, 'spanish'))
        self.playing_b.set_text(self.translate(text_b, 'spanish'))

    def video(self, img):
        pix = gtk.gdk.pixbuf_new_from_file(img)
        pix = pix.scale_simple(430, 370, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pix)

        self.box6.pack_start(self.image)

        self.window.show_all()

    def calibration_instructions(self):
        self.label.set_text(Audio.instructions.calibration_1())
        self.label.set_justify(0)
        self.box1.pack_start(self.label)
        self.label.set_alignment(0.5, 0.04)
        self.window.show_all()

    def print_move(self, turn, player, mov):
        self.turn.set_alignment(0.1, 0.004)
        self.player.set_alignment(0.1, 0.004)
        self.move.set_alignment(0.1, 0.004)

        text_1 = self.turn.get_text()
        text_2 = self.player.get_text()
        text_3 = self.move.get_text()

        a = text_1.split("\n")

        if len(a) >= 21:
            text_1 = ""
            text_2 = ""
            text_3 = ""

        text_1 = text_1 + "%s\n" % turn
        text_2 = text_2 + "%s\n" % player
        text_3 = text_3 + "%s\n" % mov

        self.turn.set_text(text_1)
        self.player.set_text(text_2)
        self.move.set_text(text_3)

        self.window.show_all()

    def print_incorrect_move(self):
        self.label.set_text(self.label.get_text() + Pieces.answer)
        self.label.set_justify(0)
        self.label.set_alignment(0.01, 0.04)
        self.window.show_all()

    @staticmethod
    def promote():
        global who_promote

        def end(widget):
            global who_promote
            who_promote = text.get_text()
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

        return inv_change_piece(who_promote)

    @staticmethod
    def movement(widget):
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
        return inv_change_position(pos0), inv_change_position(pos1)


def OpenCV(winName, x, y, width, height):
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        cv2.moveWindow(winName, x, y)
        cv2.resizeWindow(winName, width, height)
