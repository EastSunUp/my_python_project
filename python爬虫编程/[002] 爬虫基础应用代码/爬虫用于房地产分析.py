
import requests
from bs4 import BeautifulSoup # 引用的时候应该这样引用
# beautifulsoup的安装包名称叫做beautifulsoup4而不是beautifulsoup

def scrape_real_estate(city):
    """爬取特定城市的房地产数据"""
    url = f"https://www.zillow.com/homes/{city.replace(' ', '-')}_rb/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    properties = []

    for card in soup.select('article.list-card'):
        address = card.select_one('.list-card-addr').text
        price = card.select_one('.list-card-price').text
        details = card.select_one('.list-card-details').text
        link = card['href']

        properties.append({
            'address': address,
            'price': price,
            'details': details,
            'link': link
        })

    return properties


