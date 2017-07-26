# coding=utf-8
import random
import requests
import sys
import os
from bs4 import BeautifulSoup
from LoginInfo import passwd as LogInfo
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s=requests.session()
path=sys.path[0]

#s.proxies={"http": "http://110.73.30.214:8123","https": "http://121.31.85.200:8123",}

def get_index():
    #测试几次 发现直接访问验证码 然后获取到的cookie登陆会提示系统忙  需要先访问首页 获取cookie 再获取验证码
    s.headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",   
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"kyfw.12306.cn",
        "Referer":"https://kyfw.12306.cn/otn/",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    s.get("https://kyfw.12306.cn/otn/login/init",verify=False)
def _login_captcha():
    #下载验证码
    rand = random.uniform(0, 1)
    s.headers={
    "Accept":"image/webp,image/*,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8",
    #"Accept-Encoding":"gzip, deflate, sdch",
    "Connection":"keep-alive",
    "Host":"kyfw.12306.cn",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Referer":"https://kyfw.12306.cn/otn/login/init",
    }
    url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&{}'.format(str(rand))
    """
    parameters = [
        ('module', 'login'),
        ('rand', 'sjrand'),
        (str(rand),'')
    ]
    """
    resp = s.get(url,verify=False)
    if resp.status_code == 200:
        with open(path+'\captcha.png', 'wb') as f:
            f.write(resp.content)
        return True
    else:
        print('获取图片验证码失败')
        return False

#生成验证码
def codexy(numcode):
    #输入第几张图片组成的数字 比如第一二张图片 输入12 返回randCode进行验证
    codestr = []
    offsetsX = 0  # 选择的答案的left值,通过浏览器点击8个小图的中点得到的,这样基本没问题
    offsetsY = 0  # 选择的答案的top值
    
    
    for ofset in str(numcode):
        if ofset == '1':
            offsetsY = 49
            offsetsX = 42
        elif ofset == '2':
            offsetsY = 45
            offsetsX = 105
        elif ofset == '3':
            offsetsY = 46
            offsetsX = 185
        elif ofset == '4':
            offsetsY = 49
            offsetsX = 256
        elif ofset == '5':
            offsetsY = 37
            offsetsX = 118
        elif ofset == '6':
            offsetsY = 113
            offsetsX = 114
        elif ofset == '7':
            offsetsY = 113
            offsetsX = 182
        elif ofset == '8':
            offsetsY = 112
            offsetsX = 251
        else:
            pass
        codestr.append(offsetsX)
        codestr.append(offsetsY)
    randCode = str(codestr).replace(']', '').replace('[', '').replace("'", '').replace(' ', '')
    return randCode
  

def _login_check_captcha(code):
    url = r'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
    parameters = [
        ('randCode', code),
        ('rand', 'sjrand')
    ]
    headers={
        "Accept":"*/*",
        #"Accept-Encoding":"gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        #"Content-Length": "60",#待测试
        }
    s.headers.update(headers)
    resp = s.post(url, parameters, verify=False)
    if resp.status_code == 200:
        js = resp.json()
        if js['data']['result'] == '1':
            return True
        else:
            return False
    else:
        print('%s [ERROR]' % resp.status_code)
    return False

def _login(username,password):
    get_index()
    _login_captcha()
    numcode=input("Pleace input numcode:")
    code=codexy(numcode)
    #如果验证码补位True 进入循环 知道验证码正确  退出循环
    while _login_check_captcha(code) != True:
        print("验证码错误")
        _login_captcha()
        numcode=input("Pleace input numcode:")
        code=codexy(numcode)
    print("验证码验证成功！")
    
    url = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
    login_headers={
        "Content-Length":"110",
        }
       
    #s.headers.update(login_headers)
    parameters = {
        'loginUserDTO.user_name': username,
        'userDTO.password': password,
        'randCode': code
    }
    resp = s.post(url,data=parameters)
    if resp.status_code == 200:
        js = resp.json()
        if js['status'] == True:
            try:
                if js['data']['loginCheck'] == "Y":
                    print("登陆成功^_^")
                    cookies = requests.utils.dict_from_cookiejar(s.cookies)
                    with open(path+"/cookie_"+username,"w") as f:
                        f.write(str(cookies))
                    print("cookies已保存")
                else:
                	print(js)
                	print(js['data'])
            except Exception as e:
            	print(js)
            	print("登陆失败")
            	print(e)

        else:
            print(js['messages'])
            return 
    return s.cookies
def main(username,password):
    frist_headers={
    "Accept":"text/html",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"10",
    "Content-Type":"application/x-www-form-urlencoded",
    "Host":"kyfw.12306.cn",
    "Origin":"https://kyfw.12306.cn",
    "Referer":"https://kyfw.12306.cn/otn/userSecurity/bindTel",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }
    userurl="https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo"
    if os.path.exists(path+"/cookie_%s"%(username)):
    	print("正在检验cookie是否有效！")
    	cookie=open(path+"/cookie_"+username).read()
    	cookie=eval(cookie)
    	r=s.post(userurl,cookies=cookie,verify=False,headers=frist_headers,data={"_json_att":""})
    	r.encoding="utf-8"
    	soup=BeautifulSoup(r.text,"html.parser")
    	if "我的" in str(soup.title):
    		print("Cookie可用！QAQ")
    		return cookie
    	else:
    		print("Cookie失效 准备验证码登陆吧! ￣□￣｜｜")
    		_login(username,password)
    		cookie=open(path+"/cookie_"+username).read()
    		cookie=eval(cookie)
    		return cookie
    else:
    	print("NOT found Cookie 准备验证码登陆吧! ￣□￣｜｜")
    	_login(username,password)
    	cookie=open(path+"/cookie_"+username).read()
    	cookie=eval(cookie)
    	return cookie

if __name__ == '__main__':
	username=LogInfo("accunt")
	passwd=LogInfo("passwd")
	cookie=main(username,passwd)
