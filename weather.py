import pandas as pd
from xml.dom.minidom import Document
import requests
import time

std = pd.read_csv('/Users/fhan/Desktop/china_gaokong.dat',sep='\s+',encoding='gbk')[:134]

weather = ['晴',  '阴','多云', '小雨', '中雨', '大雨', '暴雨', '大暴雨','特大暴雨', '阵雨', '雨夹雪', '雷阵雨']
#style = ['#1', '#2', '#3', '#4','#5','#6','#7', '#8', '#9', '#10','#11','#12']

def icon(weather,doc,d1):
    for wea in weather:
        i1 = doc.createElement('Style')
        i1.setAttribute('id', wea)

        # i2 = doc.createElement('BalloonStyle')
        #
        # str1 = "<![CDATA[<table style='color:white'><tr><td><b>类&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;型&emsp;&emsp;</b></td><td>$[类型]</td></tr><tr><td><b>位&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;置&emsp;&emsp;</b></td><td>$[位置]</td></tr><tr><td><b>坐&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;标&emsp;&emsp;</b></td><td>$[坐标]</td></tr><tr><td><b>当前天气&emsp;&emsp;</b></td><td>$[当前天气]</td></tr></table>]]>"
        # i2.appendChild(doc.createElement('text').appendChild(doc.createTextNode(str1)))
        # i2.appendChild(doc.createElement('bnColor').appendChild(doc.createTextNode('#ff673005')))
        # i2.appendChild(doc.createElement('textColor').appendChild(doc.createTextNode('#ffffffff')))
        #
        # i1.appendChild(i2)

        i3 = doc.createElement('IconStyle')
        i4 = doc.createElement('Icon')
        i5 = doc.createElement('href')
        str2 = '天气图标/' + wea + '.png'
        i5.appendChild(doc.createTextNode(str2))
        i4.appendChild(i5)
        i3.appendChild(i4)

        i1.appendChild(i3)
        d1.appendChild(i1)

def appendcity(std,doc,d0,d1):
    for i in range(len(std)):
        d2 = doc.createElement('Placemark')

        name = doc.createElement('name')
        name_s = std.loc[i].SID
        name.appendChild(doc.createTextNode(str(name_s)))
        d2.appendChild(name)

        #获取天气
        wea_now = getwea(std.loc[i].LON, std.loc[i].LAT)
        print(std.NAME[i],' : ',wea_now)
        sty = doc.createElement('styleUrl')
        sty.appendChild(doc.createTextNode('#'+wea_now))
        d2.appendChild(sty)

        point = doc.createElement('Point')
        cor = doc.createElement('coordinates')
        cor.appendChild(doc.createTextNode(str(std.loc[i].LON) + ',' + str(std.loc[i].LAT)))
        point.appendChild(cor)
        d2.appendChild(point)

        exdata = doc.createElement('ExtendedData')
        data = doc.createElement('Data')
        val = doc.createElement('value')
        val.appendChild(doc.createTextNode('观测站'))
        data.appendChild(val)
        data.setAttribute('name', '类型')
        exdata.appendChild(data)

        data = doc.createElement('Data')
        val = doc.createElement('value')
        val.appendChild(doc.createTextNode(std.loc[i].NAME + '，' + std.loc[i].PROVINCE))
        data.appendChild(val)
        data.setAttribute('name', '位置')
        exdata.appendChild(data)

        data = doc.createElement('Data')
        val = doc.createElement('value')
        val.appendChild(doc.createTextNode(str(std.loc[i].LAT) + ' N,' + str(std.loc[i].LON) + ' E'))
        data.appendChild(val)
        data.setAttribute('name', '坐标')
        exdata.appendChild(data)

        data = doc.createElement('Data')
        val = doc.createElement('value')
        val.appendChild(doc.createTextNode(wea_now))
        data.appendChild(val)
        data.setAttribute('name', '当前天气')
        exdata.appendChild(data)

        d2.appendChild(exdata)
        d1.appendChild(d2)
        d0.appendChild(d1)

        time.sleep(1)

def getwea(lon,lat):
    url = 'https://free-api.heweather.net/s6/weather/now?location='+str(lon)+','+str(lat)+'&key=63d9ae66c2844258895e1432ac452ef4'
    response = requests.get(url)
    return response.json()['HeWeather6'][0]['now']['cond_txt']

def std_wea():
    std = pd.read_csv('/Users/fhan/Desktop/china_gaokong.dat',sep='\s+',encoding='gbk')[:134]

    weather = ['晴',  '阴','多云', '小雨', '中雨', '大雨', '暴雨', '大暴雨','特大暴雨', '阵雨', '雨夹雪', '雷阵雨']

    doc = Document()
    d0 = doc.createElement('kml')
    d1 = doc.createElement('Document')
    icon(weather,doc,d1)
    #d0.appendChild(d1)
    appendcity(std,doc,d0,d1)
    doc.appendChild(d0)

# with open('多天气0.xml', 'wb') as f:
#     f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
