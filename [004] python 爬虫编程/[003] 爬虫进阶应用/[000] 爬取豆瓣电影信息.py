
import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import os
import re

# TODO 豆瓣网最新加入了验证码机制,这份爬虫代码需要更新(增加cookies验证机制)
# 设置请求头模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.baidu.com/',    # 'https://www.google.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive'
}

def get_movie_details(url):
    """获取单个电影的详细信息"""
    time.sleep(random.uniform(1.0, 3.5))  # 随机延迟避免被封
    # 使用会话保持Cookies
    session = requests.Session()
    session.headers.update(headers)
    # response = session.get(url)
    time.sleep(random.uniform(1.0, 2.5))  # 随机延迟避免被封
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取电影标题
    title = soup.find('span', property='v:itemreviewed').text.strip()
    # 提取导演信息
    directors = [a.text.strip() for a in soup.select('a[rel="v:directedBy"]')]
    # 提取评分
    rating = soup.find('strong', class_='ll rating_num').text.strip()

    # 提取年份、地区、类型
    info = soup.find('div', id='info').text
    year = re.search(r'(\d{4})', info).group(1) if re.search(r'(\d{4})', info) else ""
    region = re.search(r'制片国家/地区: (.*?)\n', info)
    region = region.group(1).strip() if region else ""                          # 提取地区
    # 为什么有的时候使用select? 有点时候不用?(select的意思是提取,有分类的功能)
    genres = [a.text.strip() for a in soup.select('span[property="v:genre"]')]  # 提取类型

    # 提取简介
    summary = soup.find('span', property='v:summary')
    summary = summary.text.strip() if summary else ""

    return {
        'title': title,                     # 电影标题
        'directors': '/'.join(directors),   # 导演信息
        'rating': rating,                   # 电影评分
        'year': year,                       # 年份
        'region': region,                   # 地区
        'genres': '/'.join(genres),         # 电影类型
        # 提取简介
        'summary': summary.replace('\n', ' ').replace('\u3000', ' ')
    }

def scrape_douban_top250():
    """爬取豆瓣Top250电影数据"""
    base_url = "https://movie.douban.com/top250?start={}&filter="
    all_movies = []

    # 爬取所有10页数据(每页25条)
    for page in range(0, 250, 25):
        url = base_url.format(page) # 每隔25页开始
        print(f"正在爬取: {url}")

        time.sleep(random.uniform(1.0, 3.0))  # 随机延迟
        # 登录这个网页?
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"请求失败,状态码: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        movie_items = soup.find_all('div', class_='info')   # 电影表单信息表

        for item in movie_items:
            link = item.find('a')['href']   # 分离出链接地址
            # 分离出爬取的电影信息
            movie_data = get_movie_details(link)
            if movie_data:
                all_movies.append(movie_data)
                print(f"已获取: {movie_data['title']}")

    return all_movies

def save_to_csv(movies, filename='douban_top250.csv'):
    """将数据保存到CSV文件(保存为表格形式的文本文件)"""
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['title', 'directors', 'rating', 'year', 'region', 'genres', 'summary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies)
    print(f"数据已保存到 {os.path.abspath(filename)}")

def main():
    print("开始爬取豆瓣电影Top250...")
    movies = scrape_douban_top250()

    if movies:
        save_to_csv(movies)
        print(f"成功爬取 {len(movies)} 部电影数据")
    else:
        print("未能获取电影数据")

if __name__ == "__main__":
    main()
