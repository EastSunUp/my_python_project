from flask import Flask, request, jsonify
import webbrowser
import time
import threading
import requests
import json

app = Flask(__name__)

# 存储授权码的变量
authorization_code = None


@app.route('/pdd_callback', methods=['GET'])
def handle_callback():
    global authorization_code
    print(f"收到回调请求: {request.url}")

    # 获取拼多多返回的授权code
    auth_code = request.args.get('code')
    state = request.args.get('state')

    if auth_code:
        print(f"✅ 成功获取授权码: {auth_code}")
        authorization_code = auth_code
        return jsonify({"code": 0, "msg": "success"})
    else:
        print("❌ 未收到授权码")
        return jsonify({"code": 1, "msg": "Missing code parameter"}), 400


def run_flask_app():
    app.run(host='127.0.0.1', port=8080)


def get_authorization_url():
    """使用已验证有效的URL格式构造授权链接"""
    base_url = "https://mai.pinduoduo.com/h5-login.html"

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }

    # 构建查询字符串
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}?{query_string}"


if __name__ == '__main__':
    # 配置你的应用信息
    CLIENT_ID = "237bfc3d5f4d472b93b2dcb44439dff8"  # 替换为你的实际值
    CLIENT_SECRET = "9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5"  # 替换为你的实际值
    REDIRECT_URI = "https://11kt13019bi96.vicp.fun/pdd_callback"

    # 启动Flask服务（在后台线程中运行）
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    print("Flask服务已启动：http://127.0.0.1:8080")
    print("等待花生壳映射生效...")
    time.sleep(5)  # 给花生壳一点时间

    # 构造正确的授权链接
    auth_url = get_authorization_url()
    print("生成的授权链接:", auth_url)

    print("打开浏览器进行授权...")
    webbrowser.open(auth_url)

    # 等待用户完成授权
    print("等待授权回调（最长等待10分钟）...")
    start_time = time.time()
    while authorization_code is None and (time.time() - start_time < 600):
        time.sleep(1)

    if authorization_code:
        print(f"✅ 成功获取授权码: {authorization_code}")

        # 使用code换取access_token
        print("开始换取access_token...")

        token_url = "https://open-api.pinduoduo.com/oauth/token"    # access_token授权链接
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()  # 检查HTTP错误

            token_data = response.json()

            # 检查API返回的错误
            if "error_code" in token_data:
                print(f"❌ 换取令牌失败: {token_data['error_msg']}")
                print(f"错误代码: {token_data['error_code']}")
            else:
                print("\n✅ 成功获取访问令牌(access_token)!")
                print(f"Access Token: {token_data['access_token']}")
                print(f"Refresh Token: {token_data['refresh_token']}")
                print(f"有效期: {token_data['expires_in']}秒")

                # 保存token到文件或数据库
                with open("pdd_tokens.json", "w") as f:
                    json.dump(token_data, f, indent=2)

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {str(e)}")
        except ValueError:
            print("❌ 响应解析失败,返回内容:", response.text)
    else:
        print("❌ 超时未收到授权码")

    print("程序执行完毕")

