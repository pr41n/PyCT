#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from time import sleep

import lists
from scripts import memory
from tmp import cleaner

local_memory = memory.Memory()
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

    list_1, list_2 = give_values(list, 2)
    dic_1, dic_2 = give_values(dict, 2)
    compar_1, compar_2 = give_values(str, 2)

    #
    # Selecting containers based in the player

    if player == 1:
        dic_1 = lists.OccupiedSquares['White']
        dic_2 = lists.OccupiedSquares['Black']

        list_1 = lists.WhitePieces
        list_2 = lists.BlackPieces

        compar_1 = ef[0] <= 4
        compar_2 = ef[0] > 4

    elif player == 2:
        dic_1 = lists.OccupiedSquares['Black']
        dic_2 = lists.OccupiedSquares['White']

        list_1 = lists.BlackPieces
        list_2 = lists.WhitePieces

        compar_1 = ef[0] >= 4
        compar_2 = ef[0] < 4

    #

    del dic_1[e0]

    if which == "Pawn" and (ef[1] == 1 or ef[1] == 8):      # Pawn case
        dic_1[ef] = p
        list_1.append(p)

        if "Pawn_%s" % ef[0] in list_1:
            list_1.remove("Pawn_%s" % ef[0])

        else:
            for i in range(1, 9):

                j = "Pawn_%s" % i
                if j in list_1:

                    list_1.remove(j)
                    break

    else:       # Another piece case
        dic_1[ef] = which

    if ef in dic_2:     # Piece eaten
        eaten = dic_2[ef]
        del dic_2[ef]

        if eaten == "Pawn":

            if "Pawn_%s" % ef[0] in list_2:
                list_2.remove("Pawn_%s" % ef[0])

            else:
                for i in range(1, 9):

                    j = "Pawn_%s" % i
                    if j in list_2:
                        list_2.remove(j)
                        break

        elif eaten == "Rook":
            if compar_1:
                list_2.remove("Rook_2")

            elif compar_2:
                list_2.remove("Rook_1")

        elif eaten == "Knight":
            if compar_1:
                list_2.remove("Knight_2")

            elif compar_2:
                list_2.remove("Knight_1")

        elif eaten == "Bishop":
            if compar_1:
                list_2.remove("Bishop_2")

            elif compar_2:
                list_2.remove("Bishop_1")

        elif eaten == "Queen":
            list_2.remove("Queen")

        elif eaten == "King":
            list_2.remove("King")


def thread_starter(to_thread, args=()):
    """Start a new daemon thread."""

    thread = threading.Thread(target=to_thread, args=args)
    thread.setDaemon(True)
    thread.start()

    return thread


def video_exit(k):
    """Different options during video streams."""

    if k == ord('m'):       # Print used memory
        local_memory.print_used_memory()

    elif k == 227:          # Close the program after cleaning tmp files
        cleaner.Clean.images()
        cleaner.Clean.pyc()
        exit(11)

    elif k == ord('t'):     # Print the count of active threads
        print threading.activeCount()


def prevent_auido_error(audio, args):
    """Start a loop if an audio is being said."""
    try:
        audio(args)

    except RuntimeError:
        sleep(0.1)
        prevent_auido_error(audio, args)


def give_values(value, n):
    """Give n times the recieved value."""
    return [value for i in range(n)]
