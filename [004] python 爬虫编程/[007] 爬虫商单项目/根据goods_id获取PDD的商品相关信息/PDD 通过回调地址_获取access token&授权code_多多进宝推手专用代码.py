
'''
    +-----------------------+      (1) 构造授权链接 auth_url        +-----------------------+
    |                       |  (含 client_id, scope, redirect_uri) |                       |
    |  你的 Python 程序       | -----------------------------------> |       你的浏览器        |
    |  (包含 client_id,      | <----------------------------------- |                       |
    |   client_secret)      |      (2) webbrowser.open(auth_url)   +-----------------------+
    +-----------------------+                                        |
              ^   |                                                  | (3) 导航到拼多多授权页面
              |   | (6) 启动 Flask 服务器 (run_server)               |
              |   v                                                  v
    +-----------------------+                             +-----------------------+
    |                       |                             |                       |
    |   Flask App 运行中     |                             |   拼多多授权服务器       |
    |  (监听 0.0.0.0:8080)  |                             | (用户在此登录并同意授权) |
    |  定义路由 /callback    |                             |                       |
    +-----------------------+                             +-----------------------+
              ^   |                                                  |
              |   |                                                  | (4) 用户同意授权
              |   | (7) 处理回调 & 换取 token                        |
              |   v                                                  v
    +-----------------------+      (5) 回调请求 (GET)                +-----------------------+
    |                       | <--- http://花生壳域名/callback?code=XXX --- |                       |
    |      花生壳服务         |                                          |  拼多多授权服务器       |
    | (公网域名 -> localhost:8080)| -----------------------------------> | (发起回调请求)         |
    |                       |      (8) 转发请求到 localhost:8080       +-----------------------+
    +-----------------------+                                        |
                                                                     | (9) 请求到达
                                                                     v
    +-----------------------+
    |                       | <--- GET /callback?code=XXX ----------+
    |     Flask App         |                                         |
    |   (localhost:8080)    |                                         |
    |                       | ---> @app.route('/callback') 函数执行:   |
    |                       |     a. 提取 request.args.get('code')    |
    |                       |     b. 用 code, client_id, client_secret|
    |                       |        请求拼多多 token 端点换 access_token |
    |                       |     c. 存储 token                       |
    |                       |     d. 返回响应 (e.g., "Success")       |
    +-----------------------+                                         |
              ^                                                      |
              | (10) 响应 (e.g., "Success")                          |
              |                                                      |
    +-----------------------+      (11) 响应                          +-----------------------+
    |      花生壳服务         | <---------------------------------------- |                       |
    |                       |                                          |  拼多多授权服务器       |
    |                       |                                          | (收到回调响应)         |
    +-----------------------+                                          +-----------------------+
'''
'''
    [公网] <---------------------- 花生壳 (桥梁) ----------------------> [你的本地开发机]
     ^                                   |                               ^
     | (5,11) 回调请求 & 响应             | (7,8) 转发请求/响应             | (6) 运行监听
     |                                   v                               |
     +------------------------> [Flask @ /callback] <--------------------+
                                   |          ^
                                   | (10)     | (9) 提取 code, 换取 token
                                   v          |
                               [你的业务逻辑代码]
'''
from flask import Flask, request, jsonify
import requests
import threading
import webbrowser
import time
import os
import sys

# 创建Flask应用实例
app = Flask(__name__)

# ====== 配置区域 ======
CLIENT_ID = "237bfc3d5f4d472b93b2dcb44439dff8"
CLIENT_SECRET = "9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5"
# 拼多多开发者的回调地址
CALLBACK_URL = "https://11nqpe1304236.vicp.fun/pdd_callback"    # 开发者平台设置的网址(url)   #花生壳生成
SERVER_PORT = 8080

# 拼多多API地址
PDD_AUTH_URL = "http://jinbao.pinduoduo.com/open.html"
PDD_TOKEN_URL = "http://open-api.pinduoduo.com/oauth/token" # 授权地址
# =====================

# 添加路由前的诊断信息
print("=" * 50)
print("在添加路由前的路由表:")
for rule in app.url_map.iter_rules():
    print(f" - {rule}")
print("=" * 50)

@app.route('/')
def home():
    """根路由处理函数"""
    print("\n[home] 被调用!")
    return f"""
    <h1>PDD OAuth服务已启动!</h1>
    <p>回调端点: <code>{CALLBACK_URL}</code></p>
    <p><a href="/pdd_callback?test=123">本地测试</a></p>
    <p><a href="{CALLBACK_URL}?test=456">花生壳测试</a></p>
    <p>当前时间: {time.ctime()}</p>
    """


@app.route('/pdd_callback')
def handle_callback():
    """回调路由处理函数"""
    print("\n[handle_callback] 被调用!")
    print(f"请求方法: {request.method}")
    print(f"请求路径: {request.path}")
    print(f"请求参数: {request.args}")
    print(f"请求头: {request.headers}")

    # 检查授权码
    code = request.args.get('code')
    if not code:
        return jsonify({
            "status": "error",
            "message": "缺少授权码参数",
            "received_params": dict(request.args),
            "headers": dict(request.headers)
        }), 400

    print(f"✅ 获取到授权码: {code}")

    # 获取access_token
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": CALLBACK_URL
    }

    try:
        print("正在请求access_token...")
        response = requests.post(PDD_TOKEN_URL, json=token_data)
        print(f"Token响应状态码: {response.status_code}")
        print(f"Token响应内容: {response.text}")

        result = response.json()

        if 'error' in result:
            error_msg = result.get('error_description', '未知错误')
            print(f"❌ 获取token失败: {error_msg}")
            return jsonify({
                "status": "error",
                "message": f"获取token失败: {error_msg}",
                "response": result
            }), 400

        # 提取凭证
        access_token = result['access_token']
        refresh_token = result['refresh_token']
        expires_in = result['expires_in']

        print("\n======= 授权成功! =======")
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print(f"有效期: {expires_in}秒")
        print("========================")

        return "授权成功! 你可以关闭此页面"

    except Exception as e:
        print(f"服务器错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"服务器错误: {str(e)}",
            "exception_type": type(e).__name__
        }), 500


# 添加路由后的诊断信息
print("=" * 50)
print("在添加路由后的路由表:")
for rule in app.url_map.iter_rules():
    print(f" - {rule}")
print("=" * 50)


def run_server():
    """运行服务器的主函数"""
    print(f"\n{'=' * 50}")
    print(f"启动Flask服务器在端口 {SERVER_PORT}...")
    print(f"访问地址: http://127.0.0.1:{SERVER_PORT}")
    print(f"访问地址: http://{get_local_ip()}:{SERVER_PORT}")
    print(f"花生壳地址: {CALLBACK_URL}")
    print(f"{'=' * 50}\n")

    # 使用HTTP运行(启动flask服务器,监听8080端口发来的信息)
    app.run(
        host='0.0.0.0',
        port=SERVER_PORT,
        debug=False,
        use_reloader=False
    )


def get_auth_url():
    """生成授权链接"""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": CALLBACK_URL,
        "state": "pdd_auth"
    }
    return f"{PDD_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"


def get_local_ip():
    """获取本机IP地址"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"
# 237bfc3d5f4d472b93b2dcb44439dff8
# https://11nqpe1304236.vicp.fun/pdd_callback

if __name__ == '__main__':
    # 打印诊断信息
    print("\n" + "=" * 50)
    print("程序启动配置:")
    print(f"回调地址: {CALLBACK_URL}")
    print(f"本地端口: {SERVER_PORT}")
    print(f"本地IP: {get_local_ip()}")
    print("=" * 50)

    # 生成授权链接
    auth_url = get_auth_url()
    print(f"\n请访问此链接进行授权:\n{auth_url}")

    # 自动打开浏览器
    webbrowser.open(auth_url)

    # 直接运行服务器（不再使用线程）
    run_server()    # 这行代码的意思是启动flask服务器
