import os
import serial
from time import sleep


class Arduino:
    def __init__(self, time):
        # chmod('/dev/ttyACM0', 777)
        try:
            if os.path.exists('/dev/ttyACM0'):      # Wired connection
                self.arduino = serial.Serial('/dev/ttyACM0', 9600)
                
            elif os.path.exists('/dev/rfcomm0'):        # Bluetooth connection
                self.arduino = serial.Serial('/dev/rfcomm0', 9600)
                
            sleep(time)
            self.write('s', 0)
            
        except:
            raise OSError

    def write(self, write, time):
        self.arduino.write(write)
        sleep(time)
