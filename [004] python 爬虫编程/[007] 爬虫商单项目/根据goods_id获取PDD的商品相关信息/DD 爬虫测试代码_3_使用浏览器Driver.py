import requests
import json
import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

def get_pdd_product_data_with_selenium(goods_id):
    """使用浏览器自动化获取拼多多商品数据（自动管理驱动）"""
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    try:
        # 自动下载和管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 访问商品页面
        url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
        driver.get(url)

        # 等待页面加载完成
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-detail-loaded='true']"))
            )
        except:
            # 如果找不到元素，等待5秒确保页面加载
            time.sleep(5)

        # 获取页面源码
        page_source = driver.page_source

        # 从页面源码中提取JSON数据
        match = re.search(r'window\.rawData\s*=\s*({.*?});', page_source, re.DOTALL)
        if match:
            json_data = match.group(1)
            try:
                product_data = json.loads(json_data)
                return product_data
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {str(e)}")
                return {"error": "JSON解析错误", "raw_data": json_data}

        return {"error": "无法在页面中找到商品数据"}

    except Exception as e:
        print(f"浏览器自动化错误: {str(e)}")
        return {"error": str(e)}
    finally:
        if 'driver' in locals():
            driver.quit()


def save_product_data(data, goods_id):
    """保存商品数据到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pdd_{goods_id}_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 商品数据保存成功: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 保存失败: {str(e)}")
        return None


def extract_product_info(data):
    """从商品数据中提取关键信息"""
    if not data or "error" in data:
        return None

    try:
        # 尝试从不同位置获取商品信息
        if 'goods' in data:
            goods = data['goods']
        elif 'store' in data and 'initDataObj' in data['store'] and 'goods' in data['store']['initDataObj']:
            goods = data['store']['initDataObj']['goods']
        else:
            print("无法定位商品信息")
            return None

        # 提取基本信息
        product_info = {
            "goods_id": goods.get("goods_id", ""),
            "goods_name": goods.get("goods_name", ""),
            "market_price": goods.get("market_price", 0) / 100,
            "sales": goods.get("sales", 0),
            "goods_sign": goods.get("goods_sign", ""),
            "image_url": goods.get("image_url", "")
        }

        return product_info
    except Exception as e:
        print(f"提取信息失败: {str(e)}")
        return None


# 主程序
if __name__ == "__main__":
    # 商品ID - 替换为您要查询的商品ID
    goods_id = "62262510595"

    print(f"开始获取商品数据: {goods_id}")
    print("正在启动浏览器自动化...")

    # 获取商品数据
    product_data = get_pdd_product_data_with_selenium(goods_id)

    if product_data:
        # 保存原始JSON数据
        json_file = save_product_data(product_data, goods_id)

        # 提取关键信息
        product_info = extract_product_info(product_data)

        if product_info:
            print("\n商品关键信息:")
            print(f"商品ID: {product_info['goods_id']}")
            print(f"商品名称: {product_info['goods_name']}")
            print(f"商品价格: {product_info['market_price']}元")
            print(f"销量: {product_info['sales']}")
            print(f"商品签名: {product_info['goods_sign']}")
        else:
            print("⚠️ 无法提取商品关键信息，但原始数据已保存")
    else:
        print("❌ 无法获取商品数据")
        print("备选方案：使用纯请求方法...")


        # 备选方案：使用纯请求方法
        def get_pdd_product_data_simple(goods_id):
            """简单获取商品数据方法"""
            url = f"https://mobile.yangkeduo.com/proxy/api/goods/{goods_id}/detail"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Referer": f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}",
                "Accept": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"请求失败: {str(e)}")
                return None

        # 尝试备选方案
        product_data = get_pdd_product_data_simple(goods_id)
        if product_data:
            save_product_data(product_data, f"{goods_id}_alt")
            print("✅ 使用备选方案成功获取数据")
        else:
            print("❌ 所有方法均失败")
            print("手动获取方法:")
            print(f"1. 访问: https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}")
            print("2. 按F12打开开发者工具")
            print("3. 在控制台执行: copy(window.rawData)")
            print("4. 将复制的内容粘贴到文本文件中")
