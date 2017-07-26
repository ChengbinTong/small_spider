#coding=utf-8
import login_12306
import requests
import sys
from bs4 import BeautifulSoup
from LoginInfo import passwd as LogInfo
from pprint import pprint
import re
from prettytable import PrettyTable 
from stations import station
import json
import urllib
import datetime
import ssl
import time
import random
ssl._create_default_https_context = ssl._create_unverified_context



#用户信息
#---------------------------------------------------------------------------------
user_code='421121199302060000'
train_date = "2017-07-14" #车次时间
from_station = "GNN"		#出发站
to_station = "WHN"			#到达站
purpose_codes = "ADULT"		#
train_code="C5502"			#车次
ticket_type="1"  #票类
"""
		'1': u'成人票',
        '2': u'儿童票',
        '3': u'学生票',
        '4': u'残军票'
"""
Card_type='1'  #证件类型
"""
		'1': u'二代身份证',
        '2': u'一代身份证',
        'C': u'港澳通行证',
        'G': u'台湾通行证',
		'B': u'护照'
"""
"""
变量说明 citymap  地图 指定车次中会出现的代码对应地点

"""
#------------------------------------------------------------------------------------
#初始化session
def get_session():
	username=LogInfo("accunt")
	passwd=LogInfo("passwd")
	global session
	session=requests.session()
	cookie=login_12306.main(username,passwd)
	session.cookies = requests.utils.cookiejar_from_dict(cookie)
	headers={"Host":"kyfw.12306.cn",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
		"Accept": "*/*",
		"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate, br",
		"Referer": "https://kyfw.12306.cn/otn/confirmPassenger/initDc",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"X-Requested-With": "XMLHttpRequest",
		"Connection": "keep-alive"
		}
	session.headers=headers
	
	#session.cookies.update(d2)



#获取车次信息
def Inquiry_ticket():
	url="https://kyfw.12306.cn/otn/leftTicket/query"
	playdata={
	"leftTicketDTO.train_date":train_date,
	"leftTicketDTO.from_station":from_station,
	"leftTicketDTO.to_station":to_station,
	"purpose_codes":purpose_codes,
	}
	req=session.get(url,params=playdata,verify=False)
	#可能是请求过于频繁 会出现错误 判断状态码 跳过错误
	while req.status_code != 200:
		print("请稍后!")
		req=requests.get(url,params=playdata,verify=False)
	ticket=req.json()['data']['result']
	global citymap
	citymap=req.json()['data']['map']
	
	#如果每列列侧信息"|"的第一列为空 则没有票
	#把所有信息存入字典  以序号为Key list为val  list包含列车信息  list格式：  是都有票-车次-出发站-到达站-出发时间-到达时间-历时-商务座-一等座-二等座-高级软卧-软卧-动卧-硬卧-软座-硬座-无座-其他
	train_data={}
	for i in ticket:
		if i.split("|")[3] == train_code:
			train_data['secretStr']=i.split("|")[0] #车次字符串
			train_data['train_no']=i.split("|")[2] #车次数字代码
			train_data['stationTrainCode']=i.split("|")[3]      #车次代码
			train_data['fromStationTelecode']=i.split("|")[6]  #起始站
			train_data['toStationTelecode']=i.split("|")[7]    #重点站
			train_data['from_time']=i.split("|")[8]
			train_data['to_time']=i.split("|")[9]
			train_data['all_time']=i.split("|")[10]
			train_data['one_set']=i.split("|")[31]
			train_data['two_set']=i.split("|")[30]
			train_data['no_set']=i.split("|")[26]
			train_data['leftTicket']=i.split("|")[12]  #提交需要用到的参数
			break
	if train_data['secretStr'] =="":
		print(u"无票")
		return False
	else:
		print(train_code+u"有票")
		return train_data


#检查用户状态
def check_user():
	rand = random.uniform(0, 1)
	create_url="https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&{}".format(str(rand))
	#u="https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo"
	#session.post(u,data={"_json_att":""})
	session.get(create_url,verify=False)
	check_url=url5="https://kyfw.12306.cn/otn/login/checkUser"
	check=session.post(check_url,data={"_json_att":""}).json()
	if 'flag' in check['data'] and check['data']['flag']== True :
		print("用户检查完成")
		return True



#提交订单请求
def submitOrder(train_data):
	submiturl="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
	secretStr=urllib.parse.unquote(train_data['secretStr'])
	submitResult={"secretStr":secretStr,
			"train_date":train_date,
			"back_train_date":train_date,
			"tour_flag":"dc",
			"purpose_codes":purpose_codes,
			"query_from_station_name":citymap[train_data['fromStationTelecode']],
			"query_to_station_name":citymap[train_data['toStationTelecode']],
			"undefined":"",}
	
	req=session.post(submiturl,data=submitResult)
	if req.json()['status'] == True and req.json()['messages'] == [] :
		print("submitOrderRequest is OK !")
	else:
		print(req.text)
		exit()


#获取一些参数 token
def get_token():
	initDCUrl="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
	session.get("https://kyfw.12306.cn/otn/login/init")
	initDC=session.post(initDCUrl,data={"_json_att":""})
	global token
	global key_check_isChange
	try:
		token=re.findall(r"[0-9a-z]{32}",initDC.text)[0]
	except:
		print("token is ERROE!")
		return False
	try:
		key_check_isChange=re.findall(r"[0-9A-Z]{56}",initDC.text)[0]
	except:
		print("key_check_isChange is False!")
		print("---------------------------")
		print(initDC.text)
		print("----------------------------")
		exit()
	print("get token is OK!")
	return True


#获取常用联系人 返回需要下单的联系人
def getPassengerDTOs():
	passengerurl="https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
	data={
		"_json_att":"",
		"REPEAT_SUBMIT_TOKEN":token
		}
	req=session.post(passengerurl,data=data).json()
	#print(req)
	user_list=req['data']["normal_passengers"]
	userdata={}
	for i in user_list:
		if i['passenger_id_no'] == user_code:
			user_data = i 
			return user_data


def getpassengerticket():
	#passengerTicketStr:座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
	user_data=getPassengerDTOs()
	global passengerTicketStr
	global oldPassengerStr
	passengerTicketStr="O,0,{0},{1},{2},{3},{4},{5}".format(ticket_type,user_data['passenger_name'],Card_type,user_data['passenger_id_no'],user_data['mobile_no'],"N")
	#乘客名,证件类型,证件号,乘客类型
	oldPassengerStr="{0},{1},{2},1_".format(user_data['passenger_name'],Card_type,user_data['passenger_id_no'])


#提交身份信息
def checkOrderInfo():
	#提交身份信息需要下载验证码 但是不需要输入
	rand = random.uniform(0, 1)
	create_url="https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&{}".format(str(rand))
	checkOrderInfourl="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
	infodata={
		"cancel_flag""2"
		"bed_level_order_num":"000000000000000000000000000000",
		"passengerTicketStr":passengerTicketStr,
		"oldPassengerStr":oldPassengerStr,
		"tour_flag":"dc",
		"randCode":"",
		"_json_att":"",
		"REPEAT_SUBMIT_TOKEN":token,
		}
	print(infodata)
	session.get(create_url)
	req=session.post(checkOrderInfourl,data=infodata)
	if req.json()['status'] == True and req.json()['messages'] == []:
		print("checkOrderInfo is OK ！")
		return True
	else:
		return False
		print("ERROR: checkOrderInfo")

#时间格式转换
def date2UTC(d):
    # Convert '2014-01-01' to 'Wed Jan 01 00:00:00 UTC+0800 2014'
    t = time.strptime(d, '%Y-%m-%d')
    asc = time.asctime(t)  # 'Wed Jan 01 00:00:00 2014'
    # 'Wed Jan 01 00:00:00 UTC+0800 2014'
    #asc[20:31] --y
    return (asc[0:11]+asc[20:30]+asc[10:20]+'GMT+0800 ')
	
#列队提交订单
def getQueuecount(train_data):
	url="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
	date=date2UTC(train_date)
	data={
		"train_date":date,
		"train_no":train_data['train_no'],
		"stationTrainCode":train_data['stationTrainCode'],
		"seatType":"O",
		"fromStationTelecode":train_data['fromStationTelecode'],
		"toStationTelecode":train_data['toStationTelecode'],
		"leftTicket":train_data['leftTicket'],
		"purpose_codes":"00",
		"train_location":"N2",
		"_json_att":"",
		"REPEAT_SUBMIT_TOKEN":token,
		}
	req=session.post(url,data=data)
	if req.json()['messages'] == []:
		print("getQueuecount is OK")
		print("---------------------------------------------")
#确认订单
def ForQueue(train_data):
	url="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
	data={
	"passengerTicketStr":passengerTicketStr,
	"oldPassengerStr":oldPassengerStr,
	"randCode":""	,
	"purpose_codes":"00",
	"key_check_isChange":key_check_isChange,
	"leftTicketStr":train_data['leftTicket'],
	"train_location":"N2",
	"choose_seats":"",
	"seatDetailType":"000",
	"roomType":"00",
	"dwAll":"N",
	"_json_att":""	,
	"REPEAT_SUBMIT_TOKEN":token,
	}
	req=session.post(url,data=data).json()
	if req['status'] == True and req['data']['submitStatus'] ==True:
		print("下单成功！")
		return True
def MyOrder():
	time.sleep(2)
	url="https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete"
	req=session.post(url,data={"_json_att":""},verify=False).json()
	MyOrderInfo={}
	try:
		MyOrderInfo['sequence_no']=req['data']['orderDBList'][0]['tickets'][0]['ticket_no']  #订单号
		MyOrderInfo['train_date']=req['data']['orderDBList'][0]['tickets'][0]['train_date']  #日期
		MyOrderInfo['seat_type_name']=req['data']['orderDBList'][0]['tickets'][0]['seat_type_name']
		MyOrderInfo['ticket_type_name']=req['data']['orderDBList'][0]['tickets'][0]['ticket_type_name']
		MyOrderInfo['lose_time']=req['data']['orderDBList'][0]['tickets'][0]['lose_time']
		MyOrderInfo['str_ticket_price_page']=req['data']['orderDBList'][0]['tickets'][0]['str_ticket_price_page']
		MyOrderInfo['start_train_date_page']=req['data']['orderDBList'][0]['tickets'][0]['start_train_date_page']
		print(MyOrderInfo)
	except:
		print(req.text)
def main():
	get_session()

	train_data=Inquiry_ticket()  #查询列车https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date=2017-07-14&leftTicketDTO.from_station=GNN&leftTicketDTO.to_station=WHN&purpose_codes=ADULT
	check_user()					#https://kyfw.12306.cn/otn/login/checkUser
	submitOrder(train_data)		#https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest
	get_token()					#https://kyfw.12306.cn/otn/confirmPassenger/initDc
	getpassengerticket()		#https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs

	while not train_data:
		#如果无票 循环获取 直到有票
		train_data=Inquiry_ticket()
		time.sleep(3)
	if checkOrderInfo():
		pass
	if getQueuecount(train_data):
		pass
	if ForQueue(train_data) == True:
		MyOrder()
	
main()