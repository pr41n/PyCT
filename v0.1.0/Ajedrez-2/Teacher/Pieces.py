# -*- coding: cp1252 -*-

from time import sleep

import Lists

player = int
answer = str


class Piece:
    def __init__(self):
        pass
    
    @staticmethod
    def incorrect(ans):
        global answer
        answer = "Jugada incorrect:\n    " + ans + "\n\n"

    @staticmethod
    def jump(Ax, Ay, Bx, By):
        occupied_squares = Lists.occupied_squares()
    
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

        lista_b = Lists.OccupiedSquares['White']
        lista_n = Lists.OccupiedSquares['Black']

        avance_x = Bx-Ax
        avance_y = By-Ay

        def comida():
            if (ahora in lista_b) or (ahora in lista_n):
                return True

            else:
                return False

        move_1 = (avance_y == 1 or avance_y == 2 and Ay == 2) and player == 1
        move_2 = (avance_y == -1 or avance_y == -2 and Ay == 7) and player == 2

        ans = u"El peón avanza en línea recta y come en diagonal. Siempre \n" \
              u"avanzando una fila. Si es la primera vez que lo mueves, \n" \
              u"puede avanzar dos casillas en línea recta"

        if move_1 or move_2:
            if not self.jump(Ax, Ay, Bx, By):

                if avance_x == 0 and not comida() or abs(avance_x) == 1 and comida():
                    return True

                else:
                    self.incorrect(ans)
                    return False
            else:
                self.incorrect(u"La única pieza que puede saltar a otras es el caballo")
        else:
            if self.jump(Ax, Ay, Bx, By):
                pass
            else:
                self.incorrect(ans)
            return False


class Rock(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        move_1 = abs(By-Ay) > 0 and Bx-Ax == 0
        move_2 = abs(Bx-Ax) > 0 and By-Ay == 0

        if move_1 or move_2:
            if not self.jump(Ax, Ay, Bx, By):

                return True
            else:
                self.incorrect(u"La única pieza que puede saltar a otras es el caballo.")

        else:
            ans = u"La torre se mueve en línea recta."
            self.incorrect(ans)
            return False


class Knight(Piece):
    def correct_move(self, Ax, Ay, Bx, By):

        move_1 = abs(By-Ay) == 1 and abs(Bx-Ax) == 2
        move_2 = abs(By-Ay) == 2 and abs(Bx-Ax) == 1

        if move_1 or move_2:

            return True
        else:
            ans = u"El caballo se mueve dos casillas horizontalmente y una vertical\n" \
                        u"    o viceversa, de modo que forme una L."
            self.incorrect(ans)
            return False


class Bishop(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        move = abs(Bx-Ax) == abs(By-Ay)

        if move:
            if not self.jump(Ax, Ay, Bx, By):

                return True
            else:
                self.incorrect(u"La única pieza que puede saltar a otras es el caballo.")

        else:
            ans = u"El alfil se mueve en diagonal."
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
                self.incorrect(u"La única pieza que puede saltar a otras es el caballo.")

        else:
            ans = u"La reina se mueve como un alfil y una torre a la vez, es decir,\n" \
                        u"recto o en diagonal."
            self.incorrect(ans)
            return False


class King(Piece):
    def correct_move(self, Ax, Ay, Bx, By):
        """
        El enroque solo toma el movimiento del rey,
        el programa se duerme un tiempo para permitir al player mover la torre
        """
        move_1 = abs(Bx-Ax)
        move_2 = abs(By-Ay)

        if (move_1 == 1 or move_1 == 0) and (move_2 == 1 or move_2 == 0):

            return True

        elif move_1 == 2 and move_2 == 0:

            if Ax == 5 and not self.jump(Ax, Ay, Bx, By):

                if player == 1:

                    if Bx == 7 and Lists.OccupiedSquares['White'][(8, 1)] == "Rock":

                        del Lists.OccupiedSquares['White'][(8, 1)]
                        Lists.OccupiedSquares['White'][(6, 1)] = "Rock"

                    elif Bx == 3 and Lists.OccupiedSquares['White'][(1, 1)] == "Rock":

                        del Lists.OccupiedSquares['White'][(1, 1)]
                        Lists.OccupiedSquares['White'][(4, 1)] = "Rock"

                #

                elif player == 2:

                    if Bx == 7 and Lists.OccupiedSquares['Black'][(8, 8)] == "Rock":

                        del Lists.OccupiedSquares['Black'][(8, 8)]
                        Lists.OccupiedSquares['Black'][(6, 8)] = "Rock"

                    elif Bx == 3 and Lists.OccupiedSquares['Black'][(1, 8)] == "Rock":

                        del Lists.OccupiedSquares['Black'][(1, 8)]
                        Lists.OccupiedSquares['Black'][(4, 8)] = "Rock"

                sleep(2)

                return True

            else:
                ans = u"El rey solo puede enrocar si ni él ni la torre del lado en el\n" \
                            u"que se va a enrocar se han movido antes,\npor lo que es en la\n" \
                            u"misma fila. Además, no debe haber ninguna pieza entre la torre\n" \
                            u" y el rey. Existen dos enroques:\n" \
                            u"   Enroque corto: el rey se mueve a la columna G y la torre a la F.\n" \
                            u"   Enroque largo: el rey se mueve a la columna C y la torre a la D."
                if self.jump(Ax, Ay, Bx, By):
                    pass
                else:
                    self.incorrect(ans)
                return False

        else:
            ans = u"El rey solo puede avanzar una casilla en todas direcciones."
            self.incorrect(ans)
            return False
