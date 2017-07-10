from Listas import Listas

from time import sleep


def text(i, j):

        if (i or j) == "King":
            print "%s             %s" % (i, j)

        elif (i or j) == "Bishop_1" or (i or j) == "Bishop_2":
            print "%s         %s" % (i, j)

        elif (i or j) == "Queen":
            print "%s            %s" % (i, j)

        elif (i or j) == "Knight_1" or (i or j) == "Knight_2":
            print "%s         %s" % (i, j)

        else:
            print "%s           %s" % (i, j)


def text_b():
    print "=========================="
    print "Blancas          Negras"
    print "=========================="
    print "=========================="

    jugando_n = Listas.PiezasMayores_N + Listas.PiezasMenores_N
    jugando_b = Listas.PiezasMayores_B + Listas.PiezasMenores_B
    jugando = jugando_n + jugando_b
    n = 0

    for i in jugando:
        if jugando.count(i) == 2:
            text(i, i)
            jugando.delete(i)
            jugando.delete(i)

        elif jugando.count(i) == 1:
            if True:
                text(i, "")
                jugando.delete(i)
