
# 示例：简易价格监控脚本（价值约800元）
import requests
from bs4 import BeautifulSoup
import csv
import time


def monitor_prices(urls):
    results = []
    for url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 解析逻辑（不同网站需定制）
            title = soup.select_one('.product-title').text.strip()
            price = soup.select_one('.current-price').text.replace('¥', '')

            results.append({
                'product': title,
                'price': float(price),
                'time': time.strftime("%Y-%m-%d %H:%M")
            })
            time.sleep(1)  # 避免请求过快
        except Exception as e:
            print(f"爬取失败: {url} - {str(e)}")
    return results


# 进阶功能示例（价值约8000元）
# - 自动更换代理IP
# - 邮件价格报警
# - 历史价格对比
def check_price_drop(current_price, product_id):
    # 从数据库获取30天最低价
    historical_low = db.query("SELECT MIN(price) FROM prices WHERE product_id = ?", (product_id,))

    # 如果当前价低于历史最低5%
    if current_price < historical_low * 0.95:
        send_alert_email(
            subject=f"价格警报: {product_id}",
            content=f"当前价: {current_price} | 历史最低: {historical_low}"
        )

def send_alert_email(subject, content):
    # 邮件发送实现（简化版）
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = 'monitor@yourcompany.com'
    msg['To'] = 'admin@yourcompany.com'

    with smtplib.SMTP('smtp.server.com', 587) as server:
        server.login('user', 'password')
        server.send_message(msg)

# 使用示例
if __name__ == "__main__":
    target_urls = [
        'https://example.com/product/123',
        'https://example.com/product/456'
    ]
    data = monitor_prices(target_urls)

    # 保存结果
    with open('prices.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product', 'price', 'time'])
        writer.writerows(data)



