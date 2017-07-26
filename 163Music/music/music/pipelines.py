# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import sqlite3

class MusicPipeline(object):
	def open_spider(self, spider):
		self.cn = sqlite3.connect('music.db')
	def process_item(self, item, spider):
		self.cn.execute("INSERT INTO musiccomment (songid,total) values('%d','%d')"
		%(item['songid'],item['total']))

	def close_spider(self,spider):
		#因为是多线程 如果中间出现错误停止 下次开始任然不好判断起始id 当异常退出 直接放弃本次数据 不然会出现数据漏掉情况
		self.cn.commit()
		self.cn.close()