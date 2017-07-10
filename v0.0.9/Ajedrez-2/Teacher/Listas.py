PiezasMayores_B = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rock_1", "Rock_2"]
PiezasMenores_B = ["Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7", "Pawn_8"]

PiezasMayores_N = ["King", "Queen", "Bishop_1", "Bishop_2", "Knight_1", "Knight_2", "Rock_1", "Rock_2"]
PiezasMenores_N = ["Pawn_1", "Pawn_2", "Pawn_3", "Pawn_4", "Pawn_5", "Pawn_6", "Pawn_7", "Pawn_8"]

casillasOcupadas = {

        'Blancas': {(1, 2): "Pawn",   (2, 2): "Pawn",   (3, 2): "Pawn",   (4, 2): "Pawn",
                    (5, 2): "Pawn",   (6, 2): "Pawn",   (7, 2): "Pawn",   (8, 2): "Pawn",
                    (1, 1): "Rock",   (8, 1): "Rock",   (2, 1): "Knight", (7, 1): "Knight",
                    (3, 1): "Bishop", (6, 1): "Bishop", (4, 1): "Queen",  (5, 1): "King"},

        'Negras': { (1, 7): "Pawn",   (2, 7): "Pawn",   (3, 7): "Pawn",   (4, 7): "Pawn",
                    (5, 7): "Pawn",   (6, 7): "Pawn",   (7, 7): "Pawn",   (8, 7): "Pawn",
                    (1, 8): "Rock",   (8, 8): "Rock",   (2, 8): "Knight", (7, 8): "Knight",
                    (3, 8): "Bishop", (6, 8): "Bishop", (4, 8): "Queen",  (5, 8): "King"}

                        }

casillas = {}
esquinas = []
puntos = []

rectify_squares = {}
rectify_corners = []
rectify_points = []


def casillas_ocupadas():

    casillasOcupadas_T = {}

    for i in casillasOcupadas:

        for j in casillasOcupadas[i]:
            casillasOcupadas_T[j] = casillasOcupadas[i][j]

    return casillasOcupadas_T
