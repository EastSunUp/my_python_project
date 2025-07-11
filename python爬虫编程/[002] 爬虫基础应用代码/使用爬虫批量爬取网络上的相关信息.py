
# commit to git !
import re # 正则表达式
import requests
from bs4 import BeautifulSoup


def search_google(keyword, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": keyword,
        "key": api_key,
        "cx": cse_id,
        "num": 10  # 获取10条结果
    }
    response = requests.get(url, params=params)
    results = response.json()
    return [item["link"] for item in results.get("items", [])]

# 使用示例
api_key = "YOUR_GOOGLE_API_KEY"
cse_id = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
urls = search_google("人工智能最新研究", api_key, cse_id)
print(f"获取到{len(urls)}个相关URL")

def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # 模拟浏览器
        response = requests.get(url, headers=headers, timeout=10)
        # 返回200表示访问成功,返回404表示没有该网页或者访问失败
        if response.status_code == 200:
            return response.text  # 返回HTML内容
        return None
    except Exception as e:
        print(f"抓取失败 {url}: {str(e)}")
        return None


# 批量抓取示例
for url in urls[:5]:  # 只抓取前5个作为演示
    html = scrape_website(url)
    if html:
        # 下一步：信息提取
        print(f"成功抓取: {url}")

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # 尝试提取标题 - 不同网站可能使用不同标签
    title = soup.find('h1')
    title = title.text if title else "无标题"

    # 尝试提取正文 - 使用通用正文提取算法
    main_content = soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        # 更智能的正文提取
        paragraphs = soup.find_all('p')
        main_content = "\n".join(p.text for p in paragraphs)
    else:
        main_content = main_content.text

    # 尝试提取发布日期
    date = soup.find('time')
    date = date['datetime'] if date and date.has_attr('datetime') else "未知日期"

    return {
        "title": title,
        "content": main_content[:500] + "..." if len(main_content) > 500 else main_content,
        "date": date
    }

# 使用示例
for url in urls[:3]:
    html = scrape_website(url)
    if html:
        info = extract_info(html)
        print(f"\n标题: {info['title']}")
        print(f"日期: {info['date']}")
        print(f"内容摘要: {info['content'][:100]}...")


# 性能优化后的爬虫代码------------------------------------------------------------
# 使用异步提高效率
import asyncio
from aiohttp import ClientSession

async def async_scrape(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 批量异步抓取
async def batch_scrape(urls):
    tasks = [async_scrape(url) for url in urls]
    return await asyncio.gather(*tasks)
