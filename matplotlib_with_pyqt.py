import sys
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import(FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt
class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)#调用父类构造函数
        self.setWindowTitle("Demo14_1, GUI中的matplotlib绘图")
        ## rcParams[]参数设置，以正确显示汉字
        mpl.rcParams['font.sans-serif']=['KaiTi','SimHei']#汉字字体
        mpl.rcParams['font.size']=12#字体大小
        mpl.rcParams['axes.unicode_minus']=False#正常显示负号
        self.__iniFigure()#创建绘图系统，初始化窗口
        self.__drawFigure()#绘图
    ##==========自定义函数=================
    def __iniFigure(self):##创建绘图系统，初始化窗口
        self.__fig=mpl.figure.Figure(figsize=(8,5))#单位英寸
        self.__fig.suptitle("plot in GUI application")#总的图标题
        figCanvas =FigureCanvas(self.__fig)#创建FigureCanvas对象
        naviToolbar=NavigationToolbar(figCanvas,self)#创建工具栏
        naviToolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(naviToolbar)#添加工具栏到主窗口
        self.setCentralWidget(figCanvas)
    def __drawFigure(self):##绘图
        t = np.linspace(0,10,40)
        y1=np.sin(t)
        y2=np.cos(2*t)
        ax1=self.__fig.add_subplot(1,2,1)#matplotlib.axes.Axes 类
        ax1.plot(t,y1,'r-o',label="sin", linewidth=1, markersize=5)
        ax1.plot(t,y2,'b:',label="cos",linewidth=2)
        ax1.set_xlabel('X 轴')#x轴标题
        ax1.set_ylabel('Y 轴',fontsize=14)#y轴标题
        ax1.set_xlim([0,10])
        ax1.set_ylim([-1.5,1.5])
        ax1.set_title("曲线")#子图标题
        ax1.legend()#自动创建图例
        ax2=self.__fig.add_subplot(1,2,2)#matplotlib.axes.Axes 类
        week=["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]
        sales=np.random.randint(200,400,7)
        ax2.bar(week,sales)#绘制柱状图
        ax2.set_xlabel('week days')#x轴标题
        ax2.set_ylabel('参观人数')#y轴标题
        ax2.set_title("柱状图")#子图标题
## ============窗体测试程序 ================================
if __name__ =="__main__":
    app =QApplication(sys.argv)
    form=QmyMainWindow()
    form.show()
    sys.exit(app.exec_())
