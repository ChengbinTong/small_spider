import QQZone
cookie=get_rawCookie(username)
	gtk=get_gtk(username)
	info_url="https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin=%s&vuin=%s&fupdate=1&g_tk=%s"%(username,username,gtk)
	"""
	session.headers.update({"path":"/58296672"})
	session.headers.update({"upgrade-insecure-requests":"1"})
	session.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"})
	"""
	session.headers.update({"cookie":cookie})
	resp=session.get(info_url)
	data_text=resp.text.replace("_Callback","")[1:-2]
	data=json.loads(data_text)
	login_status=data["message"]
	if login_status == "获取成功":
		qqnum=data["data"]["uin"]
		return True
	else:
		return False
	
