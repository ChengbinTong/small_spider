# -*- coding: utf-8 -*-
import scrapy
import json
from music.items import MusicItem
import sqlite3

class NetspiderSpider(scrapy.Spider):
    name = 'netspider'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/#/song?id=139357']
    def parse(self, response):
        cn = sqlite3.connect('music.db')
        count=cn.execute('select count(*) from musiccomment').fetchall()[0][0]
        if count==0:
            songid=0
        #获取最高songid作为参考
        else:
            songid=cn.execute('select MAX(songid) FROM musiccomment').fetchall()[0][0]
        print(songid)
        i=0
        #songid=5000000
        #在这里设置每次爬取的量i 如果需要测试可以手动设置起始id songid在500000左右数据密集
        #每次爬取的量不可以太小 不然无法跳出 或者可以单独生成一个log 记录每次爬取的进度 
        while i<10000:
        	url="http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(songid)
        	data={
        	"params":"DSL9YFp0bLtGRawsOHSscNNCNcn+WO5k4sTcefTJ1VJqapS+6zt1ukJs+uj4C7m1MiJzVe44GbIQyW7TTM2ultoUTnHyCYDvm3fvMSlGJl2YxF/ViYbFKvsX5qoMjcQXdyM39sCZMiDQeZmgaokExg0Mwhp0xxxf0iMhK8MrB6eZcLc7yuB7Pz4tYRMud5Rq",
        	"encSecKey":"3b6ec2b9337bf3b3f4d523be5e55a3263347d16f7c762e585338d00d949fcdc85c4afe307be5fed7e6810649802656a85a320166324557397d5e8ad50096c55b2a580e855da214d65704ab15b42e284551e3c3fd51e92c685bb47b3aa6477bd6f23c2b8e7c64ccc71740da33f1ef9e77e5507557928202898540c320ad1a8e59"
        	}
        	
        	yield scrapy.FormRequest(url,formdata=data,callback=self.getinfo,meta={'songid':str(songid)})
        	songid=int(songid)+1
        	i+=1
    def getinfo(self,response):
    	#歌曲存在
    	r=json.loads(response.text)
    	item=MusicItem()
    	if 	r['comments'] !=[] and r['total'] >50:#在这里可以设置最小评论数过滤
    		songid=response.meta['songid']
    		item['songid']=int(songid)
    		item['total']=int(r['total'])
    		#print(str(songid)+"-----------"+str(r['total']))
    		#with open('log.txt','w') as f:
    		#	f.write(songid)
    		return item
    	else:
    		songid=response.meta['songid']
    		#with open('log.txt','w') as f:
    		#	f.write(songid)
    		pass