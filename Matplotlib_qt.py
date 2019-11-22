import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolBar)
import matplotlib as mpl
from matplotlib.figure import Figure
import numpy as np

class Plottest(QMainWindow):
	def __init__(self):
		super(Plottest,self).__init__()
		self.setWindowTitle('GUI with Matplotlib')

		self.__figure()
		self.__plot()

	def __figure(self):
		self.__fig = Figure(figsize=(8,5))
		self.__fig.suptitle('Demo')

		figcanvas = FigureCanvas(self.__fig)

		toolbar = NavigationToolBar(figcanvas, self)
		toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.addToolBar(toolbar)

		self.setCentralWidget(figcanvas)

	def __plot(self):
		self.__ax = self.__fig.add_subplot(1,1,1)

		x = np.linspace(-2*np.pi,2*np.pi,100)
		y = np.sin(x)

		self.__ax.plot(x,y,'b:',label="Sin",linewidth=2)
		self.__ax.legend()
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = Plottest()
	demo.show()
	sys.exit(app.exec_())
