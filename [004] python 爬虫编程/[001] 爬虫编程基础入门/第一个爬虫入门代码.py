
from urllib.request import urlopen

# 第一个爬虫程序: 爬取百度搜索网页的html中的内容.

# 要访问的网址
url = 'http://www.baidu.com'
# 发送请求
response = urlopen(url)
# 读取请求
info = response.read()
# 打印内容
# print(info)
print(info.decode())
# 返回HTTP的响应码//200:成功//404:失败
print(response.getcode())
# 返回实际访问的url
print(response.geturl())
# 返回HTTP响应头
print(response.info())

