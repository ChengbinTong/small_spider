scrapy写的爬取网易云音乐评论数 目的是爬取top500 所以计划是爬取到了id之后 过滤出评论top500的ip再爬取歌曲信息
scrapy是多线程爬取 所以就算记录断点信息也没有用 因此不支持断点续爬 直接放弃本次数据
部分数据
![image](https://github.com/ChengbinTong/small_spider/blob/master/163Music/TIM20170726101219.png)
