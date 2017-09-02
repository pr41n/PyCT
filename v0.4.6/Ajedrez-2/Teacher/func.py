# -*- coding: cp1252 -*-

import threading
import time

from tmp import cleaner

import lists
import memory


def change_piece(a):
    """Translation english-spanish."""

    if a == "Pawn":
        a = u"Peón"
    elif a == "Rook":
        a = "Torre"
    elif a == "Knight":
        a = "Caballo"
    elif a == "Bishop":
        a = "Alfil"
    elif a == "Queen":
        a = "Reina"
    elif a == "King":
        a = "Rey"

    return a


def inv_change_piece(a):
    """Translation spanish-english.
    It is only used in the promotion, so there are no pawn nor king."""

    if a.capitalize() == "Torre":
        a = "Rook"
    elif a.capitalize() == "Caballo":
        a = "Knight"
    elif a.capitalize() == "Alfil":
        a = "Bishop"
    elif a.capitalize() == "Reina":
        a = "Queen"

    return a


columns = ["A", "B", "C", "D", "E", "F", "G", "H"]


def change_position(coordinates):
    """Tuple --> String"""

    column = columns[coordinates[0] - 1]
    row = str(coordinates[1])
    return column + row


def inv_change_position(position):
    """String --> Tuple"""

    x = columns.index(position[0].upper()) + 1
    y = eval(position[1])
    return tuple([x, y])


def change_lists(which, e0, ef, player, p):

    high_1, low_1, high_2, low_2 = give_values(list, 4)
    list_1, list_2 = give_values(dict, 2)
    compar_1, compar_2 = give_values(str, 2)

    #

    if player == 1:
        list_1 = lists.OccupiedSquares['White']
        list_2 = lists.OccupiedSquares['Black']

        high_1 = lists.WhiteHighPieces
        low_1 = lists.WhiteLowPieces

        high_2 = lists.BlackHighPieces
        low_2 = lists.BlackLowPieces

        compar_1 = "ef[0] <= 4"
        compar_2 = "ef[0] > 4"

    elif player == 2:
        list_1 = lists.OccupiedSquares['Black']
        list_2 = lists.OccupiedSquares['White']

        high_1 = lists.BlackHighPieces
        low_1 = lists.BlackLowPieces

        high_2 = lists.WhiteHighPieces
        low_2 = lists.WhiteLowPieces

        compar_1 = "ef[0] >= 4"
        compar_2 = "ef[0] < 4"

    #

    del list_1[e0]

    if which == "Pawn" and (ef[1] == 1 or ef[1] == 8):
        p = inv_change_piece(p)

        list_1[ef] = p
        high_1.append(p)

        if "Pawn_%s" % ef[0] in low_1:
            low_1.remove("Pawn_%s" % ef[0])

        else:
            for i in range(1, 9):

                j = "Pawn_%s" % i
                if j in low_1:

                    low_1.remove(j)
                    break

    else:
        list_1[ef] = which

    if ef in list_2:                   # A piece has been eaten.
        eaten = list_2[ef]
        del list_2[ef]

        if eaten == "Pawn":

            if "Pawn_%s" % ef[0] in low_2:
                low_2.remove("Pawn_%s" % ef[0])

            else:
                for i in range(1, 9):

                    j = "Pawn_%s" % i
                    if j in low_2:
                        low_2.remove(j)
                        break

        elif eaten == "Rook":
            if eval(compar_1):
                high_2.remove("Rook_2")

            elif eval(compar_2):
                high_2.remove("Rook_1")

        elif eaten == "Knight":
            if eval(compar_1):
                high_2.remove("Knight_2")

            elif eval(compar_2):
                high_2.remove("Knight_1")

        elif eaten == "Bishop":
            if eval(compar_1):
                high_2.remove("Bishop_2")

            elif eval(compar_2):
                high_2.remove("Bishop_1")

        elif eaten == "Queen":
            high_2.remove("Queen")

        elif eaten == "King":
            high_2.remove("King")


def thread_starter(to_thread, args=()):
    """Start a new daemon thread."""

    thread = threading.Thread(target=to_thread, args=args)
    thread.setDaemon(True)
    thread.start()

    return thread


def video_exit(k):
    """Add different options during video streams."""

    if k == ord('m'):       # Print used memory
        memory.main()

    elif k == 227:          # Close the program cleaning cache
        cleaner.Clean.images()
        cleaner.Clean.pyc()
        exit(11)

    elif k == ord('t'):     # Print the count of active threads
        print threading.activeCount()


def prevent_auido_error(text):
    """Start a loop if an audio is being said."""

    from audio import sts       # Imported here to prevent ImportError between Audio and Functions modules

    try:
        sts.say(text)

    except RuntimeError:
        time.sleep(0.1)
        prevent_auido_error(text)


def give_values(value, n):
    """Give n times the recieved value."""
    A = []
    for x in range(n):
        A.append(value)
    return A
