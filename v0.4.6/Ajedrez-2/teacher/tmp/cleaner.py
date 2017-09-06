from os import remove
from glob import glob


class Clean:
    def __init__(self):
        self.images()

    @staticmethod
    def images():
        """Delete all temporal images"""
        images = glob('*.jpg') if __name__ == '__main__' else glob('tmp/*.jpg')

        for image in images:
            remove(image)

    @staticmethod
    def pyc():
        """Delete all binary python files"""
        if __name__ == '__main__':
            pyc_files = glob('*.pyc') + glob('../languages/*.pyc') + glob('../*.pyc') + glob('../scripts/*.pyc')
        else:
            pyc_files = glob('*.pyc') + glob('languages/*.pyc') + glob('tmp/*.pyc') + glob('scripts/*.pyc')

        for pyc in pyc_files:
            remove(pyc)

if __name__ == '__main__':
    Clean.images()
    Clean.pyc()
