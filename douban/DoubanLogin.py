#-*- encoding :utf-8 -*-
#豆瓣模拟登陆
import requests
import http.cookiejar as cookielib
import re
from bs4 import BeautifulSoup
import time
from PIL import Image
import json
# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
     "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}
# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


#获取form data 中的动态xsrf属性  输入页面内容 返回xsrf值
def get_data_xsrf():
	page=session.get('http://www.zhihu.com',headers=headers)
	page_xsrf=page.text
	soup =BeautifulSoup(page_xsrf,'html.parser')
	data_xsrf = soup.select('input[name="_xsrf"]')[0]["value"]
	return data_xsrf

#获取英文验证码
def get_captcha():
	captch_url = 'https://www.zhihu.com/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'
	captch_content= session.get(captch_url,headers=headers)
	with open("captch.jpg",'wb+') as f :
		f.write(captch_content.content)
		f.close
	im = Image.open("captch.jpg")
	im.show()
	captch=input("Please input captch:")
	return captch

#判断用户是否已经登陆
def islogin():
	islogin = session.get('https://www.zhihu.com/settings/profile',headers=headers)
	if islogin.status_code == 200:
		return True
	else:
		return False


#模拟登陆
def login(account,password):
	_xsrf = get_data_xsrf()
	headers["X-Xsrftoken"] = _xsrf
	headers["X-Requested-With"] = "XMLHttpRequest"

	post_url ='https://www.zhihu.com/login/email'
	postdata={
		'_xsrf': _xsrf,
        'password': password,
        'email': account
        }
	#不需要输入验证码能否登陆
	
	login_page = session.post(post_url,data=postdata,headers=headers)
	#pagt=session.get('https://www.zhihu.com/settings/profile')
	login_code = login_page.json()
	if login_code['r'] == 1:
		#不输入验证码登陆失败
		#以下为输入验证码的方式登陆
		postdata["captcha"] =get_captcha()
		login_page = session.post(post_url,data=postdata,headers=headers)
		login_code = login_page.json()
		print(login_code['msg'])
	session.cookies.save()

if __name__ == '__main__':
	if islogin():
		print("你已登录")
	else:
		"""
		account='58296672@qq.com'
		password='想看我密码？'
		"""
		account = input("Please input your email:")
		password = input("Please input your passwd:")
		login(account,password)
	session.put('https://www.zhihu.com/api/v4/me?include=headline%2Ccover_url',headers=headers,cookies=session.cookies,json={'headline':'python'})
	