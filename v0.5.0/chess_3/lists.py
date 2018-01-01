WhitePieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
               "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7"]

BlackPieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
               "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7"]

RedPieces = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rook_1", "Rook_2",
             "Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7"]


OccupiedSquares = {

        'White': {(1, 2, 0): "Pawn",   (2, 2, 0): "Pawn",   (3, 2, 0): "Pawn",   (4, 2, 0): "Pawn",
                  (5, 2, 0): "Pawn",   (6, 2, 0): "Pawn",   (7, 2, 0): "Pawn",
                  (1, 1, 0): "Rook",   (8, 1, 0): "Rook",   (2, 1, 0): "Knight", (7, 1, 0): "Knight",
                  (3, 1, 0): "Bishop", (6, 1, 0): "Bishop", (4, 1, 0): "Queen",  (5, 1, 0): "King"},

        'Black': {(1, 7, 0): "Pawn",   (2, 7, 0): "Pawn",   (3, 7, 0): "Pawn",   (4, 7, 0): "Pawn",
                  (5, 7, 0): "Pawn",   (6, 7, 0): "Pawn",   (7, 7, 0): "Pawn",
                  (1, 8, 0): "Rook",   (8, 8, 0): "Rook",   (2, 8, 0): "Knight", (7, 8, 0): "Knight",
                  (3, 8, 0): "Bishop", (6, 8, 0): "Bishop", (4, 8, 0): "Queen",  (5, 8, 0): "King"},

        'Red':   {(1, 7, 0): "Pawn",   (2, 7, 0): "Pawn",   (3, 7, 0): "Pawn",   (4, 7, 0): "Pawn",
                  (5, 7, 0): "Pawn",   (6, 7, 0): "Pawn",   (7, 7, 0): "Pawn",
                  (1, 8, 0): "Rook",   (8, 8, 0): "Rook",   (2, 8, 0): "Knight", (7, 8, 0): "Knight",
                  (3, 8, 0): "Bishop", (6, 8, 0): "Bishop", (4, 8, 0): "Queen",  (5, 8, 0): "King"}
                   }


def occupied_squares():
    """Return black and white occupied squares."""
    dic = {}
    for i in OccupiedSquares:
        dic.update(i)
    return dic
