import requests
from bs4 import BeautifulSoup

# 接单报价：300-800元/单

# 示例：抓取豆瓣电影TOP250
url = 'https://movie.douban.com/top250'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 提取所有电影标题
for item in soup.select('.info .hd a'):
    title = item.get_text(strip=True)  # 清除空白字符
    print(f'电影标题：{title}')


