
# TODO 该代码不能运行,需要调试 ?
import requests
from bs4 import BeautifulSoup

def scrape_news_headlines():
    """聚合多个新闻网站的头条新闻"""
    sources = {
        'BBC': 'https://www.bbc.com/news',
        'CNN': 'https://edition.cnn.com/',
        'Reuters': 'https://www.reuters.com/'
    }

    all_headlines = []

    # 设置请求头模拟浏览器访问 # TODO 这个headers在这个文件中不一定适用,需要自主修正
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive'
    }

    for source, url in sources.items():
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        if source == 'BBC':
            headlines = [h3.text.strip() for h3 in soup.select('h3.gs-c-promo-heading__title')]
        elif source == 'CNN':
            headlines = [h3.text.strip() for h3 in soup.select('h3.cd__headline')]
        elif source == 'Reuters':
            headlines = [h3.text.strip() for h3 in soup.select('h3.story-title')]

        all_headlines.append({'source': source, 'headlines': headlines[:5]})

    return all_headlines

