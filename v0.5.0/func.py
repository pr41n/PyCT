#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import cv2
from time import sleep

from scripts import memory
from tmp import cleaner

local_memory = memory.Memory()


def thread_starter(to_thread, args=()):
    """Start a new daemon thread."""

    thread = threading.Thread(target=to_thread, args=args)
    thread.setDaemon(True)
    thread.start()

    return thread


def opencv_win(name, x, y, width, height):
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name, x, y)
        cv2.resizeWindow(name, width, height)


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
