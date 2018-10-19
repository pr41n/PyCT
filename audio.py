#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import os

from scripts import synth

"""
Convert all audio functions in threads with a class
"""

languages = []

if os.name == 'posix':
    testing = __file__ == '../audio.py' or __file__ == '../audio.pyc'
    importable = glob('languages/[A-Z]*.py' if not testing else '../languages/[A-Z]*.py')

    for love in importable:
        magic = love.split("/")[1 if not testing else 2].split(".")[0]
        exec "from languages import {}".format(magic)
        languages.append(eval(magic))

elif os.name == 'nt':
    importable = [a for a in os.listdir('languages') if a.endswith('.py')]
    importable.remove('add.py')
    importable.remove('__init__.py')

    for love in importable:
        magic = love.split(".")[0]
        exec "from languages import {}".format(magic)
        languages.append(eval(magic))

language = [i for i in languages if i.babel == 'spanish'][0]
sts = synth.Sts(language.babel)


def refresh_sts():
    global language, sts
    try:
        sts = synth.Sts(language.sound)

    except AttributeError:
        sts = synth.Sts(language.babel)


class Language:
    def __init__(self):
        global language
        self.say = sts.say

    def intro(self):
        self.say(language.aud_001)
        # self.say(language.aud_002)
        return

    def calibration(self, moment):
        if moment == 1:
            self.say(language.aud_003)
            self.say(language.aud_004)
            self.say(language.aud_005)
            self.say(language.aud_006)
        elif moment == 2:
            self.say(language.aud_007)
            self.say(language.aud_008)

    def detection(self):
        self.say(language.aud_018)
        return

    def arduino(self, signal):
        if signal:
            self.say(language.aud_009)
        else:
            self.say(language.aud_010)
        return

    def match(self):
        self.say(language.aud_011)
        self.say(language.aud_012)
        self.say(language.aud_013)

    def play(self, piece, position, eaten):
        if eaten:
            self.say(language.aud_014 % (piece, position))
        else:
            self.say(language.aud_015 % (piece, position))
        return

    def error_1(self):
        self.say(language.aud_019)
        self.say(language.aud_020)
        return

    def error_2(self):
        self.say(language.aud_021)
        return

    def check_mate(self, player, turn):
        self.say(language.aud_022 % (player, turn - 1))
        return

    def promotion(self, piece):
        self.say(language.aud_023 % piece)
        return

    def castling(self, side):
        if side.lower() == 'kingside':
            self.say(language.aud_024)

        elif side.lower() == 'queenside':
            self.say(language.aud_025)
        return

    def repeat_move(self, first_time):
        self.say(language.aud_026)
        if first_time:
            self.say(language.aud_027)
        return
