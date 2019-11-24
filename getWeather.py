import pandas as pd
from xml.dom.minidom import Document
import requests
import time
from PyQt5.QtCore import *

class weath(QThread):

    city_wea = pyqtSignal(str)
    def __init__(self):
        super(weath, self).__init__()
        self.doc = Document()
        self.d0 = self.doc.createElement('kml')
        self.d1 = self.doc.createElement('Document')
        self.path = '.'

    def icon(self):
        weather = ['晴', '阴', '多云', '小雨', '中雨', '大雨', '暴雨', '大暴雨', '特大暴雨', '阵雨', '雨夹雪', '雷阵雨']
        for wea in weather:
            i1 = self.doc.createElement('Style')
            i1.setAttribute('id', wea)

            # i2 = doc.createElement('BalloonStyle')
            #
            # str1 = "<![CDATA[<table style='color:white'><tr><td><b>类&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;型&emsp;&emsp;</b></td><td>$[类型]</td></tr><tr><td><b>位&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;置&emsp;&emsp;</b></td><td>$[位置]</td></tr><tr><td><b>坐&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;标&emsp;&emsp;</b></td><td>$[坐标]</td></tr><tr><td><b>当前天气&emsp;&emsp;</b></td><td>$[当前天气]</td></tr></table>]]>"
            # i2.appendChild(doc.createElement('text').appendChild(doc.createTextNode(str1)))
            # i2.appendChild(doc.createElement('bnColor').appendChild(doc.createTextNode('#ff673005')))
            # i2.appendChild(doc.createElement('textColor').appendChild(doc.createTextNode('#ffffffff')))
            #
            # i1.appendChild(i2)

            i3 = self.doc.createElement('IconStyle')
            i4 = self.doc.createElement('Icon')
            i5 = self.doc.createElement('href')
            str2 = '天气图标/' + wea + '.png'
            i5.appendChild(self.doc.createTextNode(str2))
            i4.appendChild(i5)
            i3.appendChild(i4)

            i1.appendChild(i3)
            self.d1.appendChild(i1)

    def appendcity(self):
        for i in range(len(self.std)):
            d2 = self.doc.createElement('Placemark')

            name = self.doc.createElement('name')
            name_s = self.std.loc[i].SID
            name.appendChild(self.doc.createTextNode(str(name_s)))
            d2.appendChild(name)

            # 获取天气
            self.wea_now = self.getwea(self.std.loc[i].LON, self.std.loc[i].LAT)
            self.city = self.std.NAME[i]
            # 发送信号
            self.city_wea.emit(self.city+' : '+self.wea_now)

            sty = self.doc.createElement('styleUrl')
            sty.appendChild(self.doc.createTextNode('#' + self.wea_now))
            d2.appendChild(sty)

            point = self.doc.createElement('Point')
            cor = self.doc.createElement('coordinates')
            cor.appendChild(self.doc.createTextNode(str(self.std.loc[i].LON) + ',' + str(self.std.loc[i].LAT)))
            point.appendChild(cor)
            d2.appendChild(point)

            exdata = self.doc.createElement('ExtendedData')
            data = self.doc.createElement('Data')
            val = self.doc.createElement('value')
            val.appendChild(self.doc.createTextNode('观测站'))
            data.appendChild(val)
            data.setAttribute('name', '类型')
            exdata.appendChild(data)

            data = self.doc.createElement('Data')
            val = self.doc.createElement('value')
            val.appendChild(self.doc.createTextNode(self.std.loc[i].NAME + '，' + self.std.loc[i].PROVINCE))
            data.appendChild(val)
            data.setAttribute('name', '位置')
            exdata.appendChild(data)

            data = self.doc.createElement('Data')
            val = self.doc.createElement('value')
            val.appendChild(self.doc.createTextNode(str(self.std.loc[i].LAT) + ' N,' + str(self.std.loc[i].LON) + ' E'))
            data.appendChild(val)
            data.setAttribute('name', '坐标')
            exdata.appendChild(data)

            data = self.doc.createElement('Data')
            val = self.doc.createElement('value')
            val.appendChild(self.doc.createTextNode(self.wea_now))
            data.appendChild(val)
            data.setAttribute('name', '当前天气')
            exdata.appendChild(data)

            d2.appendChild(exdata)
            self.d1.appendChild(d2)
            self.d0.appendChild(self.d1)

            time.sleep(0.2)

    def getwea(self,lon,lat):
        url = 'https://free-api.heweather.net/s6/weather/now?location=' + str(lon) + ',' + str(
            lat) + '&key=63d9ae66c2844258895e1432ac452ef4'
        response = requests.get(url)
        return response.json()['HeWeather6'][0]['now']['cond_txt']

    def loadfile(self,filepath1):
        self.std = pd.read_csv(filepath1, sep='\s+', encoding='gbk')[:20]

    def tofile(self,filepath2):
        self.icon()
        self.appendcity()
        self.doc.appendChild(self.d0)
        with open(filepath2, 'wb') as f:
            f.write(self.doc.toprettyxml(indent='\t', encoding='utf-8'))

    def run(self):
        self.loadfile('/Users/fhan/Desktop/china_gaokong.dat')
        self.tofile(self.path+'/0.xml')

if __name__ == '__main__':
    w = weath()
    w.run()

