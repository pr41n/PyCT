from os import chmod
from serial import Serial
from time import sleep


class Arduino:
    chmod('/dev/ttyACM0', 777)
    arduino = Serial('/dev/ttyACM0', 9600)

    def inicio(self, time):
        self.Write('s', time)

    def write(self, write, time):
        self.arduino.write(write)
        sleep(time)
