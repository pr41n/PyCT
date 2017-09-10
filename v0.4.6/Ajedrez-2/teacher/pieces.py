# -*- coding: cp1252 -*-

from time import sleep

import lists
import audio

player = int
answer = str


class Piece:
    def __init__(self):
        pass
    
    @staticmethod
    def incorrect(ans):
        global answer
        answer = audio.language.incorrect_move_000 + ans + "\n\n"

    @staticmethod
    def jump(Ax, Ay, Bx, By):
        occupied_squares = lists.occupied_squares()
    
        if abs(Bx - Ax) == 1 or abs(By - Ay) == 1:
            return False
    
        elif Ax == Bx:
            a = min(Ay, By) + 1
            b = max(Ay, By)
    
            for i in range(a, b):
                j = (Ax, i)
                if j in occupied_squares:
                    return True
    
        elif Ay == By:
            a = min(Ax, Bx) + 1
            b = max(Ax, Bx)
    
            for i in range(a, b):
                j = (i, Ay)
                if j in occupied_squares:
                    return True
    
        elif abs(Bx-Ax) == abs(By-Ay):
            h = abs(Bx-Ax)
    
            if Ax < Bx and Ay > By or Ax > Bx and Ay < By:
                a = max(Ax, Bx)
                b = min(Ay, By)
    
                for i in range(1, h):
                    j = (a-i, b+i)
                    if j in occupied_squares:
                        return True
    
            else:
                a = min(Ax, Bx)
                b = min(Ay, By)
    
                for i in range(1, h):
                    j = (a+i, b+i)
                    if j in occupied_squares:
                        return True


class Pawn(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        ahora = (Bx, By)

        lista_b = lists.OccupiedSquares['White']
        lista_n = lists.OccupiedSquares['Black']

        avance_x = Bx-Ax
        avance_y = By-Ay

        def comida():
            if (ahora in lista_b) or (ahora in lista_n):
                return True
            return False

        move_1 = (avance_y == 1 or avance_y == 2 and Ay == 2) and player == 1
        move_2 = (avance_y == -1 or avance_y == -2 and Ay == 7) and player == 2

        ans = audio.language.incorrect_move_002

        if move_1 or move_2:
            if not self.jump(Ax, Ay, Bx, By):

                if avance_x == 0 and not comida() or abs(avance_x) == 1 and comida():
                    return True

                else:
                    self.incorrect(ans)
                    return False
            else:
                self.incorrect(audio.language.incorrect_move_001)
        else:
            if self.jump(Ax, Ay, Bx, By):
                pass
            else:
                self.incorrect(ans)
            return False


class Rook(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        move_1 = abs(By-Ay) > 0 and Bx-Ax == 0
        move_2 = abs(Bx-Ax) > 0 and By-Ay == 0

        if move_1 or move_2:
            if not self.jump(Ax, Ay, Bx, By):
                return True
            else:
                self.incorrect(audio.language.incorrect_move_001)

        else:
            ans = audio.language.incorrect_move_003
            self.incorrect(ans)
            return False


class Knight(Piece):
    def correct_move(self, Ax, Ay, Bx, By):

        move_1 = abs(By-Ay) == 1 and abs(Bx-Ax) == 2
        move_2 = abs(By-Ay) == 2 and abs(Bx-Ax) == 1

        if move_1 or move_2:
            return True
        else:
            ans = audio.language.incorrect_move_004
            self.incorrect(ans)
            return False


class Bishop(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        move = abs(Bx-Ax) == abs(By-Ay)

        if move:
            if not self.jump(Ax, Ay, Bx, By):
                return True
            else:
                self.incorrect(audio.language.incorrect_move_001)

        else:
            ans = audio.language.incorrect_move_005
            self.incorrect(ans)
            return False


class Queen(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        move_1 = abs(By - Ay) > 0 and Bx - Ax == 0
        move_2 = abs(Bx - Ax) > 0 and By - Ay == 0
        move_3 = abs(Bx - Ax) == abs(By - Ay)

        if move_1 or move_2 or move_3:
            if not self.jump(Ax, Ay, Bx, By):
                return True
            else:
                self.incorrect(audio.language.incorrect_move_001)

        else:
            ans = audio.language.incorrect_move_006
            self.incorrect(ans)
            return False


class King(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        move_1 = abs(Bx-Ax)
        move_2 = abs(By-Ay)

        if (move_1 == 1 or move_1 == 0) and (move_2 == 1 or move_2 == 0):
            return True

        elif move_1 == 2 and move_2 == 0:
            ans = audio.language.incorrect_move_008

            if Ax == 5 and not self.jump(Ax, Ay, Bx, By):
                try:
                    y = 1 if player == 1 else 8
                    dic = 'White' if player == 1 else 'Black'

                    if Bx == 7 and lists.OccupiedSquares[dic][(8, y)] == "Rook":
                        del lists.OccupiedSquares[dic][(8, y)]
                        lists.OccupiedSquares[dic][(6, y)] = "Rook"

                    elif Bx == 3 and lists.OccupiedSquares[dic][(1, y)] == "Rook":
                        del lists.OccupiedSquares[dic][(1, y)]
                        lists.OccupiedSquares[dic][(4, y)] = "Rook"

                except KeyError:
                    self.incorrect(ans)
                    return False

                sleep(4)
                return True

            else:
                if self.jump(Ax, Ay, Bx, By):
                    pass
                else:
                    self.incorrect(ans)
                return False

        else:
            ans = audio.language.incorrect_move_007
            self.incorrect(ans)
            return False
