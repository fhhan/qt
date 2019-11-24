from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from getWeather import weath
import sys

class weather_Dlg(QWidget):
    def __init__(self):
        super(weather_Dlg, self).__init__()
        self.initUI()

    def initUI(self):

        #self.resize(400,200)
        #禁止窗口大小被改变
        #self.setFixedSize(self.width(), self.height())
        #禁止窗口最大化
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        layout = QVBoxLayout()

        self.edit1 = QLineEdit()
        self.edit1.setMinimumWidth(300)
        self.btn1 = QPushButton('...')

        self.btn1.setMaximumWidth(120)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.edit1)
        layout1.addWidget(self.btn1)

        self.groupbox = QGroupBox('浏览文件夹')
        self.groupbox.setFont(QFont("Myriad Pro", 13))
        self.groupbox.setLayout(layout1)

        layout2 = QVBoxLayout()
        self.edit2 = QTextEdit()
        self.edit2.verticalScrollBar().hide()

        #文本浏览框不可编辑
        #self.edit2 = QTextBrowser()

        layout2.addWidget(self.edit2)
        self.groupbox1 = QGroupBox('生成文件')
        self.groupbox1.setFont(QFont("Myriad Pro", 13))
        self.groupbox1.setLayout(layout2)

        layout.addWidget(self.groupbox)
        layout.addWidget(self.groupbox1)

        self.btn2 = QPushButton('生成')
        self.btn2.clicked.connect(self.savefile)
        layout.addWidget(self.btn2)

        self.setLayout(layout)

        self.btn1.clicked.connect(self.loadpath)


        #self.edit2.setEnabled(False)

    def loadpath(self):
        self.dic = QFileDialog.getExistingDirectory(self,'选择文件夹','./')
        self.edit1.setText(self.dic)
        #print(self.edit1.text())

    def savefile(self):
        self.btn2.setEnabled(False)
        self.w = weath()
        self.w.city_wea.connect(self.showinfo)
        self.w.loadfile('/Users/fhan/Desktop/china_gaokong.dat')
        self.w.path = self.dic
        self.w.start()

    def showinfo(self,s):
        self.edit2.moveCursor(QTextCursor.End)
        self.edit2.append(s)

        #print(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wea_dlg = weather_Dlg()
    wea_dlg.show()
    sys.exit(app.exec_())
