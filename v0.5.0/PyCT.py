#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep

import cv2
import numpy as np

import audio
import window
from scripts import connection
from chess_2 import lists, pieces, video
from func import thread_starter, video_exit, opencv_win

"""
Delete c argument at PyCT when window.py will be finished (celdas gtk2)
Take control of advices (property)
Do auds optional and configurable at subclasses
"""


class PyCT:
    def __init__(self):
        self.first_incorrect = True
        self.rectified = False

        # Pieces
        self.pawn = pieces.Pawn(audio)
        self.rook = pieces.Rook(audio)
        self.knight = pieces.Knight(audio)
        self.bishop = pieces.Bishop(audio)
        self.queen = pieces.Queen(audio)
        self.king = pieces.King(audio)

        # GUI, the configuration takes place here
        self.win = window.Main(2)
        chooser = window.ChooseDetection()
        self.__manual_move = window.ManualMove()
        self.insert_promotion = window.Promotion()
        self.win.main()

        # Audio and language
        self.sts = audio.sts

        self.audio = audio.Language()
        self.language = audio.language.babel

        thread_starter(self.audio.intro).join()

        # Choose camera
        camera = video.Camera()
        self.cam = camera.choose()
        del camera

        # Calibration
        thread_starter(self.audio.calibration, [1])
        self.chessboard = self.calibration()

        cv2.destroyWindow(audio.language.open_cv_2)
        self.win.correction.set_text('')

        # Check arduino
        self.arduino, self.good, self.bad, self.checkmate = self.arduino_connection()

        # Detection
        self.detection = video.Detection(self.chessboard)
        thread_starter(self.audio.detection)
        self.sort_of_detection = chooser.main()
        del chooser

        self.player = 'White'
        self.turn = 1
        self.match = True
        self.win.show_logo()

        while self.match:
            self.occupied_squares = lists.occupied_squares()

            try:
                self.pos0, self.pos1 = self.detect_move()
                if self.pos0 not in self.occupied_squares.keys():
                    raise self.detection.DetectionError

            except EnvironmentError:
                continue

            except self.detection.DetectionError as err:
                print "Detection Error: {}".format(err)
                thread_starter(self.audio.error_1)

                if cv2.waitKey(0) & 0xFF == 27:
                    self.pos0, self.pos1 = self.manual_move()
                else:
                    continue

            piece = eval('self.{}'.format(self.occupied_squares[self.pos0].lower()))
            self.lets_advice, self.advice = piece.piece_advices(self.pos0, self.pos1, self.player, self.turn)
            self.check_move(piece)

        eval(self.checkmate)
        winner = audio.language.player_2 if self.player == 'White' else audio.language.player_1
        thread_starter(self.audio.check_mate, [winner, self.turn - 1]).join()
        try:
            self.arduino.write('r', 0)
        except AttributeError:
            pass
        finally:
            video_exit(227)

    def calibration(self):
        opencv_win(audio.language.open_cv_1, 1100, -100, 440, 350)

        while True:
            frame = self.cam.read()[1]
            k = cv2.waitKey(1) & 0xFF
            video_exit(k)

            # Showing video
            cv2.imshow(audio.language.open_cv_1, frame)

            # Calibration
            if k == 10:
                cv2.destroyWindow(audio.language.open_cv_1)
                thread_starter(self.audio.calibration, [2])
                self.win.correct_move()
                return video.Calibration(frame)

    def arduino_connection(self):
        arduino, good, bad, checkmate, con_stat = [None]*5
        try:
            con_stat = True
            delay = 0

            arduino = connection.Arduino(2)
            good = "self.arduino.write('a', %s)" % delay
            bad = "self.arduino.write('b', %s)" % delay
            checkmate = "self.arduino.write('c', %s)" % delay

        except OSError:
            con_stat = False
            arduino, good, bad, checkmate = ['None']*4

        finally:
            thread_starter(self.audio.arduino, [con_stat]).join()
            return arduino, good, bad, checkmate

    def detect_move(self):
        initial_pos, final_pos = [None]*2
        moving, show_hist = [False]*2
        frame_num = 0

        img = cv2.imread('languages/Video.png')
        win_title = audio.language.open_cv_3
        opencv_win(win_title, 490, 485, 435, 170)

        while True:
            frame = self.cam.read()[1]
            k = cv2.waitKey(1) & 0xFF
            video_exit(k)

            if k == 27:
                return self.manual_move()

            if k == ord('d'):       # Force DetectionError
                return None, None

            # Frame to show
            if k == ord('r'):
                self.rectified = False if self.rectified else True

            frame2show = self.chessboard.rectify_image(frame, rotate=True) if self.rectified else frame

            # Prevent video error for semi-automatic and automatic
            if frame_num < 10 and self.sort_of_detection in ['s', 'a']:
                frame_num += 1
                initial_pos = frame

            # Detect movement
            if self.sort_of_detection in ['m', 's']:        # Manual or semi-automatic, respectively
                if k == 32:
                    if type(initial_pos) == np.ndarray:
                        final_pos = frame
                    elif self.sort_of_detection == 'm':
                        initial_pos = frame

            elif self.sort_of_detection == 'a':         # Automatic
                rectified_init = self.chessboard.rectify_image(initial_pos)
                rectified_frame = self.chessboard.rectify_image(frame)

                img_1 = cv2.cvtColor(rectified_init, cv2.COLOR_BGR2GRAY)
                img_2 = cv2.cvtColor(rectified_frame, cv2.COLOR_BGR2GRAY)

                hist1 = cv2.calcHist([img_1], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([img_2], [0], None, [256], [0, 256])

                n = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                if n < 0.97:
                    moving = True
                elif n > 0.98 and moving:
                    sleep(1)
                    final_pos = self.cam.read()[1]

                if k == ord('s'):
                    show_hist = True

                if show_hist:
                    hist_frame = rectified_frame.copy()
                    cv2.putText(hist_frame, str(n), (300, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255),
                                fontScale=1, thickness=2)

                    cv2.imshow('histogram value', hist_frame)

            # Detect the movement
            if type(initial_pos) == np.ndarray and type(final_pos) == np.ndarray:
                return self.detection.board(initial_pos, final_pos, self.player)

            cv2.imshow(win_title, img)
            cv2.imwrite('tmp/frame.jpg', frame2show)
            self.win.video('tmp/frame.jpg')

    def manual_move(self):
        pos0, pos1 = self.__manual_move.main()
        pos0 = self.king.inv_change_position(pos0)
        pos1 = self.king.inv_change_position(pos1)
        return pos0, pos1

    def check_move(self, one_piece):
        one_piece.player = self.player

        if one_piece.correct_move(self.pos0[0], self.pos0[1], self.pos1[0], self.pos1[1]):
            promotion = None

            if one_piece.name == "King" and self.pos0[0] == 5 and abs(self.pos1[0]-self.pos0[0]) == 2:
                if self.pos1[0] == 5:
                    aud = thread_starter(self.audio.castling, ['QueenSide'])
                    movement = audio.language.aud_024
                else:
                    aud = thread_starter(self.audio.castling, ['KingSide'])
                    movement = audio.language.aud_025

            elif one_piece.name == "Pawn" and self.pos1[1] == 8 or self.pos1[1] == 1:
                promotion = self.insert_promotion.main()
                aud = thread_starter(self.audio.promotion, [promotion[0]])
                movement = audio.language.aud_023 % promotion[0]

            else:
                name = window.translate(one_piece.name)
                alph_pos = one_piece.change_position(self.pos1)

                if self.pos1 in self.occupied_squares:
                    eaten = True
                    text = audio.language.aud_014
                else:
                    eaten = False
                    text = audio.language.aud_015

                aud = thread_starter(self.audio.play, [name, alph_pos, eaten])
                movement = text % (name, alph_pos)

            self.win.print_move(str(self.turn), self.player, movement)
            one_piece.change_lists(self.pos0, self.pos1, promotion)
            self.win.refresh_playing(promotion)

            if self.lets_advice:
                aud.join()
                thread_starter(self.sts.say, [self.advice])

            if self.player == 'Black':
                self.turn += 1

            self.player = 'Black' if self.player == 'White' else 'White'

            if "King" not in eval("lists.%sPieces" % self.player):
                self.match = False
            else:
                eval(self.good)

        else:
            self.win.correct_move(one_piece.answer)
            thread_starter(self.audio.repeat_move, [True if self.first_incorrect else False])
            self.first_incorrect = False

            eval(self.bad)
            cv2.waitKey(0)


class Teacher(PyCT):
    pass


class Tracker(PyCT):
    pass


class Player(PyCT):
    pass


if __name__ == '__main__':
    pyct = PyCT()
