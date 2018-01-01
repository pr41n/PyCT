#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import gtk
except ImportError:
    import pygtk
    pygtk.require(2.0)
    import gtk
finally:
    import re
    import audio
    from chess_2 import lists

"""
Change lists of pieces to sets
make a refresh decorator/template
"""


def translate(string, to=None):
    if to == 'english':
        string = re.sub(audio.language.player_1, "White", string)
        string = re.sub(audio.language.player_2, "Black", string)
        string = re.sub(audio.language.pawn, "Pawn", string)
        string = re.sub(audio.language.rook, "Rook", string)
        string = re.sub(audio.language.knight, "Knight", string)
        string = re.sub(audio.language.bishop, "Bishop", string)
        string = re.sub(audio.language.queen, "Queen", string)
        string = re.sub(audio.language.king, "King", string)

    else:
        string = re.sub("White", audio.language.player_1, string)
        string = re.sub("Black", audio.language.player_2, string)
        string = re.sub("Pawn", audio.language.pawn, string)
        string = re.sub("Rook", audio.language.rook, string)
        string = re.sub("Knight", audio.language.knight, string)
        string = re.sub("Bishop", audio.language.bishop, string)
        string = re.sub("Queen", audio.language.queen, string)
        string = re.sub("King", audio.language.king, string)

    return string


class Main:
    def __refresh(self, f):
        pass

    def __init__(self, num_players):
        self.num_players = num_players

        # Labels
        self.correction = gtk.Label()
        self.turns = gtk.Label()
        self.players = gtk.Label()
        self.movements = gtk.Label()

        # Window
        self.window = gtk.Window()
        self.window.maximize()
        self.window.set_title("PyCT")

        # Tables
        self.main_table = gtk.Table(2, 3, gtk.TRUE)
        self.buttons_table = gtk.Table(4, 2, gtk.TRUE)
        self.players_table = gtk.Table(22-self.num_players, self.num_players, gtk.TRUE)
        self.info_table_left = gtk.Table(4, 1, gtk.TRUE)
        self.info_table_right = gtk.Table(1, 1, gtk.TRUE)
        self.display_info = gtk.Table(1, 3, gtk.TRUE)

        self.main_table.attach(self.buttons_table, 1, 2, 1, 2)
        self.main_table.attach(self.players_table, 1, 2, 0, 1)
        self.main_table.attach(self.info_table_left, 0, 1, 0, 2)
        self.main_table.attach(self.info_table_right, 2, 3, 1, 2)
        self.display_info.attach(self.turns, 0, 1, 0, 1)
        self.display_info.attach(self.players, 1, 2, 0, 1)
        self.display_info.attach(self.movements, 2, 3, 0, 1)

        # Buttons
        self.language_button = self.__make_button(audio.language.name_of_the_button,
                                                  lambda w: self.__change_language(),
                                                  (0, 2, 0, 1))
        self.start_button = self.__make_button(audio.language.start,
                                               lambda w: gtk.main_quit(),
                                               (0, 2, 1, 2))
        self.pyct_button = self.__make_button('Teacher',
                                              lambda w: self._change_pyct(),
                                              (0, 1, 2, 3))
        self.chess_button = self.__make_button('Chess 2',
                                               lambda w: None,
                                               (1, 2, 2, 3))
        self.exit_button = self.__make_button(audio.language.out,
                                              lambda w: exit(11),
                                              (0, 2, 3, 4))

        # Players
        for player in range(self.num_players):
            name = eval('audio.language.player_%d' % (player + 1))
            self.players_table.attach(gtk.Label(name), player, player+1, 2, 3)

            for pos, piece in enumerate(eval('lists.%sPieces' % translate(name, 'english'))):
                piece = translate(piece)
                self.players_table.attach(gtk.Label(piece), player, player + 1, pos+4, pos+5)

        self.players_table.attach(gtk.Label(' '), 0, self.num_players, 21, 22)

        # Video
        self.frame = gtk.Image()

        # Scrollbars
        self.scroll_1 = gtk.ScrolledWindow()
        self.scroll_2 = gtk.ScrolledWindow()

        self.scroll_1.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self.scroll_2.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)

        self.scroll_1.add_with_viewport(self.correction)
        self.scroll_2.add_with_viewport(self.display_info)

        self.info_table_left.attach(self.scroll_1, 0, 1, 0, 3)
        self.info_table_right.attach(self.scroll_2, 0, 1, 0, 1)

    def main(self):
        self.window.connect('delete-event', lambda w, e: gtk.main_quit())
        self.window.add(self.main_table)
        self.window.show_all()
        gtk.main()

    def video(self, img):
        """
        Should be changed as soon as possible
        """
        pix = gtk.gdk.pixbuf_new_from_file(img)
        pix = pix.scale_simple(430, 370, gtk.gdk.INTERP_BILINEAR)
        self.frame.set_from_pixbuf(pix)

        self.main_table.attach(self.frame, 2, 3, 0, 1)
        self.window.show_all()

    def show_logo(self):
        pix = gtk.gdk.pixbuf_new_from_file('PyCT.png')
        pix = pix.scale_simple(440, 180, gtk.gdk.INTERP_BILINEAR)

        logo = gtk.Image()
        logo.set_from_pixbuf(pix)

        self.info_table_left.attach(logo, 0, 1, 3, 4)
        self.window.show_all()

    def print_move(self, turn, player, movement):
        self.turns.set_alignment(0.1, 0.004)
        self.players.set_alignment(0.1, 0.004)
        self.movements.set_alignment(0.1, 0.004)

        turns = self.turns.get_text()
        players = self.players.get_text()
        movements = self.movements.get_text()

        # Check turn
        try:
            turn = audio.language.turn + " " + turn if turn != turns[-2] else ""
        except IndexError:      # First turn
            turn = audio.language.turn + " " + turn

        # Display info
        self.turns.set_text(turns + turn + "\n")
        self.players.set_text(players + translate(player) + "\n")
        self.movements.set_text(movements + movement + "\n")

        self.window.show_all()

    def correct_move(self, *args):
        if len(args) == 0:      # Calibration instructions
            self.correction.set_text(audio.language.calibration)
            self.correction.set_alignment(0.5, 0.04)

        else:
            self.correction.set_text(self.correction.get_text() + args[0])
            self.correction.set_alignment(0.01, 0.04)
        self.window.show_all()

    def refresh_playing(self, promoted=None):       # promoted must be in English
        children = self.players_table.get_children()
        children.remove([i for i in children if i.get_label() == ' '][0])

        lenght = len(self.players_table.get_children())
        player_range = lenght / self.num_players

        for player in range(self.num_players):
            begin = player_range * player
            finish = lenght / self.num_players * (player + 1)
            player_name = eval('audio.language.player_%d' % (player + 1))
            piezas = eval('lists.%sPieces' % translate(player_name, 'english'))

            for pos, child in enumerate(children[::-1][begin+1:finish]):
                piece = child.get_label()
                e_piece = translate(piece, 'english')
                if e_piece not in piezas:
                    if type(promoted) == str:
                        child.set_label(translate(promoted))
                        promoted = None
                    else:
                        child.set_label(' ')

    def _change_pyct(self):
        pass

    def _change_chess(self):
        pass

    def __make_button(self, text, func, coor):
        new_button = gtk.Button(text)
        new_button.connect('clicked', func)
        self.buttons_table.attach(new_button, coor[0], coor[1], coor[2], coor[3])
        return new_button

    def __change_language(self):
        l_index = audio.languages.index(audio.language)
        new_l = audio.languages[l_index - 1]

        audio.language = new_l
        audio.refresh_sts()
        self.__refresh_gui()

    def __refresh_gui(self):
        """
          Only used during the configuration, so it suposses all
        the initial pieces are in their respective lists with their
        respective position.
        """
        self.language_button.set_label(audio.language.name_of_the_button)
        self.start_button.set_label(audio.language.start)
        self.exit_button.set_label(audio.language.out)

        children = self.players_table.get_children()
        children.remove([i for i in children if i.get_label() == ' '][0])

        lenght = len(self.players_table.get_children())
        player_range = lenght / self.num_players

        for player in range(self.num_players):
            begin = player_range * player
            finish = lenght / self.num_players * (player + 1)
            player_name = eval('audio.language.player_%d' % (player + 1))
            piezas = eval('lists.%sPieces' % translate(player_name, 'english'))

            for pos, child in enumerate(children[::-1][begin:finish]):
                if pos == 0:
                    child.set_label(player_name)
                else:
                    child.set_label(translate(piezas[pos - 1]))


class __Window:
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_size_request(500, 40)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.box = gtk.HBox()
        self.label1 = gtk.Label()
        self.label2 = gtk.Label()
        self.entry1 = gtk.Entry()
        self.entry2 = gtk.Entry()

        self.window.add(self.box)
        self.window.connect('delete-event', lambda w, e: self.forced_exit())
        self.ans_1, self.ans_2 = [str]*2

    class WindowError(Exception):
        pass

    def _add_button(self, title, f):
        button = gtk.Button(title)
        button.connect('clicked', f)
        self.box.pack_start(button)
        return button

    def _start(self):
        self.window.show_all()
        gtk.main()

    def _add2box(self, *args):
        for arg in args:
            self.box.pack_start(arg)

    def forced_exit(self):
        gtk.main_quit()
        raise self.WindowError


class ChooseDetection(__Window):
    def main(self):
        del self.label1, self.entry1, self.label2, self.entry2, self.ans_2

        self.window.set_title(audio.language.sort_of_detection)

        manual = self._add_button(audio.language.sort_of_detection_1, self.end)
        s_automatic = self._add_button(audio.language.sort_of_detection_2, self.end)
        automatic = self._add_button(audio.language.sort_of_detection_3, self.end)

        manual.set_tooltip_text(audio.language.detection_description_1)
        s_automatic.set_tooltip_text(audio.language.detection_description_2)
        automatic.set_tooltip_text(audio.language.detection_description_3)

        self._start()
        return self.ans_1[0].lower()

    def end(self, widget):
        self.ans_1 = widget.get_label()
        self.window.destroy()
        gtk.main_quit()


class ManualMove(__Window):
    def main(self):
        self.window.set_title(audio.language.move_1)
        self.label1.set_text(audio.language.move_2)
        self.label2.set_text(audio.language.move_2)

        self._add2box(self.label1, self.entry1, self.label2, self.entry2)
        self._add_button('OK', self.end)

        self._start()
        return self.ans_1.upper(), self.ans_2.upper()

    def end(self, w):
        del w
        self.ans_1 = self.entry1.get_text()
        self.ans_2 = self.entry2.get_text()
        self.window.hide()
        gtk.main_quit()


class Promotion(__Window):
    def main(self):
        del self.label2, self.entry2, self.ans_2

        self.window.set_title(audio.language.promote_1)
        self.label1.set_text(audio.language.promote_2)

        self._add2box(self.label1, self.entry1)
        self._add_button('OK', self.end)

        self._start()
        final_ans = self.ans_1.capitalize()
        return final_ans, translate(final_ans, 'english')

    def end(self, w):
        del w
        self.ans_1 = self.entry1.get_text()
        self.window.hide()
        gtk.main_quit()
