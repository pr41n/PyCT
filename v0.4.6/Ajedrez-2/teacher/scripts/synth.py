#!/usr/bin/python

import pyttsx


class Sts:
    def __init__(self, language):
        self._unlocked = True

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 143)
        self.engine.setProperty('voice', language)

    def say(self, text):
        """This is the only way I found to make engine.say works"""
        while True:
            if self._unlocked:
                self.engine.say(text)
                self.engine.say(' ')

                self._unlocked = False
                self.engine.runAndWait()
                self.engine.runAndWait()
                self._unlocked = True

                return


if __name__ == '__main__':
    import threading
    from time import sleep
    sts = Sts('english')


    def thread_say(string):
        thread = threading.Thread(target=sts.say, args=[string])
        thread.start()
        return thread

    thread_say('Have you tried turning it off and on again?')
    sleep(0.5)
    thread_say("I'd rather throw away the computer")
