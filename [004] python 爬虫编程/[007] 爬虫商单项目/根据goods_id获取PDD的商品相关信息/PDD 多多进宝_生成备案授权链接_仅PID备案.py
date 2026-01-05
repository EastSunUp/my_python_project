import requests
import hashlib
import time
import json

app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
access_token = 'd473c080fe3c422189c0d5f5e9a29ea4270377a3'
pid = "43211858_307667234"  # 替换为你的PID # 多多分享ID


def generate_auth_url():
    url = "https://gw-api.pinduoduo.com/api/router"
    timestamp = str(int(time.time()))

    # 关键修改：添加必要参数
    params = {
        "type": "pdd.ddk.rp.prom.url.generate",
        "client_id": app_key,
        "access_token": access_token,
        "timestamp": timestamp,
        "p_id_list": json.dumps([pid]),  # 必须JSON数组格式
        "channel_type": 10,  # 微信场景
        "generate_we_app": True,
        "custom_parameters": json.dumps({"uid": "default"}),  # 必须参数
        "generate_weapp_webview": True  # 新增必要参数
    }

    # 生成签名
    param_str = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    sign_str = f"{app_secret}{param_str}{app_secret}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    params["sign"] = sign

    # 打印请求参数（调试用）
    print("请求参数:", json.dumps(params, indent=2, ensure_ascii=False))

    response = requests.post(url, data=params)
    result = response.json()

    # 打印完整响应（关键调试）
    print("API响应:", json.dumps(result, indent=2, ensure_ascii=False))

    # 处理不同响应格式
    if 'error_response' in result:
        error = result['error_response']
        raise Exception(f"API错误: {error.get('error_msg')} - {error.get('sub_msg')}")

    if 'rp_promotion_url_generate_response' in result:
        url_data = result['rp_promotion_url_generate_response']['url_list'][0]

        # 优先获取微信小程序路径
        if 'we_app_page_path' in url_data:
            return url_data['we_app_page_path']

        # 备用方案：获取普通URL
        if 'url' in url_data:
            return url_data['url']

        # 终极方案：获取短链接
        if 'short_url' in url_data:
            return url_data['short_url']

    raise Exception("无法解析授权链接")


try:
    auth_url = generate_auth_url()
    print("\n成功生成授权链接:")
    print(auth_url)

    # 提供手机访问方案
    print("\n手机访问步骤:")
    print("1. 复制上方链接")
    print("2. 在微信中粘贴打开")
    print("3. 使用拼多多账号登录并确认授权")

except Exception as e:
    print(f"生成失败: {str(e)}")
    print("\n请按以下步骤检查:")
    print("1. 登录开放平台确认应用已开通'微信场景'权限")
    print("2. 确保开发者账号完成企业认证")
    print("3. 尝试使用测试PID: pid = 'test'")