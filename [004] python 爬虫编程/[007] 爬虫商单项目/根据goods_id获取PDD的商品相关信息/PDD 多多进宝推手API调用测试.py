import requests
import hashlib
import time

# 开发者凭证（从开放平台获取）
app_key = "237bfc3d5f4d472b93b2dcb44439dff8"  # 替换为实际值
app_secret = "9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5"

# 商品标识 (支持goods_id或goods_sign)
goods_sign = "62262510595"  # 示例商品标识

# 生成签名 (拼多多要求MD5加密)
def generate_sign(params, app_secret):
    param_str = ''.join([f'{k}{v}' for k, v in sorted(params.items())])
    sign_str = app_secret + param_str + app_secret
    return hashlib.md5(sign_str.encode()).hexdigest().upper()

# 构造基础参数
params = {
    "type": "pdd.ddk.goods.detail",  # 接口名
    "client_id": app_key,
    "timestamp": str(int(time.time())),  # 当前时间戳
    "data_type": "JSON",
    "goods_sign_list": f'["{goods_sign}"]'  # 支持批量查询
}

# 添加签名
params["sign"] = generate_sign(params, app_secret)

# ----------------------发送请求并解析JSON响应-----------------------------------------------------------------
url = "https://gw-api.pinduoduo.com/api/router"

try:
    response = requests.get(url, params=params)
    result = response.json()

    # 检查错误
    if "error_response" in result:
        error = result["error_response"]
        print(f"API调用失败！错误码: {error['error_code']}, 原因: {error['error_msg']}")
    else:
        goods_info = result["goods_detail_response"]["goods_details"][0]
        print("商品标题:", goods_info["goods_name"])
        print("价格:", goods_info["min_group_price"] / 100)  # 单位分转元
        print("销量:", goods_info["sales_tip"])
        print("商品ID:", goods_info["goods_id"])
        # 更多字段：coupon_discount, image_url, cat_id 等:cite[8]

except Exception as e:
    print(f"请求异常: {e}")