#!/usr/bin/python

import os
from serial import Serial
from time import sleep


class Arduino:
    def __init__(self, time):
        try:
            if os.name == 'posix':      # Linux or mac
                ports = ['/dev/ttyACM0', '/dev/rfcomm0']      # Wired and Bluetooth connection respectively

            elif os.name == 'nt':       # Windows
                ports = ['COM0', 'COM1']

            else:
                raise OSError

            for port in ports:
                if os.path.exists(port):
                    # os.chmod(port, 777)
                    self.arduino = Serial(port, 9600)
                    break

            sleep(time)
            self.write('s', 0)

        except:
            raise OSError

    def write(self, write, time):
        self.arduino.write(write)
        sleep(time)


if __name__ == '__main__':
    arduino = Arduino(1)
