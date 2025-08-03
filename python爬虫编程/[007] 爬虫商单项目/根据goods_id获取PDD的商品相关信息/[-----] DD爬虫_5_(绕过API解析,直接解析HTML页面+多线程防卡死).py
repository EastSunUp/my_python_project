import json
import time
import random

import pandas as pd
import argparse
import logging
from curl_cffi import requests
from urllib.parse import quote  # 确保这行存在
import os
import re
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdd_crawler.log"),
        logging.StreamHandler()
    ]
)


class PDDCrawler:
    def __init__(self):
        # 用户代理池
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        ]

        # 设备ID池（模拟不同设备）
        self.device_ids = [str(uuid.uuid4()) for _ in range(10)]

        # 请求计数器
        self.request_count = 0
        self.last_request_time = 0

        # 创建会话
        self.session = requests.Session()

    def request_delay(self):
        """智能请求延迟"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        # 基础延迟 - 根据请求频率动态调整
        if self.request_count < 5:
            base_delay = random.uniform(2.0, 3.0)
        elif self.request_count < 10:
            base_delay = random.uniform(3.0, 5.0)
        else:
            base_delay = random.uniform(5.0, 8.0)

        # 确保最小延迟
        if elapsed < base_delay:
            sleep_time = base_delay - elapsed
            logging.info(f"请求延迟: {sleep_time:.2f}秒")
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1

    def get_dynamic_cookie(self):
        """获取动态Cookie - 使用curl_cffi访问首页"""
        try:
            self.request_delay()

            # 使用curl_cffi访问首页
            home_url = "https://mobile.yangkeduo.com/"

            # 生成随机设备ID
            device_id = random.choice(self.device_ids)

            headers = {
                "User-Agent": random.choice(self.user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
                "Referer": "https://www.google.com/",
                "Upgrade-Insecure-Requests": "1",
                "DNT": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "X-Device-Id": device_id  # 关键：添加设备ID
            }

            response = self.session.get(
                home_url,
                headers=headers,
                timeout=15,
                impersonate="chrome110"
            )

            if response.status_code == 200:
                logging.info("成功获取动态Cookie")
                # 尝试从响应中提取实际Cookie
                if 'Set-Cookie' in response.headers:
                    cookies = response.headers['Set-Cookie']
                    # 提取关键Cookie值
                    api_uid_pattern = r'api_uid=([^;]+)'
                    match = re.search(api_uid_pattern, cookies)
                    if match:
                        api_uid = match.group(1)
                        logging.info(f"获取到关键Cookie: api_uid={api_uid}")
                return True
            else:
                logging.warning(f"获取Cookie失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"获取Cookie失败: {e}")
            return False

    def make_api_request(self, url, max_retries=3):
        """执行API请求"""
        for attempt in range(max_retries):
            try:
                self.request_delay()

                # 获取最新Cookie
                self.get_dynamic_cookie()

                # 使用curl_cffi模拟浏览器指纹
                headers = {
                    "User-Agent": random.choice(self.user_agents),
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Connection": "keep-alive",
                    "Referer": "https://mobile.yangkeduo.com/",
                    "X-Requested-With": "com.pinduoduo",  # 关键伪装
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "X-Device-Id": random.choice(self.device_ids)  # 关键：添加设备ID
                }

                # 使用curl_cffi发送请求
                response = self.session.get(
                    url,
                    headers=headers,
                    impersonate="chrome110",  # 模拟Chrome 110
                    timeout=15
                )

                # 检查响应状态
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    logging.warning(f"尝试 {attempt + 1}/{max_retries}: 403 Forbidden 错误")
                    # 更换设备ID并重试
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    logging.warning(f"尝试 {attempt + 1}/{max_retries}: 状态码 {response.status_code}")
                    time.sleep(2 ** attempt)
            except Exception as e:
                logging.error(f"尝试 {attempt + 1}/{max_retries}: 请求异常 - {str(e)}")
                time.sleep(2 ** attempt)

        return None

    def search_products(self, keyword, page=1, limit=10):
        """搜索商品"""
        try:
            # 编码关键词
            encoded_keyword = quote(keyword)

            # 构造搜索URL - 添加时间戳避免缓存
            timestamp = int(time.time() * 1000)
            api_url = f"https://mobile.yangkeduo.com/proxy/api/search?q={encoded_keyword}&page={page}&size={limit}&_={timestamp}"

            # 发送请求
            response = self.make_api_request(api_url)
            if not response:
                logging.warning("API请求失败，返回空结果")
                return []

            # 解析JSON响应
            try:
                data = response.json()
            except json.JSONDecodeError:
                logging.error("响应不是有效的JSON格式")
                return []

            # 提取商品列表
            goods_list = data.get('items', [])

            if not goods_list:
                logging.warning("未找到商品数据")
                return []

            results = []
            for goods in goods_list:
                if len(results) >= limit:
                    break

                goods_id = goods.get('goods_id')
                name = goods.get('goods_name')

                # 价格处理
                price_info = goods.get('normal_price', 0)
                if isinstance(price_info, int):
                    price = price_info / 100
                else:
                    price = 0

                sales = goods.get('sales', 0)

                if goods_id and name:
                    results.append({
                        'goods_id': goods_id,
                        'name': name,
                        'price': price,
                        'sales': sales
                    })

            return results

        except Exception as e:
            logging.error(f"搜索商品时出错: {e}")
            return []

    def get_product_details(self, goods_id):
        """获取商品详情"""
        try:
            # 构造详情URL - 添加时间戳避免缓存
            timestamp = int(time.time() * 1000)
            api_url = f"https://mobile.yangkeduo.com/proxy/api/goods/{goods_id}?_={timestamp}"

            # 发送请求
            response = self.make_api_request(api_url)
            if not response:
                return None

            # 解析JSON响应
            try:
                data = response.json()
            except json.JSONDecodeError:
                logging.error("商品详情响应不是有效的JSON格式")
                return None

            goods_info = data.get('goods', {})
            store_info = data.get('store', {})

            # 提取商品信息
            name = goods_info.get('goods_name', '未知商品')

            # 价格处理
            price_info = goods_info.get('market_price', 0)
            if isinstance(price_info, int):
                price = price_info / 100
            else:
                price = "未知价格"

            sales = goods_info.get('sales', '未知销量')
            shop = store_info.get('store_name', '未知店铺')

            # 商品描述
            desc = goods_info.get('goods_desc', '无描述')

            # 构造结果字典
            result = {
                'goods_id': goods_id,
                'name': name,
                'price': price,
                'sales': sales,
                'shop': shop,
                'description': desc
            }

            return result

        except Exception as e:
            logging.error(f"获取商品详情时出错: {e}")
            return None


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='拼多多商品信息爬取工具')

    # 添加命令参数
    parser.add_argument('--search', type=str, help='搜索关键词')
    parser.add_argument('--detail', type=str, help='商品ID')
    parser.add_argument('--page', type=int, default=1, help='搜索页数 (默认: 1)')
    parser.add_argument('--limit', type=int, default=10, help='每页结果数 (默认: 10)')
    parser.add_argument('--output', type=str, help='输出文件路径 (CSV 或 TXT)')

    args = parser.parse_args()

    # 创建爬虫实例
    crawler = PDDCrawler()

    if args.search:
        # 执行搜索
        logging.info(f"开始搜索: {args.search}, 页数: {args.page}, 每页结果数: {args.limit}")
        results = crawler.search_products(args.search, args.page, args.limit)

        if not results:
            logging.warning("未找到相关商品")
            return

        # 显示结果
        print("\n搜索结果:")
        print("=" * 80)
        for i, item in enumerate(results, 1):
            print(f"{i}. 商品ID: {item['goods_id']}")
            print(f"   名称: {item['name']}")
            print(f"   价格: {item['price']}元")
            print(f"   销量: {item['sales']}")
            print("-" * 60)

        # 导出结果到CSV
        if args.output:
            df = pd.DataFrame(results)
            # 确保文件扩展名为.csv
            if not args.output.lower().endswith('.csv'):
                args.output += '.csv'
            df.to_csv(args.output, index=False, encoding='utf_8_sig')
            logging.info(f"搜索结果已保存到: {args.output}")

    elif args.detail:
        # 获取商品详情
        logging.info(f"开始查询商品ID: {args.detail}")
        details = crawler.get_product_details(args.detail)

        if not details:
            logging.warning("未找到商品详情")
            return

        # 显示详情
        print("\n商品详情:")
        print("=" * 80)
        print(f"商品ID: {details['goods_id']}")
        print(f"商品名称: {details['name']}")
        print(f"价格: {details['price']}")
        print(f"销量: {details['sales']}")
        print(f"店铺: {details['shop']}")
        print("-" * 60)
        print(f"商品描述:\n{details['description']}")
        print("=" * 80)

        # 导出详情到文本文件
        if args.output:
            # 确保文件扩展名为.txt
            if not args.output.lower().endswith('.txt'):
                args.output += '.txt'

            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"商品ID: {details['goods_id']}\n")
                f.write(f"商品名称: {details['name']}\n")
                f.write(f"价格: {details['price']}\n")
                f.write(f"销量: {details['sales']}\n")
                f.write(f"店铺: {details['shop']}\n")
                f.write("-" * 60 + "\n")
                f.write(f"商品描述:\n{details['description']}\n")

            logging.info(f"商品详情已保存到: {args.output}")

    else:
        print("请使用 --search 或 --detail 参数指定操作类型")
        print("示例:")
        print("  搜索商品: python script.py --search \"手机\" --page 1 --limit 10 --output results.csv")
        print("  查询详情: python script.py --detail \"12345678\" --output product.txt")


if __name__ == "__main__":
    main()