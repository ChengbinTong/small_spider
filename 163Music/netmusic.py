import requests
import threading
import sqlite3

#存储数据
def save_data(songid,total):
	con=sqlite3.connect('mucic.db')
	#必须手动创建musiccomment表
	con.execute('INSERT INTO musiccomment(songid,total) VALUES(%d,%d)'%(songid,total))
	con.commit()
#获取数据
def get_data(startid,endid):
	data={
			"params":"e+qzcnlpVVmofIpft0Fo5J0HzQhmV+Fxo/9/hg2NMKZpl/3FUecjdcZo2tgve22aRbB1WDXm8CMh9Z+nDFYnb+zDbCwvU88Ja3H/9fOA49fkxhwiYkYb4Li2A7ucO5Kj84kqcHuRFTFUTbphzhkaFQ==",
			"encSecKey":"9210e896f057ecb2ef9f0def5414e6f34eaecd26198502c30e2f879c374bc5d29c2428f20a85ce488137c88f65057302944278e2e7886d814ca51904ee2c40b8e2fb19edbeb4a24a575916fcb5ecc9666eb8ed544290ab90ae8e3d65efd4e629479c478c3812d3f86f1c2e3d09c171338606ea71be2c7f65fbd0921e7cefe5d3"
			}
	headers={
    	'Cookie': 'appver=1.5.0.75771',
    	'Referer': 'http://music.163.com',
    	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
			}
	for songid in range(startid,endid):
		url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % (str(songid))
		print(url)
		r = requests.post(url,headers=headers,data=data)
		#判断返回是否成功
		if r.status_code == 200 and r.json()['comments'] !=[]:
			pass
		else:
			continue
		total_comments = r.json()['total']
		if total_comments >=50:
			save_data(songid,total_comments)
		else:
			continue


def crreat_thread(th,start,num):
	oneth=int(num/th)
	idlist=[]
	for i in range(th):
		one=int(start+num*(i+1)/th)
		idlist.append(one)
	
	thread = []
	for i in range(th):
		args=(start+oneth*i,start+oneth*(i+1))
		t=threading.Thread(target=get_data,args=args)
		thread.append(t)
	#启动线程
	for i in thread:
		i.start()
	for i in thread:
		i.join()

	
if __name__=='__main__':
	#th 线程数
	th=10
	start=5000000#开始id
	#本次需要爬取的id总数
	num=1000
	crreat_thread(th,start,num)