import hashlib
import time
import requests
import json
import re
import random

# 配置参数
app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
# access_token = 'd473c080fe3c422189c0d5f5e9a29ea4270377a3'
goods_id = "62262510595"
access_token = '92ff137bb298427abbb66a46696f5c13dfb97c6c'
# Refresh Token: 81a91632883744abb756ab4a635e8b2c3d16dc30
# 新增参数 - 需要替换为你在拼多多备案的实际PID
# 格式: "推广位ID_推广位ID" 例如: "12345_67890"
pid = "43211858_307667234"  # 必须替换

'''
# 新函数：通过生成推广链接获取goods_sign
def generate_promotion_url():
    BASE_URL = "https://gw-api.pinduoduo.com/api/router"
    timestamp = str(int(time.time()))

    # 构造生成推广链接的请求参数
    params = {
        "type": "pdd.ddk.goods.promotion.url.generate",
        "client_id": app_key,
        "access_token": access_token,
        "timestamp": timestamp,
        "p_id": pid,
        "goods_id_list": f'["{goods_id}"]',
        "custom_parameters": json.dumps({"uid": "default"})
    }

    # 生成签名
    param_str = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    sign_str = f"{app_secret}{param_str}{app_secret}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    params["sign"] = sign

    # 发送请求
    response = requests.post(BASE_URL, data=params)
    result = response.json()

    # 调试输出
    print("生成链接API响应:", json.dumps(result, indent=2, ensure_ascii=False))

    # 解析响应获取goods_sign
    if 'goods_promotion_url_generate_response' in result:
        goods_list = result['goods_promotion_url_generate_response']['goods_promotion_url_list']
        if goods_list:
            return goods_list[0]['goods_sign']

    # 错误处理
    if 'error_response' in result:
        error_msg = result['error_response'].get('error_msg', '未知错误')
        sub_msg = result['error_response'].get('sub_msg', '无详细说明')
        raise Exception(f"生成链接API错误: {error_msg} - {sub_msg}")

    raise Exception("无法获取商品推广链接")

'''

def generate_valid_url(goods_id):
    """生成包含商品ID的有效访问链接"""
    # 创建随机UID参数以生成唯一链接
    random_uid = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))

    # 构建商品访问链接
    return f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}&uin={random_uid}"

'''
    def extract_ps_from_url(url):
    """从原始链接中提取ps参数"""
    try:
        # 尝试直接访问链接获取重定向后的URL
        response = requests.head(url, allow_redirects=True)
        final_url = response.url

        # 调试输出
        print(f"初始URL: {url}")
        print(f"重定向后URL: {final_url}")

        # 从重定向URL中提取ps参数
        match = re.search(r'[?&]ps=([^&]+)', final_url)
        if match:
            return match.group(1)

        # 如果未找到ps参数，尝试其他可能的参数
        match = re.search(r'[?&]share_token=([^&]+)', final_url)
        if match:
            return match.group(1)

        raise ValueError("无法从URL中提取有效参数")

    except Exception as e:
        raise ValueError(f"链接访问失败: {str(e)}")

'''

# 步骤1：获取GoodsSign（已修复page_size\已添加PID参数）
def get_goods_sign(url):
    BASE_URL = "https://gw-api.pinduoduo.com/api/router"
    timestamp = str(int(time.time()))
    params = {
        "type": "pdd.ddk.goods.search",
        "client_id": app_key,
        "access_token": access_token,
        "timestamp": timestamp,
        "keyword": url,     # ps_value,    # goods_id,
        "page_size": 100,  # 拼多多要求: 其必须≥10且≤100
        # 新增必须参数
        "pid": pid  ,  # 已备案的推广位ID
        "custom_parameters": json.dumps({"uid": "default"})  # 自定义参数（备案时使用的）
    }

    # 生成签名（保持不变）
    param_str = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    sign_str = f"{app_secret}{param_str}{app_secret}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    params["sign"] = sign

    # 发送请求
    response = requests.post(BASE_URL, data=params)
    result = response.json()

    # 调试输出
    print("API响应:", json.dumps(result, indent=2, ensure_ascii=False))

    # 提取GoodsSign (增加错误详情输出)
    if 'error_response' in result:
        error_msg = result['error_response'].get('error_msg', '未知错误')
        sub_msg = result['error_response'].get('sub_msg', '无详细说明')
        raise Exception(f"API返回错误: {error_msg} - {sub_msg}")

    if 'goods_search_response' in result and result['goods_search_response'].get('goods_list'):
        return result['goods_search_response']['goods_list'][0]['goods_sign']
    raise Exception("未找到商品数据，请检查goods_id有效性")

# 步骤2：获取商品详情
def get_goods_detail(goods_sign):
    BASE_URL = "https://gw-api.pinduoduo.com/api/router"
    timestamp = str(int(time.time()))

    # 构造请求参数
    params = {
        "type": "pdd.ddk.goods.detail",
        "client_id": app_key,
        "access_token": access_token,
        "timestamp": timestamp,
        "goods_sign_list": f'["{goods_sign}"]',
        # 新增必须参数
        "pid": pid  ,  # 已备案的推广位ID
        "custom_parameters": json.dumps({"uid": "default"})  # 自定义参数
    }

    # 生成签名
    param_str = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    sign_str = f"{app_secret}{param_str}{app_secret}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    params["sign"] = sign

    # 发送请求
    response = requests.post(BASE_URL, data=params)
    result = response.json()

    # 解析商品数据
    if 'goods_detail_response' in result:
        return result['goods_detail_response']['goods_details'][0]
    raise Exception("获取商品详情失败：" + json.dumps(result.get('error_response', {})))


# 主程序
if __name__ == "__main__":
    try:
        '''
            print("正在获取GoodsSign...")
            # goods_sign = get_goods_sign()
            goods_sign = generate_promotion_url()
            print(f"成功获取GoodsSign: {goods_sign}")
        '''

        # 步骤1: 生成有效商品链接
        print("生成有效商品访问链接...")
        generated_url = generate_valid_url(goods_id)
        print(f"生成的商品链接: {generated_url}")

        '''
            # 步骤2: 从链接中提取有效参数
            print("\n从链接中提取有效参数...")
            url_param = extract_ps_from_url(generated_url)
            print(f"提取的有效参数: {url_param}")
        '''
        # 步骤3: 使用参数获取GoodsSign
        print(f"\n使用参数获取商品ID为{goods_id}的GoodsSign...")
        goods_sign = get_goods_sign(url=generated_url)
        print(f"成功获取GoodsSign: {goods_sign}")

        print("\n正在获取商品详情...")
        goods_detail = get_goods_detail(goods_sign)
        print(f"商品标题: {goods_detail['goods_name']}")

        # # 提取关键信息
        # print("\n商品信息:")
        # print(f"标题: {goods_detail['goods_name']}")
        # print(f"店铺名: {goods_detail['mall_name']}")
        # print(f"原价: {goods_detail['min_group_price'] / 100}元")
        # print(f"店铺ID: {goods_detail['mall_id']}")
        # print(f"商品ID: {goods_detail['goods_id']}")
        #
        # # 输出完整数据
        # print("\n完整商品数据:")
        # print(json.dumps(goods_detail, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"程序出错: {str(e)}")
