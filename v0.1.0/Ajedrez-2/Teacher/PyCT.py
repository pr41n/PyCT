# -*- coding: cp1252 -*-

import cv2

import Audio
import Pieces
from Functions import *
from Window import OpenCV, Window
from Video import Detection, Calibration, Camera

clean = Clean()
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

        self.audio = Audio.selected_idiom

        self.language = Audio.language

        self.advices = Audio.Advice()
        self.advices.main()

        self.sts = Audio.sts

        intro = thread_starter(self.audio.intro)
        intro.join()

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

        clean.images()

        self.good, self.bad, self.checkmate = self.arduino_conection()

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
            error = False, None
            pos0, pos1 = self.detect_move()

            try:
                piece, move = self.detect_piece()
                self.check_move(piece, move)

            except (KeyError, AttributeError, TypeError) as err:
                error = True, err

            if error[0]:
                err = error[1]
                print "Detection Error: {}".format(err)
                thread_starter(self.audio.error_1)
                if cv2.waitKey(0) & 0xFF == 27:
                    pos0, pos1 = self.win.movement(None)

                    piece, move = self.detect_piece()
                    self.check_move(piece, move)

        player = 'blancas' if self.player == 1 else 'negras'

        eval(self.checkmate)

        thread_starter(self.audio.check_mate, [player, self.turn - 1])
        time.sleep(2)
        prevent_auido_error(" ")

        video_exit(227)

    def calibrated(self, first_attempt):
        global calibration
        OpenCV('Coloca el tablero', 1100, -100, 440, 350)

        while True:
            k = cv2.waitKey(1) & 0xFF

            ret, frame = self.cam.read()
            cv2.imshow('Coloca el tablero', frame)
            cv2.imwrite('PythonCache/frame.jpg', frame)
            self.win.video('PythonCache/frame.jpg')

            if k == 10:
                cv2.destroyWindow('Coloca el tablero')
                if first_attempt:
                    thread_starter(self.audio.calibration, [2])
                    self.win.calibration_instructions()

                cv2.imwrite('PythonCache/ChessBoard.jpg', frame)
                calibration = Calibration('PythonCache/ChessBoard.jpg')
                cv2.destroyWindow('Calibrate')
                break

            video_exit(k)

        return calibration.value()

    def arduino_conection(self):
        global arduino
        try:
            from Connection import Arduino
            arduino = Arduino(2)

            thread_starter(self.audio.arduino, [True])
            delay = 0

            return 'arduino.write(\'a\', %s)' % delay, \
                   'arduino.write(\'b\', %s)' % delay, \
                   'arduino.write(\'c\', %s)' % delay

        except OSError:
            thread_starter(self.audio.arduino, [False])
            return 'None', 'None', 'None'

    def detect_move(self):
        global pos0, pos1, calibration, rectified
        instructions = cv2.imread('Instructions/Video.png')
        try:
            move = False
            OpenCV('Sobre esta ventana pulsa:', 490, 485, 435, 170)
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

                cv2.imshow('Sobre esta ventana pulsa:', instructions)
                cv2.imwrite('PythonCache/frame.jpg', img)
                self.win.video('PythonCache/frame.jpg')

                video_exit(k)

                if not move:
                    move = True
                    cv2.imwrite('PythonCache/origin.jpg', frame)
                    original = 'PythonCache/origin.jpg'

                elif k == 32 and move:
                    cv2.imwrite('PythonCache/now.jpg', frame)
                    now = 'PythonCache/now.jpg'

                    detection = Detection(original, now, self.player)
                    pos0, pos1 = detection.Board()
                    return pos0, pos1

                elif k == 27:
                    pos0, pos1 = self.win.movement(None)
                    return pos0, pos1

        except cv2.error:
            thread_starter(self.audio.error_2)
            pos0, pos1 = self.win.movement(None)
            return pos0, pos1

        except IndexError:
            thread_starter(self.audio.error_2)
            pos0, pos1 = self.win.movement(None)
            return pos0, pos1

    def detect_piece(self):
        who, which = give_values(None, 2)

        occupied_squares = Lists.occupied_squares()

        if occupied_squares[pos0] == "Pawn":
            from Pieces import Pawn
            who = Pawn()
            which = "Pawn"

            self.n_pawns_1 += 1
            if self.turn <= 15 and self.n_pawns_1 == 9:
                self.lets_advice = True
                self.advice = self.advices.pawn_1

        elif occupied_squares[pos0] == "Rock":
            from Pieces import Rock
            who = Rock()
            which = "Rock"
            self.n_pawns_2 += 1

        elif occupied_squares[pos0] == "Knight":
            from Pieces import Knight
            who = Knight()
            which = "Knight"
            self.n_pawns_2 += 1

            if pos1[0] == 1 or pos1[0] == 8or pos1[1] == 1 or pos1[1] == 8:
                self.n_knight += 1
                if self.n_knight < 3:
                    self.lets_advice = True
                    self.advice = self.advices.knight

        elif occupied_squares[pos0] == "Bishop":
            from Pieces import Bishop
            who = Bishop()
            which = "Bishop"
            self.n_pawns_2 += 1

        elif occupied_squares[pos0] == "Queen":
            from Pieces import Queen
            who = Queen()
            which = "Queen"
            self.n_pawns_2 += 1

        elif occupied_squares[pos0] == "King":
            from Pieces import King
            who = King()
            which = "King"
            self.n_pawns_2 += 1

        if self.n_pawns_2 == 6:
            self.advice = self.advices.pawn_2
            self.n_pawns_2 += 1

        return which, who
        
    def check_move(self, which, who):
        global pos0, pos1, arduino

        Pieces.player = self.player
        occupied_squares = Lists.occupied_squares()

        if who.correct_move(pos0[0], pos0[1], pos1[0], pos1[1]):

            H = "Turno %s" % self.turn, "Jugador %s" % self.player
            J = int
            K = None

            if which == "King" and pos0[0] == 5 and pos1[1] - pos0[1] == 0 and abs(pos1[0] - pos0[0]) == 2:
                if pos1[0] == 3:
                    J = thread_starter(self.audio.castling, ['QueenSide'])
                    H = H, u"Enroque largo"

                elif pos1[0] == 7:
                    J = thread_starter(self.audio.castling, ['KingSide'])
                    H = H, u"Enroque corto"

            elif which == "Pawn" and (pos1[1] == 8 or pos1[1] == 1):
                K = self.win.promote()
                K = K.capitalize()
                J = thread_starter(self.audio.promotion, [change_piece(K)])
                H = H, u"%s corona" % change_piece(K)

            elif pos1 in occupied_squares:
                J = thread_starter(self.audio.play, [change_piece(which), change_position(pos1), True])
                H = H, u"%s por %s" % (change_piece(which), change_position(pos1))

            else:
                J = thread_starter(self.audio.play, [change_piece(which), change_position(pos1), False])
                H = H, u"%s a %s" % (change_piece(which), change_position(pos1))

            self.win.print_move(H[0][0], H[0][1], H[1])

            if self.lets_advice:
                J.join()
                thread_starter(self.sts.say, [self.advice])
                self.lets_advice = False

            #

            change_lists(which, pos0, pos1, self.player, K)
            self.win.refresh_playing(K, self.player)
            self.turn += 1

            #

            if self.player == 1:
                if "King" not in Lists.BlackHighPieces:
                    self.match = False
                else:
                    self.player = 2

            elif self.player == 2:
                if "King" not in Lists.WhiteHighPieces:
                    self.match = False
                else:
                    self.player = 1

            eval(self.good)

        else:
            global z
            self.win.print_incorrect_move()
            thread_starter(self.audio.repeat_move, [z])
            
            if z:
                z = False
                
            cv2.waitKey(0)
            eval(self.bad)

    def test(self):
        import Pieces
        for i in range(4):
            Pieces.answer = "Prueba\n\n"
            self.win.print_incorrect_move()
            self.win.main()

if __name__ == '__main__':
    pyct = PyCT()
