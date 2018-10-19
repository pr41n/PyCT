WhitePieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
               "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7"]

BlackPieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
               "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7"]

RedPieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
             "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7"]


OccupiedSquares = {

        'White': {(1, 1, 5): "Pawn",   (1, 4, 8): "Pawn",   (2, 2, 5): "Pawn",   (2, 4, 7): "Pawn",
                  (3, 3, 0): "Pawn",   (3, 4, 5): "Pawn",   (3, 4, 6): "Pawn",
                  (1, 2, 6): "Rook",   (1, 3, 7): "Rook",   (1, 2, 5): "Knight", (1, 4, 7): "Knight",
                  (2, 3, 5): "Bishop", (2, 4, 6): "Bishop", (2, 3, 6): "Queen",  (1, 3, 6): "King"},

        'Black': {(5, 6, 5): "Pawn",   (5, 6, 6): "Pawn",   (5, 7, 7): "Pawn",   (5, 8, 8): "Pawn",
                  (6, 6, 5): "Pawn",   (7, 7, 5): "Pawn",   (8, 8, 5): "Pawn",
                  (6, 8, 6): "Rook",   (7, 8, 7): "Rook",   (7, 8, 5): "Knight", (5, 8, 7): "Knight",
                  (5, 7, 5): "Bishop", (6, 7, 5): "Bishop", (6, 7, 6): "Queen",  (6, 8, 6): "King"},

        'Red':   {(5, 1, 1): "Pawn",   (5, 2, 2): "Pawn",   (5, 3, 3): "Pawn",   (5, 4, 3): "Pawn",
                  (6, 4, 1): "Pawn",   (7, 4, 2): "Pawn",   (8, 4, 3): "Pawn",
                  (6, 2, 1): "Rook",   (7, 3, 1): "Rook",   (7, 2, 1): "Knight", (5, 4, 1): "Knight",
                  (5, 3, 2): "Bishop", (6, 4, 2): "Bishop", (6, 3, 2): "Queen",  (6, 3, 1): "King"}
                   }


def occupied_squares():
    """Return black and white occupied squares."""

    dic = {}
    for i in OccupiedSquares.values():
        dic.update(i)
    return dic
