

import requests
import time
import json
import os
import hashlib
import re
import random
from datetime import datetime
from urllib.parse import urlencode

# 配置信息
app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
access_token = '92ff137bb298427abbb66a46696f5c13dfb97c6c'
goods_id = "62262510595"  # 商品ID

# 创建会话对象
session = requests.Session()


def generate_sign(params, app_secret):
    """生成API签名 - 符合拼多多要求"""
    # 1. 排序所有参数（按参数名ASCII码从小到大排序）
    sorted_params = sorted(params.items(), key=lambda x: x[0])

    # 2. 拼接参数（使用原始值,不进行URL编码）
    param_str = app_secret
    for k, v in sorted_params:
        param_str += f"{k}{v}"
    param_str += app_secret

    # 3. MD5加密并转为大写
    return hashlib.md5(param_str.encode('utf-8')).hexdigest().upper()


def get_valid_goods_sign(goods_id):
    """获取有效的GoodsSign（28-64个字符，以_分隔）"""
    print(f'获取商品 {goods_id} 的有效GoodsSign...')

    # 方法1: 通过搜索API获取GoodsSign
    try:
        # 基础公共参数
        base_params = {
            "client_id": app_key,
            "access_token": access_token,
            "timestamp": str(int(time.time())),
            "data_type": "JSON",
            "version": "v1",
        }

        # 搜索接口参数
        method_params = {
            "type": "pdd.ddk.goods.search",
            "keyword": goods_id,  # 使用商品ID作为关键词
            "page": 1,
            "page_size": 1,
            "with_coupon": "false"
        }

        # 合并参数
        all_params = {**base_params, **method_params}

        # 生成签名
        sign = generate_sign(all_params, app_secret)
        all_params["sign"] = sign

        # 发送POST请求
        url = "https://gw-api.pinduoduo.com/api/router"
        response = session.post(url, data=all_params)
        response_data = response.json()

        # 解析响应
        if "goods_search_response" in response_data:
            goods_list = response_data["goods_search_response"].get("goods_list", [])
            if goods_list:
                goods_info = goods_list[0]
                goods_sign = goods_info.get("goods_sign", "")
                if len(goods_sign) >= 28 and len(goods_sign) <= 64 and '_' in goods_sign:
                    print(f"✅ 通过搜索API获取到有效GoodsSign: {goods_sign}")
                    return goods_sign

        print(f"⚠️ 搜索API未返回有效GoodsSign: \n{response.text[:200]}")
    except Exception as e:
        print(f"搜索API请求异常: {str(e)}")

    # 方法2: 备选方案 - 通过商品页面解析
    print("尝试通过商品页面解析GoodsSign...")
    try:
        url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

        # 访问商品页面
        response = session.get(url, headers=headers)
        response.raise_for_status()

        # 从页面内容中提取GoodsSign
        match = re.search(r'goods_sign=([a-zA-Z0-9_-]{28,64})', response.text)
        if match:
            goods_sign = match.group(1)
            print(f"✅ 通过页面解析获取到GoodsSign: {goods_sign}")
            return goods_sign

        # 从重定向URL中提取
        if 'goods_sign=' in response.url:
            goods_sign = response.url.split('goods_sign=')[1].split('&')[0]
            if len(goods_sign) >= 28 and len(goods_sign) <= 64:
                print(f"✅ 从重定向URL获取到GoodsSign: {goods_sign}")
                return goods_sign

        print("❌ 无法从页面解析GoodsSign")
    except Exception as e:
        print(f"页面解析异常: {str(e)}")

    return None


def get_product_detail(goods_sign):
    """使用GoodsSign获取商品详情"""
    print('正在获取商品JSON信息')

    # 基础公共参数
    base_params = {
        "client_id": app_key,
        "access_token": access_token,
        "timestamp": str(int(time.time())),
        "data_type": "JSON",
        "version": "v1",
    }
    # 缺少sign参数,这是拼多多的API入参参数签名,签名值根据如下算法给出计算过程.
    # 接口特定参数 - 使用goods_sign
    method_params = {
        "type": "pdd.ddk.goods.detail",
        "goods_sign": goods_sign,
    }

    # 合并参数
    all_params = {**base_params, **method_params}

    # 打印参数用于调试
    print("请求参数:", json.dumps(all_params, indent=2, ensure_ascii=False))

    # 生成签名
    sign = generate_sign(all_params, app_secret)
    all_params["sign"] = sign

    # 发送POST请求
    url = "https://gw-api.pinduoduo.com/api/router"
    try:
        print(f"发送请求到: {url}")
        response = session.post(url, data=all_params)
        print(f"响应状态码: {response.status_code}")

        # 尝试解析JSON
        try:
            json_data = response.json()
            return json_data
        except json.JSONDecodeError:
            print(f"响应内容不是JSON格式: {response.text[:200]}")
            return {"raw_response": response.text}
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return {"error": str(e)}


def save_json_response(data, identifier, save_dir):
    """保存JSON数据到文件"""
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pdd_{identifier}_{timestamp}.json"
    filepath = os.path.join(save_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON保存成功: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ JSON保存失败: {str(e)}")
        return None


def extract_unique_id(goods_sign):
    """提取GoodsSign中的唯一标识符（最后一段）"""
    if '_' in goods_sign:
        parts = goods_sign.split('_')
        if len(parts) > 1:
            return parts[-1]
    return goods_sign


# 主程序
if __name__ == "__main__":
    print(f"开始处理商品ID: {goods_id}")

    # 步骤1: 获取有效的GoodsSign
    goods_sign = get_valid_goods_sign(goods_id)

    if not goods_sign:
        print("❌ 无法获取有效的GoodsSign,程序终止")
        exit()

    # 提取唯一标识符
    unique_id = extract_unique_id(goods_sign)
    print(f"商品唯一标识符: {unique_id}")

    # 步骤2: 使用GoodsSign获取商品详情
    print(f'使用GoodsSign获取商品详情: {goods_sign}')
    product_data = get_product_detail(goods_sign)

    # 保存数据
    if product_data:
        save_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = save_json_response(product_data, unique_id, save_dir)

        # 检查响应
        if "error_response" in product_data:
            error = product_data["error_response"]
            print(f"❌ API错误: {error.get('error_msg', '未知错误')}")
            print(f"子错误: {error.get('sub_msg', '无')}")
            print(f"错误代码: {error.get('error_code', '未知')}")
            print(f"子代码: {error.get('sub_code', '无')}")
            print(f"请求ID: {error.get('request_id', '无')}")
        elif "goods_detail_response" in product_data:
            print("🎉 成功获取商品数据")
            # 尝试提取商品信息
            if "goods_details" in product_data["goods_detail_response"]:
                goods_list = product_data["goods_detail_response"]["goods_details"]
                if goods_list:
                    goods_info = goods_list[0]
                    print(f"商品名称: {goods_info.get('goods_name', '未知')}")
                    print(f"商品价格: {goods_info.get('min_group_price', 0) / 100}元")
                    print(f"已售数量: {goods_info.get('sales_tip', '未知')}")
        else:
            print("⚠️ 未知响应格式，已保存原始数据")
    else:
        print("🚫 未获取到商品数据")
