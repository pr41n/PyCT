# -*- coding: cp1252 -*-

from time import sleep

import cv2
import numpy as np

import audio
import lists
import pieces
from func import thread_starter, prevent_auido_error, give_values, video_exit, \
                 change_position, change_lists

from video import Detection, Calibration, Camera
from window import OpenCV, Window
from scripts import connection

calibration, pos0, pos1, arduino = give_values(None, 4)
rectified = False
z = True


class PyCT:
    def __init__(self, testing=False):
        self.win = Window()
        self.win.main()

        if testing:
            self.test()
            exit(12)

        self.audio = audio.Language()

        self.language = audio.language.babel

        self.advices = audio.Advice()
        self.advices.main()

        self.sts = audio.sts

        thread_starter(self.audio.intro).join()

        camera = Camera()
        cam_chosen = camera.choose()
        self.cam = cv2.VideoCapture(cam_chosen)

        thread_starter(self.audio.calibration, [1])

        attempt1 = True
        while True:
            if self.calibrated(attempt1):
                break
            attempt1 = False

        self.win.label.set_text("")

        self.good, self.bad, self.checkmate = self.arduino_conection()

        thread_starter(self.audio.detection).join()
        self.sort_of_detection = self.win.sort_of_detection()
        print self.sort_of_detection

        self.player = 1
        self.turn = 1
        self.match = True

        self.lets_advice = False
        self.n_pawns_1 = 0
        self.n_pawns_2 = 0
        self.n_knight = 0
        self.advice = str

        thread_starter(self.audio.match)

        global pos0, pos1, rectified

        while self.match:
            try:
                sleep(0.1)
                if self.sort_of_detection == 'automatic':
                    pos0, pos1 = self.detect_move_automatically()
                else:
                    pos0, pos1 = self.detect_move()

            except EnvironmentError:
                continue

            try:
                piece = self.detect_piece()
                self.check_move(piece)

            except (KeyError, AttributeError, TypeError) as err:
                print "Detection Error: {}".format(err)
                thread_starter(self.audio.error_1)
                if cv2.waitKey(0) & 0xFF == 27:
                    pos0, pos1 = self.win.movement(None)

                    piece, move = self.detect_piece()
                    self.check_move(piece)

        player = audio.language.player_1 if self.player == 1 else audio.language.player_2

        eval(self.checkmate)

        thread_starter(self.audio.check_mate, [player, self.turn - 1])
        sleep(2)
        prevent_auido_error(self.audio.say, " ")
        global arduino
        arduino.write('r')
        video_exit(227)

    def calibrated(self, first_attempt):
        global calibration
        OpenCV(audio.language.open_cv_1, 1100, -100, 440, 350)

        while True:
            k = cv2.waitKey(1) & 0xFF

            ret, frame = self.cam.read()
            cv2.imshow(audio.language.open_cv_1, frame)
            cv2.imwrite('tmp/frame.jpg', frame)
            self.win.video('tmp/frame.jpg')

            if k == 10:
                cv2.destroyWindow(audio.language.open_cv_1)
                if first_attempt:
                    thread_starter(self.audio.calibration, [2])
                    self.win.calibration_instructions()

                cv2.imwrite('tmp/ChessBoard.jpg', frame)
                calibration = Calibration('tmp/ChessBoard.jpg')
                cv2.destroyWindow(audio.language.open_cv_2)
                break

            video_exit(k)

        return calibration.value()

    def arduino_conection(self):
        global arduino
        try:
            arduino = connection.Arduino(2)

            thread_starter(self.audio.arduino, [True])
            delay = 0

            return "arduino.write('a', %s)" % delay, \
                   "arduino.write('b', %s)" % delay, \
                   "arduino.write('c', %s)" % delay

        except OSError:
            thread_starter(self.audio.arduino, [False])
            return 'None', 'None', 'None'

    def detect_move(self):
        """Detects manual and semi-automatic moves,
        because of the only difference between them
        is press the space bar once or twice"""

        global pos0, pos1, calibration, rectified
        language = cv2.imread('languages/Video.png')
        try:
            move = False
            OpenCV(audio.language.open_cv_3, 490, 485, 435, 170)
            original = None
            while True:
                k = cv2.waitKey(1)

                ret, frame = self.cam.read()
                if k == ord('r'):
                    if rectified:
                        rectified = False
                    else:
                        rectified = True

                if rectified:
                    img = calibration.rectify_image(frame)
                else:
                    img = frame

                cv2.imshow(audio.language.open_cv_3, language)
                cv2.imwrite('tmp/frame.jpg', img)
                self.win.video('tmp/frame.jpg')

                video_exit(k)

                if (k == 32 and self.sort_of_detection == 'manual' or
                   self.sort_of_detection == 'semi-automatic') and not move:

                    move = True
                    cv2.imwrite('tmp/origin.jpg', frame)
                    original = 'tmp/origin.jpg'

                elif k == 32 and move:
                    cv2.imwrite('tmp/now.jpg', frame)
                    now = 'tmp/now.jpg'

                    detection = Detection(original, now, self.player)
                    pos0, pos1 = detection.Board()
                    return pos0, pos1

                elif k == 27:
                    pos0, pos1 = self.win.movement(None)
                    return pos0, pos1

        except (cv2.error, IndexError):
            thread_starter(self.audio.error_2)
            pos0, pos1 = self.win.movement(None)
            return pos0, pos1

    def detect_move_automatically(self):
        """Detects the move automatically using histograms."""

        global pos0, pos1, calibration, rectified
        instructions = cv2.imread('languages/Video.png')
        try:
            OpenCV(audio.language.open_cv_3, 490, 485, 435, 170)
            first_frame = 10
            moving, moved, show_diff = give_values(False, 3)
            origin = None
            original = None
            while True:
                k = cv2.waitKey(1)

                ret, frame = self.cam.read()
                if k == ord('r'):
                    if rectified:
                        rectified = False
                    else:
                        rectified = True

                if rectified:
                    img = calibration.rectify_image(frame)
                else:
                    img = frame

                cv2.imshow(audio.language.open_cv_3, instructions)
                cv2.imwrite('tmp/frame.jpg', img)
                self.win.video('tmp/frame.jpg')

                video_exit(k)

                if k == 27:
                    pos0, pos1 = self.win.movement(None)
                    return pos0, pos1

                elif k == ord('s'):
                    if not show_diff:
                        show_diff = True
                    else:
                        show_diff = False
                        cv2.destroyWindow('diff')
                        cv2.destroyWindow('histogram')

                if first_frame > 0:
                    origin = frame
                    original = 'tmp/origin.jpg'
                    cv2.imwrite(original, frame)
                    first_frame -= 1

                diff = cv2.absdiff(calibration.rectify_image(frame),
                                   calibration.rectify_image(origin))
                im = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

                histogram = cv2.calcHist([im], [0], None, [256], [0, 256])

                hist = np.ones((256, 256))
                hist[:] = histogram

                if show_diff:
                    cv2.imshow('diff', im)
                    cv2.imshow('histogram', hist)

                n = 0
                for i in histogram:
                    if i > 1000:
                        n += 1

                if moving and n < 21:
                        sleep(1)
                        now = 'tmp/now.jpg'
                        cv2.imwrite(now, frame)
                        """
                        cv2.imshow('frame', frame)
                        cv2.imshow('origin', origin)
                        cv2.waitKey(0)
                        cv2.destroyWindow('origin')
                        cv2.destroyWindow('frame')
                        """
                        detection = Detection(original, now, self.player)
                        pos0, pos1 = detection.Board()
                        if show_diff:
                            cv2.destroyWindow('diff')
                            cv2.destroyWindow('histogram')
                        return pos0, pos1

                if n > 30:
                    moving = True

        except (cv2.error, IndexError):
            thread_starter(self.audio.error_2)
            pos0, pos1 = self.win.movement(None)
            return pos0, pos1

    def detect_piece(self):
        occupied_squares = lists.occupied_squares()

        if occupied_squares[pos0] == "Pawn":
            self.n_pawns_1 += 1
            if self.turn <= 15 and self.n_pawns_1 == 9:
                self.lets_advice = True
                self.advice = self.advices.pawn_1

        elif occupied_squares[pos0] == "Rook":
            self.n_pawns_2 += 1

        elif occupied_squares[pos0] == "Knight":
            self.n_pawns_2 += 1

            if pos1[0] == 1 or pos1[0] == 8or pos1[1] == 1 or pos1[1] == 8:
                self.n_knight += 1
                if self.n_knight < 2:
                    self.lets_advice = True
                    self.advice = self.advices.knight

        elif occupied_squares[pos0] == "Bishop":
            self.n_pawns_2 += 1

        elif occupied_squares[pos0] == "Queen":
            self.n_pawns_2 += 1

        elif occupied_squares[pos0] == "King":
            self.n_pawns_2 += 1

        if self.n_pawns_2 == 6:
            self.advice = self.advices.pawn_2
            self.n_pawns_2 += 1

        who = eval('pieces.%s()' % occupied_squares[pos0])
        return who
        
    def check_move(self, who):
        global pos0, pos1, arduino

        pieces.player = self.player
        occupied_squares = lists.occupied_squares()
        which = occupied_squares[pos0]

        if who.correct_move(pos0[0], pos0[1], pos1[0], pos1[1]):

            H = "%s %d" % (audio.language.turn, self.turn), "%s %d" % (audio.language.player, self.player)
            J = int
            K = None

            if which == "King" and pos0[0] == 5 and pos1[1] - pos0[1] == 0 and abs(pos1[0] - pos0[0]) == 2:
                if pos1[0] == 3:
                    J = thread_starter(self.audio.castling, ['QueenSide'])
                    H = H, audio.language.aud_025

                elif pos1[0] == 7:
                    J = thread_starter(self.audio.castling, ['KingSide'])
                    H = H, audio.language.aud_024

            elif which == "Pawn" and (pos1[1] == 8 or pos1[1] == 1):
                K = self.win.promote()
                K = K.capitalize()
                J = thread_starter(self.audio.promotion, [self.win.translate(K, audio.language)])
                H = H, audio.language.aud_023 % self.win.translate(K, audio.language)

            elif pos1 in occupied_squares:
                J = thread_starter(self.audio.play, [self.win.translate(which, audio.language),
                                                     change_position(pos1), True])

                H = H, audio.language.aud_014 % (self.win.translate(which, audio.language), change_position(pos1))

            else:
                J = thread_starter(self.audio.play, [self.win.translate(which, audio.language),
                                                     change_position(pos1), False])

                H = H, audio.language.aud_015 % (self.win.translate(which, audio.language), change_position(pos1))

            self.win.print_move(H[0][0], H[0][1], H[1])

            if self.lets_advice:
                J.join()
                thread_starter(self.sts.say, [self.advice])
                self.lets_advice = False

            #

            change_lists(which, pos0, pos1, self.player, K)
            self.win.refresh_playing(K, self.player)

            #

            if self.player == 1:
                if "King" not in lists.BlackPieces:
                    self.match = False
                else:
                    self.player = 2
                    eval(self.good)

            elif self.player == 2:
                if "King" not in lists.WhitePieces:
                    self.match = False
                else:
                    self.player = 1
                    self.turn += 1
                    eval(self.good)


        else:
            global z
            self.win.print_incorrect_move()
            thread_starter(self.audio.repeat_move, [z])
            
            if z:
                z = False
                
            eval(self.bad)
            cv2.waitKey(0)

    def test(self):
        import pieces
        for i in range(4):
            pieces.answer = "Prueba\n\n"
            self.win.print_incorrect_move()
            self.win.main()


if __name__ == '__main__':
    pyct = PyCT()
