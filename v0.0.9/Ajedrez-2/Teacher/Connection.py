import os
import serial
from time import sleep


class Arduino:

    def __init__(self, time):
        # chmod('/dev/ttyACM0', 777)
        if os.path.exists('/dev/ttyACM0'):
            self.arduino = serial.Serial('/dev/ttyACM0', 9600)
            self.write('s', time)
        else:
            raise OSError


    def write(self, write, time):
        self.arduino.write(write)
        sleep(time)
