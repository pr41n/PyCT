#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import sys
import copy
import cv2
from random import randint
from shutil import copy2

sys.path.append('..')
copy2('../chess_2/lists.py', 'cache/o_lists.py')
from cache import o_lists
from chess_2 import lists, pieces, video
from scripts import connection, memory, synth
from tmp import cleaner
import audio, func, window

pawn = pieces.Pawn(audio)
rook = pieces.Rook(audio)
knight = pieces.Knight(audio)
bishop = pieces.Bishop(audio)
queen = pieces.Queen(audio)
king = pieces.King(audio)


def clean_cache():
    lists.OccupiedSquares = copy.copy(o_lists.OccupiedSquares)
    lists.WhitePieces = copy.copy(o_lists.WhitePieces)
    lists.BlackPieces = copy.copy(o_lists.BlackPieces)


class Video(unittest.TestCase):
    def test_A(self):
        lista = ['A/00.jpg', 'A/01.jpg', 'A/02.jpg', 'A/03.jpg', 'A/04.jpg',
                 'A/05.jpg', 'A/06.jpg', 'A/07.jpg', 'A/08.jpg', 'A/09.jpg']

        movimientos = ['E2 E3', 'B8 C6', 'F1 C4', 'B7 B6', 'D1 H5',
                       'C8 A6', 'H5 F7', 'E8 F7', 'C4 F7']

        self.__iterar(lista, movimientos)
        clean_cache()

    def test_B(self):
        lista = [
            'B/00.jpg', 'B/01.jpg', 'B/02.jpg', 'B/03.jpg', 'B/04.jpg', 'B/05.jpg',
            'B/06.jpg', 'B/07.jpg', 'B/08.jpg', 'B/09.jpg', 'B/10.jpg',
            'B/11.jpg', 'B/12.jpg', 'B/13.jpg', 'B/14.jpg', 'B/15.jpg',
            'B/16.jpg', 'B/17.jpg', 'B/18.jpg', 'B/19.jpg', 'B/20.jpg'
        ]

        movimientos = [
            'D2 D4', 'E7 E5', 'D4 E5', 'B8 C6', 'G1 F3',
            'D7 D6', 'E5 D6', 'F8 D6', 'C1 D2', 'C8 G4',
            'H2 H3', 'D6 B4', 'H3 G4', 'C6 D4', 'D2 B4',
            'D4 F3', 'E2 F3', 'D8 D1', 'E1 D1', 'E8 C8',
        ]

        self.__iterar(lista, movimientos)
        clean_cache()

    def __iterar(self, images, movimientos):
        global pawn, rook, knight, bishop, queen, king
        main_image = images[0]

        chessboard = video.Calibration(main_image)
        detection = video.Detection(chessboard)
        cv2.destroyWindow('test')

        for image in images[1:]:
            index = images.index(image)

            self.jugador = 'Black' if index % 2 == 0 else 'White'

            sub_image = images[index - 1]

            antes, ahora = detection.board(cv2.imread(sub_image), cv2.imread(image), self.jugador)
            try:
                piece_name = lists.OccupiedSquares[self.jugador][antes]
                piece = eval(piece_name.lower())
                piece.player = self.jugador

            except KeyError:
                cv2.imshow('antes', cv2.imread(sub_image))
                cv2.imshow('ahora', cv2.imread(image))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            try:
                piece.change_lists(antes, ahora)
                movimiento = '%s %s' % (piece.change_position(antes), piece.change_position(ahora))

            except AttributeError:
                print piece, antes, ahora
                movimiento = "Nulo"

            try:
                self.assertEqual(movimiento, movimientos[index - 1])

            except AssertionError:
                cv2.imshow('antes', cv2.imread(sub_image))
                cv2.imshow('ahora', cv2.imread(image))
                cv2.waitKey(0)
                cv2.destroyAllWindows()


class Pieces(unittest.TestCase):
    def test_A(self):
        global pawn, knight, bishop, queen
        piezas = [pawn, knight, bishop, queen]

        # change and inv_change position
        for pieza in piezas:
            coor = (randint(1, 8), randint(1, 8))
            alnm = pieza.change_position(coor)
            self.assertEqual(pieza.inv_change_position(alnm), coor)

        # change lists
        knight.player = 'White'
        knight.change_lists((2, 1), (1, 3), None)
        self.assertEqual(lists.OccupiedSquares['White'][(1, 3)], "Knight")

        queen.player = 'Black'
        queen.change_lists((4, 8), (4, 1), None)
        self.assertTrue("Queen" not in lists.WhitePieces)

        pawn.player = 'White'
        pawn.change_lists((4, 2), (4, 8), "Queen")
        self.assertEqual(lists.OccupiedSquares['White'][(4, 8)], "Queen")
        self.assertTrue("Pawn_4" not in lists.WhitePieces)
        self.assertTrue("Queen" in lists.WhitePieces)

        clean_cache()

    def test_B(self):
        global king, rook

    def test_C(self):
        global rook, knight
        rook.player = 'White'
        self.assertFalse(rook.correct_move(1, 1, 1, 3))
        knight.player = 'Black'
        self.assertFalse(knight.correct_move(3, 8, 1, 6))

if __name__ == '__main__':
    unittest.main()