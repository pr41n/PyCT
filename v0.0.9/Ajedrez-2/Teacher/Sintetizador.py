import pyttsx


class Sts:
    def __init__(self, language):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 143)
        self.engine.setProperty('voice', language)

    def say(self, texto):
        self.engine.say(texto)
        self.engine.say(' ')
        self.engine.runAndWait()
        self.engine.runAndWait()
