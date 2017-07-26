import requests
import time
import json
import re
import  jd_selenium_login as login
#调用session
stock_id="4099139"
session=login.main()
area="17_1381_50718_0"
def get_status():
	extraParam={"originid":"1"}
	cat='737,794,880'

	status_url = 'https://c0.3.cn/stock?skuId={}&area={}&cat={}'.format(stock_id,area,cat)+"""&extraParam={"originid":"1"}"""
	gs_resp=session.get(status_url).text
	gs_json=json.loads(gs_resp)
	city=gs_json["stock"]["area"]["provinceName"]+"--"+gs_json["stock"]["area"]["cityName"]+"--"+gs_json["stock"]["area"]["countyName"]
	gs_status=gs_json["stock"]["StockState"]
	return gs_status
	
	#print(gs_resp)
	#获取商品标题
def get_title():
	stock_link="http://item.jd.com/{0}.html".format(stock_id)
	goods_resp=session.get(stock_link)
	gs_title=re.findall(r"<title>(.+?)</title>",goods_resp.text)[0]
	return gs_title
#获取价格函数
def get_price():
	price_url="https://p.3.cn/prices/mgets"
	payload={
	"type":"1",
	"pduid":str(time.time()*1000),
	"skuIds":"J_"+stock_id
	}
	goods_resp=session.get(price_url,params=payload)
	#从js中提取价格
	goods_price=eval(goods_resp.text[1:-2])["p"]
	return goods_price
def add_cart():
	pid=stock_id
	pcount=1#件数
	ptype=1
	buy_car_url="https://cart.jd.com/gate.action?pid={}&pcount={}&ptype={}".format(pid,pcount,ptype)
	r=session.get(buy_car_url)
	if "商品已成功加入购物车" in r.text:
		print("商品已成功加入购物车")
if __name__=="__main__":
	price=get_price()
	title=get_title()
	status=get_status()
	print("Name："+title)
	print("Price："+price)
	if status==33:
		print("状态：有货")
		Isbuy=input("是否加入购物车Y/N：")
		if Isbuy=="Y":
			add_cart()
		else:
			print("END!")
			exit()
	
	else:
		print("状态：无货")
		Iscode=input("是否监听Y/N:")
		if Iscode=="Y":
			print(get_status())
			while get_status()!="33":
				print("正在监听.....",end="\r")
		else:
			print("erro")
		
	