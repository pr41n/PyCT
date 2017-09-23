import pyttsx


class Sts:
    def __init__(self, language):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 143)
        self.engine.setProperty('voice', language)

    def say(self, text):
        """This is the only way I found to make engine.say works"""
        self.engine.say(text)
        self.engine.say(' ')
        self.engine.runAndWait()
        self.engine.runAndWait()


if __name__ == '__main__':
    sts = Sts('english')
    sts.say('Have you tried turning it off and on again?')
