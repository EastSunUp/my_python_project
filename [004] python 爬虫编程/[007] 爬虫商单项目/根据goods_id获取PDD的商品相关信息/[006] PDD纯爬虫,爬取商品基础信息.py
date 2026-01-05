import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import os
from urllib.parse import quote, urlparse, parse_qs

# ============================== 配置参数 ==========================
goods_id = "62262510595"
output_dir = "pdd_data"  # 保存数据的目录

# ============================== 请求头配置 =======================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

# ============================= 创建输出目录 ==========================
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# ============================= 获取商品页面 ==========================
def get_product_page(goods_id):
    """获取商品页面HTML"""
    url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
    print(f"正在访问商品页面: {url}")

    try:
        # 添加随机延迟避免被封
        time.sleep(random.uniform(1.0, 3.0))

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        if response.status_code == 200:
            # 保存到文件
            filename = os.path.join(output_dir, f"product_html_{goods_id}.json")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    except Exception as e:
        print(f"请求异常: {str(e)}")
        return None


# ============================= 解析商品信息 =======================
def parse_product_info(html, goods_id):
    """从HTML中解析商品信息"""
    soup = BeautifulSoup(html, 'html.parser')
    product_data = {"goods_id": goods_id}

    try:
        # 1. 解析商品标题
        title_tag = soup.find("title")
        if title_tag:
            product_data["title"] = title_tag.text.strip()

        # 2. 解析商品价格
        price_tag = soup.select_one(".price-container .price")
        if price_tag:
            product_data["price"] = price_tag.text.strip()

        # 3. 解析销量
        sales_tag = soup.select_one(".sales-container")
        if sales_tag:
            sales_text = sales_tag.text.strip()
            # 提取数字部分
            sales_num = re.search(r'\d+', sales_text.replace(',', ''))
            if sales_num:
                product_data["sales"] = int(sales_num.group())

        # 4. 解析店铺信息
        shop_tag = soup.select_one(".shop-name")
        if shop_tag:
            product_data["shop_name"] = shop_tag.text.strip()

        # 5. 解析商品描述
        desc_tag = soup.select_one(".goods-desc")
        if desc_tag:
            product_data["description"] = desc_tag.text.strip()

        # 6. 解析商品图片
        image_tags = soup.select(".swiper-slide img")
        if image_tags:
            product_data["images"] = [img.get("src") for img in image_tags if img.get("src")]

        # 7. 解析规格信息
        sku_tags = soup.select(".sku-item")
        if sku_tags:
            skus = []
            for sku in sku_tags:
                sku_name = sku.select_one(".sku-item-name")
                sku_price = sku.select_one(".sku-item-price")
                if sku_name and sku_price:
                    skus.append({
                        "name": sku_name.text.strip(),
                        "price": sku_price.text.strip()
                    })
            product_data["skus"] = skus

        # 8. 尝试解析JSON-LD结构化数据（如果有）
        json_ld = soup.find("script", type="application/ld+json")
        if json_ld:
            try:
                ld_data = json.loads(json_ld.string)
                if isinstance(ld_data, list):
                    for item in ld_data:
                        if item.get("@type") == "Product":
                            product_data.update({
                                "brand": item.get("brand", {}).get("name"),
                                "rating": item.get("aggregateRating", {}).get("ratingValue"),
                                "review_count": item.get("aggregateRating", {}).get("reviewCount")
                            })
                elif isinstance(ld_data, dict) and ld_data.get("@type") == "Product":
                    product_data.update({
                        "brand": ld_data.get("brand", {}).get("name"),
                        "rating": ld_data.get("aggregateRating", {}).get("ratingValue"),
                        "review_count": ld_data.get("aggregateRating", {}).get("reviewCount")
                    })
            except json.JSONDecodeError:
                pass
        else:
            print('网页不存在json_ld数据')

        return product_data

    except Exception as e:
        print(f"解析商品信息时出错: {str(e)}")
        return product_data  # 返回已解析的部分数据


# ======== 保存商品信息 ========
def save_product_info(product_data, goods_id):
    """保存商品信息到文件"""
    filename = os.path.join(output_dir, f"product_{goods_id}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=2)
    print(f"商品信息已保存到: {filename}")
    return filename


# ============================= 主函数 ==========================
def scrape_pdd_product(goods_id):
    """爬取拼多多商品信息"""
    print("=" * 50)
    print(f"开始爬取商品ID: {goods_id} 的信息")
    print("=" * 50)

    start_time = time.time()

    # 1. 获取页面HTML
    html = get_product_page(goods_id)
    if not html:
        print("❌ 无法获取商品页面")
        return None

    # 2. 解析商品信息
    product_data = parse_product_info(html, goods_id)
    if not product_data:
        print("❌ 无法解析商品信息")
        return None

    # 3. 保存结果
    save_path = save_product_info(product_data, goods_id)

    print("\n" + "=" * 50)
    print(f"✅ 成功爬取商品信息")
    print(f"标题: {product_data.get('title', '未知')}")
    print(f"价格: {product_data.get('price', '未知')}")
    print(f"销量: {product_data.get('sales', '未知')}")
    print(f"店铺: {product_data.get('shop_name', '未知')}")
    print(f"保存路径: {save_path}")
    print("=" * 50)

    print(f"总耗时: {time.time() - start_time:.2f}秒")
    return product_data


# ========================== 执行爬取 =============================
if __name__ == "__main__":
    # 可以爬取多个商品
    product_ids = [goods_id]  # 可以添加更多商品ID

    for pid in product_ids:
        scrape_pdd_product(pid)
        print("\n" + "-" * 50 + "\n")

        # 添加随机延迟，避免请求过于频繁
        time.sleep(random.uniform(2.0, 5.0))
