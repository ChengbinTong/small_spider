#coding:utf-8
# selenium+PhantomJS+lxml 登录qq空间 获取cookie信息
from selenium import webdriver
import time
from lxml import etree
import requests
import os
import re
import json
from PIL import Image
#全局session
session=requests.session()

def login(username,password):
	# 打开浏览器
	driver=webdriver.Firefox()
	login_url="https://qzone.qq.com"
	driver.get(login_url)
	driver.switch_to_frame('login_frame')
	# 定位输入框 输入qq号和密码
	driver.find_element_by_id('switcher_plogin').click()
	driver.find_element_by_id('u').send_keys(username)
	# time.sleep(1)
	driver.find_element_by_id('p').clear()
	driver.find_element_by_id('p').send_keys(password)
	# 点击button 登录 （暂未考虑验证码）
	driver.find_element_by_id('login_button').click()
	time.sleep(1)
	
	try:
		driver.find_element_by_id('login_button').click()
		#切换ifram
		driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
		time.sleep(1)
		driver.save_screenshot('screenshot.png')
		code=input("Please input Security code:")
		driver.find_element_by_id('capAns').send_keys(code)
		driver.find_element_by_id('submit').click()
		print("等待跳转！")
		time.sleep(3)  # 等待浏览器跳转
	except:
		time.sleep(2)
		print("正在加载！")
	driver.switch_to_default_content()
	title=driver.title
	if "QQ空间" in title:
		#driver.quit()
		return False
	else:
		qqnum=re.findall(r"\/\/(.+?)\.qzone",title)
		print(qqnum[0]+"登陆成功")
		#获取cookie
		items=[item['name']+'='+item['value'] for item in driver.get_cookies()]
		cookie=';'.join(items)
		# 退出浏览器
		#driver.quit()
		#写入cookie到文件
		with open("cookie/%s_cookie"%(username),"w") as f:
			f.write(cookie)
		return True
		
#获取原始cookies  定位到cookies目录下
def get_rawCookie(username):
	filename="cookie/%s_cookie"%(username)
	cookie=''
	with open(filename,'r') as f:
		for line in f:
			cookie+=line.strip()
	return cookie
#获取字典类型cookie
def dict_cookie(cookie):
	dict_cookie={}
	list_cookie=cookie.split(";")
	for k in list_cookie:
		dict_cookie[k.split("=")[0]]=k.split("=")[1]
	return dict_cookie


def get_skey(cookie):
	item=re.findall(r'p_skey=(.*?);',cookie)
	if len(item)>0:
		return item[0]
	return None 	
# 计算gtk
def get_gtk(username):
	cookie=get_rawCookie(username)
	skey=get_skey(cookie)
	thash=5381
	for c in skey:
		thash+=(thash<<5)+ord(c)
	return thash&2147483647



def get_qqNo(cookie):
	item=re.findall(r'p_uin=(.*?);',cookie)
	if len(item)>0:
		return item[0][1:] if 'o' in item[0] else item[0]
	return None


def check_cookie(username):
	#传入username 判断cookies是否可用 如果不可用  返回flase
	cookie=get_rawCookie(username)
	gtk=get_gtk(username)
	info_url="https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin=%s&vuin=%s&fupdate=1&g_tk=%s"%(username,username,gtk)
	session.headers.update({"cookie":cookie})
	resp=session.get(info_url)
	data_text=resp.text.replace("_Callback","")[1:-2]
	data=json.loads(data_text)
	login_status=data["message"]
	if "获取成功" in login_status:
		qqnum=data["data"]["uin"]
		return True
	else:
		print("False")
		return False

def main(username,password):
	"""
	输入账户密码 判断账户是否存在cookies  如果存在 判断cookies是否可用
	如果cookies不存在 采用selenium登陆
	"""
	if os.path.exists("cookie/%s_cookie"%(username)):
		if check_cookie(username):
			return session
		else:
			#cookie失效
			login(username,password)
			if check_cookie(username):
				return session
			else:
				print("登陆失败")
				return
	else:
		#cookies文件不存在
		login(username,password)
		if check_cookie(username):
			return session
		else:
			print("登陆失败")
			return
		
	

if __name__ == '__main__':
	main("58296672","")
