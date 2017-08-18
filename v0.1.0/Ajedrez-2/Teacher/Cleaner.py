from os import remove
from glob import glob


class Clean:
    def __init__(self):
        self.images()

    @staticmethod
    def images():
        """Delete all temporal images"""
        images = glob('PythonCache/*.jpg')
        for image in images:
            remove(image)

    @staticmethod
    def pyc():
        """Delete all binary python files"""
        pyc_files = glob('*.pyc') + glob('Instructions/*.pyc')
        for pyc in pyc_files:
            remove(pyc)

if __name__ == '__main__':
    Clean.images()
    Clean.pyc()
