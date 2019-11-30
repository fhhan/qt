import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolBar)
import matplotlib as mpl
from matplotlib.figure import Figure
import numpy as np

class MplCanvas(FigureCanvas):
	def __init__(self,width=8, height=5, dpi=100):
		
		self.fig = Figure(figsize=(width,height), dpi=dpi)
		super(MplCanvas,self).__init__(self.fig)
		
		self.ax = self.fig.add_subplot(1,1,1)
		#FigureCanvas.__init__(self, fig)  应该与super(MplCanvas,self).__init__(self.fig)一样，老式写法


class MyPlot(QWidget):
	def __init__(self):
		super(MyPlot,self).__init__()
		self.setWindowTitle('GUI with Matplotlib')

		vbox = QVBoxLayout()
		self.canvas = MplCanvas(width=5, height=4, dpi=100)
		

		self.btn = QPushButton('plot')
		hbox = QHBoxLayout()
		hbox.addWidget(self.btn)
		
		vbox.addWidget(self.canvas)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		self.btn.clicked.connect(self.__plot)

		self.flag = True


	def __plot(self):
		#clear 画布，刷新画布
		self.canvas.ax.clear()
		x = np.linspace(-2*np.pi,2*np.pi,100)

		if self.flag:
			self.canvas.ax.plot(x,np.sin(x),'b:',label="Sin",linewidth=2)
		else:
			self.canvas.ax.plot(x,np.cos(x),'r:',label="Cos",linewidth=2)

		self.canvas.ax.legend(loc=3)
		#canvas.draw() 与 canvas.draw_idle()
		#在 win 上canvas.draw可以，但 mac 上无反应，需要切换窗口或者最大化窗口才刷新
		#self.canvas.draw()
		self.canvas.draw_idle()
		self.flag = not self.flag

if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = MyPlot()
	demo.show()
	sys.exit(app.exec_())
