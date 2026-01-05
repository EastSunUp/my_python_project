import requests
import hashlib
import time
import json

app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
access_token = '7df56a56bc7642e8870a7ce2c5258d565a135cbe'
# 92ff137bb298427abbb66a46696f5c13dfb97c6c # 原access_token码
# 多多分享PID码: 43211858_307667234

def check_pid_auth(pid):
    url = "https://gw-api.pinduoduo.com/api/router"
    timestamp = str(int(time.time()))  # 确保为字符串类型

    # 准备请求参数（过滤空值）
    params = {
        "type": "pdd.ddk.member.authority.query",
        "client_id": app_key,
        # "access_token": access_token, # 这是一个公开接口,这个接口不需要access_token,
        "timestamp": timestamp,
        "pid": pid,
        "custom_parameters": json.dumps({"uid": "default"})
    }
    # 移除值为None或空字符串的参数
    sign_params = {k: str(v) for k, v in params.items() if v not in [None, ""]}

    # 生成签名（关键修正）
    param_str = ''.join(f'{k}{v}' for k, v in sorted(sign_params.items()))
    sign_str = f"{app_secret}{param_str}{app_secret}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

    # 添加签名到请求参数
    params["sign"] = sign

    # 发送请求（使用JSON格式）
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=params, headers=headers)

    try:
        result = response.json()
        print(f"{pid}的API响应信息:\n", json.dumps(result, indent=2, ensure_ascii=False))

        # 解析备案信息
        if "authority_query_response" in result:
            auth_info = result["authority_query_response"]
            print(f"\nPID备案状态: {'已备案' if auth_info['bind'] else '未备案'}")
            if "custom_parameters" in auth_info:
                print(f"自定义参数: {auth_info['custom_parameters']}")
        else:
            print("查询失败:", result.get("error_response", {}))

    except json.JSONDecodeError:
        print("响应解析失败，原始内容:", response.text)


# 测试查询
check_pid_auth("43211858_307667234")
