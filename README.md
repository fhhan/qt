# PyQt5 小试  

## 图书馆查询
### [图书查询](https://github.com/fhhan/qt/blob/master/QBook.py)  

#### 界面显示  

![图片](https://github.com/fhhan/qt/blob/master/fig/WindowView.png)  

#### 控件之间的逻辑关系  

#### 数据库查询  

> 参考借鉴于 [LibraryManageDesktopApp](https://github.com/ycdxsb/LibraryManageDesktopApp)

## Matplotlib and PyQt5
### [自定义 MplFigure 类](https://github.com/fhhan/qt/blob/master/Matplotlib_MplCanvas.py)  

#### 界面显示  

![图片2](https://github.com/fhhan/qt/blob/master/fig/Canvas1.png)

### [无自定义 MplFigure 类](https://github.com/fhhan/qt/blob/master/Matplotlib_qt.py)  

#### 界面显示  

![图片](https://github.com/fhhan/qt/blob/master/fig/Canvas3.png)

> 参考借鉴于 Code:
>[绘制](matplotlib_with_pyqt.py) &nbsp;|&nbsp; [实时添加、绘制数据](Animation_matplotlib_1.py) &nbsp;|&nbsp; [动画](Animation_matplotlib_2.py)

## 天气查询
### [查询天气并保存为 xml 文件](setWeather.py)  

#### 界面显示  

![图片](fig/weather.jpg)  

#### 控件之间的逻辑关系  

- [getWeather.py](getWeather.py)中weath类为QThread子类  

- 文本编辑框QTextEdit（可编辑）和文本浏览框QTextBrowser（不可编辑）
