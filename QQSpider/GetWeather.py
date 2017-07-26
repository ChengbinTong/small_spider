#!/usr/bin/python
#--*--encoding=utf-8-*-
import requests
import time
import re
import json
def weather_today(citycode):
	headers={
		"Accept":"*/*",
		"Accept-Encoding":"gzip, deflate, sdch",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Host":"d1.weather.com.cn",
		"Referer":"http://www.weather.com.cn/weather1d/101200510.shtml",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
		}
	t=time.time()*1000
	url="http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(citycode,int(t))
	r=requests.get(url,headers=headers)
	r.encoding='utf-8'
	json_data=json.loads(re.findall(r"=(.+);",r.text)[0])
	weather_data={}
	
	weather_data={"cityname":json_data["weatherinfo"]['cityname'],
						"tempPM":json_data["weatherinfo"]['temp'],
						"tempAM":json_data["weatherinfo"]['tempn'],
						"weather":json_data["weatherinfo"]['weather'],
						"wd":json_data["weatherinfo"]['wd'],
						"ws":json_data["weatherinfo"]['ws']}
				
	return weather_data


citycode="101200510"
weather_today(citycode)