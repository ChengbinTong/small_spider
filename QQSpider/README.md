环境  python3.6  Centos7
    安装selenium模块 添加PhantomJS到环境变量
    
QQZone.py  主要实现登陆
	check_cookie模块查看cookie是否有效  如果有效 返回加载cookie的session给后面的模块使用
	
	如果cookie失效 运行使用selenium模块登陆并且保存cookie到本地  然后加载cookie
	
	代码是在云服务器测试的  没有图形界面  需要输入验证码  我把验证码保存到了/home/tong 下
	
	如果在本机一般不需要验证码  如果需要验证码的话把这个验证码输入一下就可以了
   
   
CareInfo.py
	主要是功能实现
	
	get_index： 提取Qztoken  后面会用到
	
	get_Myinfo  获取用户个人信息
	
	get_care_Me 获取关心我的好友排行详细数据 写入文件
	
	get_Care_her 获取我关心的好友的详细数据 写入文件
	
	get_message 取用户的所有留言
	
	postnew() 自动留言
GetWeather.py
	从中国气象网获取天气信息
参数：
	message:需要留言的信息 
	
	QQtarget需要留言的目标  
	
	qtk ：cookie中提取

	qztoken 直接在首页html代码中
	
	citycode=城市代码 在http://www.weather.com.cn/weather/101200901.shtml获得
