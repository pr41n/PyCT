from os import remove
from glob import glob


class Clean:
    def __init__(self):
        self.images()

    @staticmethod
    def images():
        images = glob('PythonCache/*.jpg')
        for image in images:
            remove(image)

    @staticmethod
    def pyc():
        pyc_files = glob('*.pyc') + glob('Instrucciones/*.pyc')
        for pyc in pyc_files:
            remove(pyc)

if __name__ == '__main__':
    Clean.images()
    Clean.pyc()
