#!/usr/bin/python

WhitePieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
               "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7", "Pawn_8"]

BlackPieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
               "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7", "Pawn_8"]

OccupiedSquares = {

        'White': {(1, 2): "Pawn",   (2, 2): "Pawn",   (3, 2): "Pawn",   (4, 2): "Pawn",
                  (5, 2): "Pawn",   (6, 2): "Pawn",   (7, 2): "Pawn",   (8, 2): "Pawn",
                  (1, 1): "Rook",   (8, 1): "Rook",   (2, 1): "Knight", (7, 1): "Knight",
                  (3, 1): "Bishop", (6, 1): "Bishop", (4, 1): "Queen",  (5, 1): "King"},

        'Black': {(1, 7): "Pawn",   (2, 7): "Pawn",   (3, 7): "Pawn",   (4, 7): "Pawn",
                  (5, 7): "Pawn",   (6, 7): "Pawn",   (7, 7): "Pawn",   (8, 7): "Pawn",
                  (1, 8): "Rook",   (8, 8): "Rook",   (2, 8): "Knight", (7, 8): "Knight",
                  (3, 8): "Bishop", (6, 8): "Bishop", (4, 8): "Queen",  (5, 8): "King"}

                   }

squares = {}
corners = []
points = []

rectified_squares = {}
rectified_corners = []
rectified_points = []


def occupied_squares():
    """Return black and white occupied squares."""

    t_dic = {}
    for dic in OccupiedSquares.values():
        t_dic.update(dic)
    return t_dic
