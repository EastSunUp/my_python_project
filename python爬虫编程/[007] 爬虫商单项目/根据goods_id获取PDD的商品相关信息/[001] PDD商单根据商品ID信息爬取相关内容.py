

# import sys
import os
import csv
import re
import time
import random
# import threading
import json
import requests
from bs4 import BeautifulSoup

# 基础配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'Referer': 'https://mobile.yangkeduo.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
CSV_FILE = 'pdd_products.csv'
PRODUCT_IDS = ['12345678', '23456789','62262510595']  # 替换为实际商品ID列表
MAX_RETRIES = 3
REQUEST_DELAY = 1.5  # 请求延迟(秒)


def get_product_info(product_id):
    """根据商品ID获取商品信息"""
    url = f'https://mobile.yangkeduo.com/goods.html?goods_id={product_id}'

    for attempt in range(MAX_RETRIES):
        try:
            # 发送请求
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 定位包含商品信息的JSON数据
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if not script_tag:
                raise ValueError("未找到商品数据标签")

            json_data = script_tag.string

            # 使用正则提取关键信息
            title_match = re.search(r'"goodsName":"(.*?)"', json_data)
            price_match = re.search(r'"minGroupPrice":(\d+)', json_data)
            sales_match = re.search(r'"sales":(\d+)', json_data)
            shop_match = re.search(r'"mallName":"(.*?)"', json_data)

            # 处理提取结果
            title = title_match.group(1) if title_match else 'N/A'
            price = int(price_match.group(1)) / 100 if price_match else 0
            sales = int(sales_match.group(1)) if sales_match else 0
            shop = shop_match.group(1) if shop_match else 'N/A'

            return {
                'id': product_id,
                'title': title,
                'price': f"{price:.2f}",
                'sales': sales,
                'shop': shop
            }

        except (requests.RequestException, ValueError) as e:
            print(f"请求失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {str(e)}")
            time.sleep(2 ** attempt)  # 指数退避策略
        except Exception as e:
            print(f"解析错误: {str(e)}")
            break

    return None


def save_to_csv(data, filename):
    """将数据保存到CSV文件"""
    fieldnames = ['id', 'title', 'price', 'sales', 'shop']

    # 第一次写入时创建文件并写入表头
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    # 追加数据
    with open(filename, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)


# ---------------------------------------------------------------------------
def get_pdd_token(app_key, app_secret):
    """ 获取拼多多API的访问令牌 """
    url = "https://gw-api.pinduoduo.com/api/router"
    params = {
        "type": "json",
        "client": "web",
        "method": "pdd.oauth.token",
        "data_type": "json",
        "client_id": app_key,
        "client_secret": app_secret,
        "grant_type": "client_credential"
    }
    response = requests.get(url, params=params)
    response_data = response.json()
    if response_data['status'] == 0:
        return response_data['data_token']
    else:
        raise Exception("Failed to get token: " + response_data['msg'])


def get_product_detail(access_token, pdd_sku_id):
    """ 获取商品详情 """
    url = "https://gw-api.pinduoduo.com/api/router"
    params = {
        "type": "json",
        "client": "web",
        "method": "pdd.ddk.goods.detail",   # 这里指的是接口明朝
        "data_type": "json",
        "access_token": access_token,
        "pdd_sku_id": pdd_sku_id,  # 商品ID # PDD的这个接口已经禁用了goods_id了,使用的是goods_sign
    }
    response = requests.get(url, params=params)
    return response.json()


# 使用你的AppKey和AppSecret替换下面的值
app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
pdd_sku_id = '62262510595'  # 示例SKU ID，请替换为实际SKU ID

try:
    access_token = get_pdd_token(app_key, app_secret)
    product_detail = get_product_detail(access_token, pdd_sku_id)
    print(json.dumps(product_detail, indent=4, ensure_ascii=False))  # 打印商品详情，美化输出中文等非ASCII字符
except Exception as e:
    print(e)


if __name__ == '__main__':
    print(f"开始爬取 {len(PRODUCT_IDS)} 个商品数据...")

    for idx, pid in enumerate(PRODUCT_IDS):
        print(f"正在处理商品 {idx + 1}/{len(PRODUCT_IDS)} (ID: {pid})")

        product_data = get_product_info(pid)

        if product_data:
            save_to_csv(product_data, CSV_FILE)
            print(f"成功保存: {product_data['title'][:20]}...")
        else:
            print(f"无法获取商品数据: {pid}")

        # 随机延迟避免封禁
        time.sleep(REQUEST_DELAY + random.uniform(0, 0.5))

    print(f"爬取完成! 数据已保存至 {CSV_FILE}")




