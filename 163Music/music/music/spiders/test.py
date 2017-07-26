import requests
u='http://music.163.com/#/playlist?id=65415757'
a=requests.get(u)
print(a)