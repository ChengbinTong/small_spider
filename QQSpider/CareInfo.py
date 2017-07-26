#-*-coding:utf-8-*-
import gzip
import re
import os
import requests
import QQZone
import json
import GetWeather
#初始化信息
username="58296672"
password=""
session=QQZone.main(username,password)
cookie=QQZone.get_rawCookie(username)
dict_cookie=QQZone.dict_cookie(cookie)

gtk=QQZone.get_gtk(username)
session.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"})

def get_index():
	headers={
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	#"Accept-Encoding":"gzip, deflate, sdch, br",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Avail-Dictionary":"XprLfaXG",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"Cookie":"pgv_si={};ptcz={}; pt2gguin={}; uin={}; skey={}; p_uin={}; p_skey={}; pt4_token={};".format(dict_cookie["pgv_si"],dict_cookie["ptcz"],dict_cookie["pt2gguin"],dict_cookie["uin"],dict_cookie["skey"],dict_cookie["p_uin"],dict_cookie["p_skey"],dict_cookie["pt4_token"],),
	"Host":"user.qzone.qq.com",
	"If-Modified-Since":"Sun, 25 Jun 2017 01:34:44 GMT",
	"Referer":"https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
	}
	r=session.get("https://user.qzone.qq.com/58296672",headers=headers)
	#r.encoding="utf-8"
	#result = gzip.decompress(r.content)
	qztoken=re.findall(r'try\{return(.+?)\}',r.text)
	#print(qztoken)
	return qztoken[0][2:-2]
get_index()
#获取我的信息
def get_Myinfo(username):
	gtk=QQZone.get_gtk(username)
	info_url="https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin=%s&vuin=%s&fupdate=1&g_tk=%s"%(username,username,gtk)
	resp=session.get(info_url)
	data_text=resp.text.replace("_Callback","")[1:-2]
	data=json.loads(data_text)['data']
	return data

	
#获取关心我的排行
def get_Care_Me(username):
	gtk=QQZone.get_gtk(username)
	url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk=#gtk#'
	url=url.replace('#qqNo#',username).replace('#gtk#',str(gtk))
	r=session.get(url)
	data_careme=json.loads(r.text[10:-2])
	CareMeList=data_careme["data"]["items_list"]
	f=open("CareMeList_for_%s.txt"%(username),"w",encoding="utf-8")
	for i in CareMeList:
		f.write(str(i)+"\n")
#获取我关心的排行
def get_Care_her(username):
	gtk=QQZone.get_gtk(username)
	url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk=#gtk#'
	url=url.replace('#qqNo#',username).replace('#gtk#',str(gtk))
	r=session.get(url)
	data_careme=json.loads(r.text[10:-2])
	CareHerList=data_careme["data"]["items_list"]
	f=open("CareHerList_for_%s.txt"%(username),"w",encoding="utf-8")
	for i in CareHerList:
		f.write(str(i)+"\n")
#获取所有留言
def get_message():
	qztoken=get_index()
	#start指定第一个留言的序号 每次获取十条
	message_url="https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin={}&hostUin={}&start=0&s=0.7790470899601283&format=jsonp&num=10&inCharset=utf-8&outCharset=utf-8&g_tk={}&qzonetoken={}".format(username,QQtarget,gtk,qztoken)
	r=session.get(message_url)
	html=json.loads(r.text.replace("_Callback","")[1:-3])
	prime_message=html["data"]["authorInfo"]['msg']  	#签名档
	message_num=html['data']['total']					#留言总数
	liuyan=html["data"]["commentList"]
	for i in liuyan:
		print(i["htmlContent"])
#自动留言
def postnew(message,QQtarget):
	gtk=QQZone.get_gtk(username)
	qztoken=get_index()
	posturl="https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/add_msgb?g_tk={}&qzonetoken={}".format(gtk,qztoken)
	headers={
	"Host":"h5.qzone.qq.com",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate, br",
	"Content-Type": "application/x-www-form-urlencoded",
	"Content-Length": "210",
	"Cookie":"pgv_si={};ptcz={}; pt2gguin={}; uin={}; skey={}; p_uin={}; p_skey={}; pt4_token={};".format(dict_cookie["pgv_si"],dict_cookie["ptcz"],dict_cookie["pt2gguin"],dict_cookie["uin"],dict_cookie["skey"],dict_cookie["p_uin"],dict_cookie["p_skey"],dict_cookie["pt4_token"],),
	"Connection": "keep-alive",
	"Upgrade-Insecure-Requests":"1"
	}

	post_data={
	"content":message,
	"hostUin":QQtarget,
	"uin":username,
	"format":"fs",
	"inCharset":"utf-8",
	"outCharset":"utf-8",
	"iNotice":"1",
	"ref":"qzone",
	"json":"1",
	"g_tk":gtk,
	"qzreferrer":"https://qzs.qq.com/qzone/msgboard/msgbcanvas.html#page=1",
	}
	req=session.post(posturl,data=post_data,headers=headers)
	status_message=re.findall(r"message\":\"(.+?)\",",req.text)
	#print(req.text)
	return status_message[0]
if __name__ == '__main__':
	QQtarget="995857140"
	citycode="101200205"
	message_dict=GetWeather.weather_today(citycode)
	message=str(message_dict).replace(", ","\r\n").replace("{","").replace("}","").replace("'","")
	status=postnew(message,QQtarget)
	print(status)
	#get_message()
