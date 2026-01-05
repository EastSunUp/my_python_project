

# 示例：XPath提取数据
from lxml import etree
import aiohttp
# import requests
import requests

url = "www.douban.com"
mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://mobile.yangkeduo.com/',
            'Accept-Encoding': 'gzip, deflate, br',
        }
response = requests.get(url, headers=mobile_headers, timeout=15)    # 注意使用get方法

# TODO 该代码没有调试,不能运行,记得调试 !
html = etree.HTML(response.text)    # 这个函数可以把txt文件变成html树的形式(拷贝的文本是否也可以?)
title = html.xpath('//h1[@class="title"]/text()')[0]

# 异步爬虫示例
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

