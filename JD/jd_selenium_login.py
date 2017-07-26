# tested on ubuntu15.04
import time
from selenium import webdriver
import http.cookiejar as HC
import requests
#实例化一个session
session=requests.session()
def selenium_login():
	username=""
	password=""
	login_url = 'https://passport.jd.com/new/login.aspx'
	#driver = webdriver.PhantomJS()
	driver = webdriver.Firefox()
	driver.get(login_url)
	driver.find_element_by_link_text("账户登录").click()
	time.sleep(2)
	account = driver.find_element_by_id('loginname')
	passwd = driver.find_element_by_id('nloginpwd')
	submit = driver.find_element_by_id('loginsubmit')

	account.clear()
	account.send_keys(username)
	passwd.send_keys(password)
	submit.click()
	session=requests.session()
	#格式化cookies
	cookie=[]
	for item in driver.get_cookies():
		cookie.append(item["name"]+"="+item["value"])
	
	cookies=";".join(cookie)
	#保存cookies到本地
	with open("cookies","w") as f:
		f.write(cookies)
def cookies_login():
	cookies=open("cookies","r").read()
	session.headers.update({"cookie":cookies})
	home_url = "https://home.jd.com/"
	resp=session.get(home_url)
	return resp.text





def main():
	if "我的京东" in cookies_login():
		print("login success")
	else:
		selenium_login()
		if "我的京东" in cookies_login():
			print("login success")
		else:
			print("登陆失败")
			exit()
	return session
if __name__=="__main__":
	main()




	
	
