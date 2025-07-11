

# 示例：XPath提取数据
from lxml import etree
import aiohttp
# import requests
import requests

# TODO 该代码没有调试,不能运行,记得调试 !
html = etree.HTML(response.text)
title = html.xpath('//h1[@class="title"]/text()')[0]

# 异步爬虫示例
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

