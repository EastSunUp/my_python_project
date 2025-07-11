
from urllib.request import Request, urlopen

def get_html(url):
    headers ={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    request = Request(url, headers=headers)
    response = urlopen(request)

def save_html(html):
    pass

def main():
    url = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E5%B0%9A%E5%AD%A6%E5%A0%82&fr=search'
    # url = 'http://tieba.baidu.com/f?kw=%E5%B0%9A%E5%AD%A6%E5%A0%82%ie=utf-8&pn=0'
    html = get_html(url)
    save_html(html)
    pass


