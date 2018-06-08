#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep

import lists

answer = str


class Piece:
    def __init__(self, aud):
        self.advice, self.answer, self.player, self.incorrect = [str]*4
        self.lets_advice = False

        self.audio = aud
        self.advices_source = self.audio.language

        self.columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.pieces = ["King", "Queen", "Bishop", "Knight", "Rook", "Pawn"]

        self.name = str(self.__class__).split('.')[2]
        self.abs_x = 0
        self.abs_y = 0
        self.abs_z = 0

        self.ad_pawn = 0

    def change_position(self, coordinates):
        """Tuple --> String"""

        column = self.columns[coordinates[0] - 1]
        row_1 = str(coordinates[1])
        row_2 = str(coordinates[2])
        return column + row_1 + row_2

    def inv_change_position(self, position):
        """String --> Tuple"""

        x = self.columns.index(position[0].upper()) + 1
        y = eval(position[1])
        z = eval(position[2])
        return tuple([x, y, z])

    def change_lists(self, e0, ef, promotion):
        pass

    def _check_move(self, moves, ans, jump=True):
        for move in moves:
            if move:
                if jump:
                    if not self._jump():
                        return True
                    else:
                        self._incorrect(self.audio.language.incorrect_move_001)
                        return False
                else:
                    return True
        else:
            self._incorrect(ans)
            return False

    def _jump(self):
        pass

    def _refresh(self, ax, ay, bx, by):
        self.ax, self.ay, self.bx, self.by = ax, ay, bx, by
        self.abs_x = abs(self.bx - self.ax)
        self.abs_y = abs(self.by - self.ay)
        self.abs_z = abs(self.bz - self.az)

    def _incorrect(self, ans):
        self.answer = self.audio.language.incorrect_move_000 + ans + "\n\n"

    def _general_advices(self, turn):
        self.lets_advice = False

        if self.name == 'Pawn':
            self.ad_pawn += 1

        if turn <= 7 and self.ad_pawn == 9:
            self.lets_advice = True
            self.advice = self.advices_source.aud_A01

        if turn == 7 and self.ad_pawn <= 6:
            self.lets_advice = True
            self.advice = self.advices_source.aud_A02


class Rook(Piece):
    def correct_move(self, a_x, a_y, a_z, b_x, b_y, b_z):
        self._refresh(a_x, a_y, b_x, b_y)

        move_1 = self.abs_x == 0
        move_2 = self.abs_y == 0
        move_3 = self.abs_z == 0

        return self._check_move([move_1, move_2, move_3],
                                self.audio.language.incorrect_move_003)

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class Knight(Piece):
    def correct_move(self, a_x, a_y, a_z, b_x, b_y, b_z, c_0, c_f):
        self._refresh(a_x, a_y, b_x, b_y)

        move_1 = self.abs_x == 1

        return self._check_move([move_1, move_2, move_3],
                                self.audio.language.incorrect_move_004,
                                jump=False)

    def piece_advices(self, *args):
        e1 = args[1]
        self._general_advices(args[-1])

        if e1[0] == 1 or e1[0] == 8 or e1[1] == 1 or e1[1] == 8 or e1[2] == 1 or e1[2] == 8:
            self.lets_advice = True
            self.advice = self.advices_source.aud_A03

        return self.lets_advice, self.advice


class Bishop(Piece):
    def correct_move(self, a_x, a_y, a_z, b_x, b_y, b_z, c_0, c_f):
        self._refresh(a_x, a_y, b_x, b_y)

        move = abs(b_x - a_x) == abs(b_y - a_y)

        return self._check_move([move], self.audio.language.incorrect_move_005)

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class Queen(Piece):
    def correct_move(self, a_x, a_y, a_z, b_x, b_y, b_z):
        self._refresh(a_x, a_y, b_x, b_y)

        move_1 = abs(b_y - a_y) > 0 and b_x - a_x == 0
        move_2 = abs(b_x - a_x) > 0 and b_y - a_y == 0
        move_3 = abs(b_x - a_x) == abs(b_y - a_y)

        return self._check_move([move_1, move_2, move_3],
                                self.audio.language.incorrect_move_006)

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class King(Piece):
    def correct_move(self, a_x, a_y, a_z, b_x, b_y, b_z):
        self._refresh(a_x, a_y, b_x, b_y)

        move_1 = self.abs_x == 1 and self.abs_y == self.abs_z == 0
        move_2 = self.abs_y == 1 and self.abs_x == self.abs_z == 0
        move_3 = self.abs_z == 1 and self.abs_x == self.abs_y == 0

        return self._check_move([move_1, move_2, move_3],
                                None)

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class Pawn(Piece):
    def correct_move(self, a_x, a_y, a_z, b_x, b_y, b_z):
        self._refresh(a_x, a_y, b_x, b_y)

        eaten = (b_x, b_y, b_z) in lists.occupied_squares()

        if self.player == 'White':
            move_1 = b_x-a_x == 1
            move_2 = b_x-a_x == 0 and (self.abs_y == 1 or self.abs_z == 1)

        elif self.player == 'Black':
            move_1 = b_y-a_y == -1
            move_2 = b_y-a_y == 0 and (self.abs_x == 1 or self.abs_z == 1)

        else:
            move_1 = b_z-a_z == 1
            move_2 = b_z-a_z == 0 and (self.abs_x == 1 or self.abs_y == 1)

        if not eaten:
            return True if move_1 else False
        else:
            return True if move_2 else False

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice
