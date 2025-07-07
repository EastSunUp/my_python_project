
from bs4 import BeautifulSoup
import requests

def monitor_amazon_price(product_url):
    """监控亚马逊商品价格变化"""
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取商品信息
    title = soup.select_one('#productTitle').text.strip()
    price = soup.select_one('span.a-offscreen').text
    availability = soup.select_one('#availability').text.strip()

    # 价格低于阈值时发送通知
    if float(price.replace('$', '').replace(',', '')) < 100:
        print(f'title:{title}, price:{price}')  # 打印报警时候的价格
        # send_email_alert(title, price)

    return {'title': title, 'price': price, 'availability': availability}

