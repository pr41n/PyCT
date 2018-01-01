#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep

import lists


class Piece:
    def __init__(self, aud):
        self.advice, self.answer = [str]*2
        self.lets_advice = False

        self.audio = aud
        self.advices_source = self.audio.language

        self.columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.pieces = ["King", "Queen", "Bishop", "Knight", "Rook", "Pawn"]

        self.name = str(self.__class__).split('.')[2]
        self.incorrect = str
        self.player = str

        self.ad_pawn = 0

    def inv_change_position(self, position):
        """String --> Tuple"""

        x = self.columns.index(position[0].upper()) + 1
        y = eval(position[1])
        return tuple([x, y])

    def change_position(self, coordinates):
        """Tuple --> String"""

        column = self.columns[coordinates[0] - 1]
        row = str(coordinates[1])
        return column + row

    def change_lists(self, e0, ef, promotion):
        other_player = 'White' if self.player == 'Black' else 'Black'

        # Initial parameters
        dic_1 = lists.OccupiedSquares[self.player]
        dic_2 = lists.OccupiedSquares[other_player]
        list_1 = eval("lists.{}Pieces".format(self.player))
        list_2 = eval("lists.{}Pieces".format(other_player))
        compar = ef[0] <= 4 if self.player == 'White' else ef[0] >= 4

        # Moving case
        del dic_1[e0]

        if self.name == "Pawn" and (ef[1] == 1 or ef[1] == 8):     # Promotion
            dic_1[ef] = promotion
            list_1.append(promotion)

            if "Pawn_%d" % ef[0] in list_1:
                promoted = "Pawn_%d" % ef[0]
            else:
                possible = [i for i in range(1, 9) if "Pawn_%d" % i in list_1]
                promoted = "Pawn_%d" % possible[0]

            list_1.remove(promoted)

        else:
            dic_1[ef] = self.name

        # Eating case
        if ef in dic_2:
            eaten = dic_2[ef]
            del dic_2[ef]

            if eaten == "Pawn":
                if "Pawn_%d" % ef[0] in list_2:
                    which = "Pawn_%d" % ef[0]
                else:
                    possible = [i for i in range(1, 9) if "Pawn_%d" % i in list_2]
                    which = "Pawn_%d" % possible[0]

                list_2.remove(which)

            elif eaten == "Queen":
                list_2.remove("Queen")

            elif eaten == "King":
                list_2.remove("King")

            else:
                for piece in self.pieces:
                    if eaten == piece:
                        list_2.remove(piece + "_2" if compar else piece + "_1")

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
        occupied_squares = lists.occupied_squares()

        if abs(self.bx - self.ax) == 1 or abs(self.by - self.ay) == 1:
            return False

        elif self.ax == self.bx or self.ay == self.by:
            con = self.ax == self.bx
            a = min((self.ay, self.by) if con else (self.ax, self.bx)) + 1
            b = max((self.ay, self.by) if con else (self.ax, self.bx))

            for i in range(a, b):
                j = (self.ax, i) if con else (i, self.ay)
                if j in occupied_squares:
                    return True

        elif abs(self.bx - self.ax) == abs(self.by - self.ay):
            a = 1
            b = abs(self.bx - self.ax)

            # First or third cuadrant
            con = self.ax < self.bx and self.ay < self.by or \
                self.ax > self.bx and self.ay > self.by

            n = min(self.ax, self.bx) if con else max(self.ax, self.bx)
            m = min(self.ay, self.by)

            for i in range(a, b):
                j = (n+i if con else n-i, m+i)
                if j in occupied_squares:
                    return True

    def _refresh(self, ax, ay, bx, by):
        self.ax, self.ay, self.bx, self.by = ax, ay, bx, by

    def _incorrect(self, ans):
        self.answer = self.audio.language.incorrect_move_000 + ans + "\n"

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
    def correct_move(self, a_x, a_y, b_x, b_y):
        self._refresh(a_x, a_y, b_x, b_y)

        move_1 = abs(b_x - a_x) > 0 and b_x - a_x == 0
        move_2 = abs(b_x - a_x) > 0 and b_y - a_y == 0

        return self._check_move([move_1, move_2],
                                self.audio.language.incorrect_move_003)

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class Knight(Piece):
    def correct_move(self, a_x, a_y, b_x, b_y):
        self._refresh(a_x, a_y, b_x, b_y)
        
        move_1 = abs(b_y-a_y) == 1 and abs(b_x-a_x) == 2
        move_2 = abs(b_y-a_y) == 2 and abs(b_x-a_x) == 1

        return self._check_move([move_1, move_2],
                                self.audio.language.incorrect_move_004,
                                jump=False)

    def piece_advices(self, *args):
        e1 = args[1]
        self._general_advices(args[-1])

        if e1[0] == 1 or e1[0] == 8 or e1[1] == 1 or e1[1] == 8:
            self.lets_advice = True
            self.advice = self.advices_source.aud_A03

        return self.lets_advice, self.advice

            
class Bishop(Piece):
    def correct_move(self, a_x, a_y, b_x, b_y):
        self._refresh(a_x, a_y, b_x, b_y)

        move = abs(b_x - a_x) == abs(b_y - a_y)

        return self._check_move([move], self.audio.language.incorrect_move_005)

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class Queen(Piece):
    def correct_move(self, a_x, a_y, b_x, b_y):
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
    def correct_move(self, a_x, a_y, b_x, b_y):
        self._refresh(a_x, a_y, b_x, b_y)

        move_1 = abs(b_x - a_x)
        move_2 = abs(b_y - a_y)
    
        if (move_1 == 1 or move_1 == 0) and (move_2 == 1 or move_2 == 0):
            return True

        elif move_1 == 2 and move_2 == 0:
            if a_x == 5 and not self._jump() and (b_x, b_y) not in lists.occupied_squares():
                try:
                    y = 1 if self.player == 1 else 8

                    if b_x == 7 and lists.OccupiedSquares[self.player][(8, y)] == "Rook":
                        del lists.OccupiedSquares[self.player][(8, y)]
                        lists.OccupiedSquares[self.player][(6, y)] = "Rook"

                    elif b_x == 3 and lists.OccupiedSquares[self.player][(1, y)] == "Rook":
                        del lists.OccupiedSquares[self.player][(1, y)]
                        lists.OccupiedSquares[self.player][(4, y)] = "Rook"

                except KeyError:
                    self._incorrect(self.audio.language.incorrect_move_008)
                    return False

                sleep(4)
                return True

            else:
                self._incorrect(self.audio.language.incorrect_move_008)
                return False

        else:
            self._incorrect(self.audio.language.incorrect_move_007)
            return False

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice


class Pawn(Piece):
    def correct_move(self, a_x, a_y, b_x, b_y):
        self._refresh(a_x, a_y, b_x, b_y)
        
        eaten = (b_x, b_y) in lists.OccupiedSquares['White'] or \
                (b_x, b_y) in lists.OccupiedSquares['Black']

        move_1 = (b_y-a_y == 1 or b_y-a_y == 2 and a_y == 2) and self.player == 'White'
        move_2 = (b_y-a_y == -1 or b_y-a_y == -2 and a_y == 7) and self.player == 'Black'

        if move_1 or move_2:
            if not self._jump():
                if b_x-a_x == 0 and not eaten or abs(b_x-a_x) == 1 and eaten:
                    return True
                else:
                    self._incorrect(self.audio.language.incorrect_move_002)
            else:
                self._incorrect(self.audio.language.incorrect_move_001)
        else:
            if not self._jump():
                self._incorrect(self.audio.language.incorrect_move_002)
        return False

    def piece_advices(self, *args):
        self._general_advices(args[-1])
        return self.lets_advice, self.advice
