import requests
import json
import random

def render_page_via_service(url):
    """使用第三方渲染服务获取页面内容"""
    # 选择无头浏览器服务（轮换使用）
    services = [
        {
            'url': 'https://api.render-wizard.com/v1/render',
            'api_key': 'your_api_key_1',
            'params': {'wait': 5000, 'block_ads': True}
        },
        {
            'url': 'https://headless-proxy.io/render',
            'api_key': 'your_api_key_2',
            'params': {'wait_for': '.product-list', 'timeout': 10000}
        }
    ]

    service = random.choice(services)

    payload = {
        'url': url,
        'apikey': service['api_key'],
        **service['params']
    }

    response = requests.post(service['url'], json=payload)
    result = response.json()

    if result['status'] == 'success':
        return result['html']
    else:
        raise Exception(f"渲染失败: {result['error']}")


# 使用示例
html_content = render_page_via_service('https://target-site.com/products?q=商品')