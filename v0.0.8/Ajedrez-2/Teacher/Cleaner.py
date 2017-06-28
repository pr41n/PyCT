import os
import glob


class Clean:
	def __init__(self):
		pass

	def pyc(self):
		pyc = glob.glob('*.pyc')
		for i in self.pyc:
			os.remove(i)

	def images(self):
		os.remove('PythonCache/Image.jpg')

