import requests
import json
import webbrowser
from urllib.parse import urlencode
from flask import Flask, request, jsonify
import threading
import hashlib
import time

# ====== 配置区域 ====== (请修改以下参数)
CLIENT_ID = "237bfc3d5f4d472b93b2dcb44439dff8"  # 替换为你的应用Client ID
PID = "43211858_307667234"  # 替换为你的推广位PID (格式: xxxxx_xxxxx)
REDIRECT_URI = "https://11nqpe1304236.vicp.fun/pdd_callback"  # 替换为你的回调地址
# 我的花生壳回调地址: https://11nqpe1304236.vicp.fun/pdd_callback
CLIENT_SECRET = "9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5"
# access_token ="7df56a56bc7642e8870a7ce2c5258d565a135cbe"
# 使用flask服务对应的代码端
app = Flask(__name__)

# 在代码中添加服务状态检查
@app.route('/')
def service_status():
    return jsonify({
        "status": "running",
        "service": "PDD Callback Handler",
        "endpoints": {
            "health": "/",
            "callback": "/pdd_callback"
        }
    }), 200

@app.route('/get_token')
def get_token():
    """获取当前存储的PID授权token"""
    global PID_ACCESS_TOKEN
    if PID_ACCESS_TOKEN:
        return jsonify({
            "access_token": PID_ACCESS_TOKEN,
            "status": "success"
        }), 200
    return jsonify({
        "error": "尚未获取PID授权token",
        "status": "not_found"
    }), 404

@app.route('/pdd_callback')
def pdd_callback():
    """
    处理拼多多授权回调
    """
    # 全局参数: PID_ACCESS_TOKEN
    global PID_ACCESS_TOKEN

    # 获取授权码
    auth_code = request.args.get('code')
    state = request.args.get('state')
    pid = request.args.get('pid')  # 从回调参数获取PID

    if not auth_code:
        return jsonify({"error": "缺少授权码参数"}), 400
    print(f"收到回调: code={auth_code}, pid={pid}, state={state}")

    # ---------------在获取授权码之后进行授权操作--------------------------------

    # 1. 使用授权码获取access_token
    token_url = "https://open-api.pinduoduo.com/oauth/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }

    # 使用JSON格式提交请求,手动构建JSON确保格式正确
    json_data = json.dumps(token_data, separators=(',', ':'))
    headers = {"Content-Type": "application/json"}

    try:
        print("正在获取access_token...")
        token_resp = requests.post(token_url, data=json_data, headers=headers)
        token_result = token_resp.json()

        # 打印调试信息
        print("Token接口响应:", token_result)
        # print("Token接口响应(API响应):", json.dumps(token_result, indent=2, ensure_ascii=False))

        # 调试输出
        print(f"Token请求状态: {token_resp.status_code}")
        print(f"Token响应内容: {json.dumps(token_result, indent=2)}")

        # 检查错误
        if "error_response" in token_result:
            error_msg = token_result["error_response"].get("error_msg", "未知错误")
            return f"<h1>获取Token失败</h1><p>{error_msg}</p>", 400

        # 检查是否成功获取access_token
        if "access_token" not in token_result:
            return "<h1>获取Token失败</h1><p>响应中未包含access_token</p>", 400

        access_token = token_result["access_token"]
        print(f"✅ 成功获取Access Token: {access_token}")

        # 保存token用于后续查询
        PID_ACCESS_TOKEN = access_token
    except Exception as e:
        error_msg = f"获取Token时发生异常: {str(e)}"
        print(error_msg)
        return f"<h1>Token请求失败</h1><p>{error_msg}</p>", 500

    # 2. 调用PID备案接口
    TIMESTAMP = str(int(time.time()))
    authority_params = {
        "type": "pdd.ddk.member.authority.add",
        "client_id": CLIENT_ID,
        "access_token": access_token,
        "timestamp": TIMESTAMP,
        "pid": pid,
        "custom_parameters":None
    }

    # 生成签名
    param_str = ''.join(f'{k}{v}' for k, v in sorted(authority_params.items()))
    sign_str = f"{CLIENT_SECRET}{param_str}{CLIENT_SECRET}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    authority_params["sign"] = sign

    try:
        # 调用备案接口
        auth_resp = requests.post(
            "https://gw-api.pinduoduo.com/api/router",
            data=authority_params
        )
        auth_result = auth_resp.json()

        # 调试输出
        print("备案接口响应:", auth_result)
        print(f"备案请求状态: {auth_resp.status_code}")
        print(f"备案响应内容: {json.dumps(auth_result, indent=2)}")

        # 3. 处理备案结果
        if "error_response" in auth_result:
            error_msg = auth_result["error_response"].get("error_msg", "备案失败")
            return f"""
                    <html>
                        <head><title>备案失败</title></head>
                        <body style="font-family: Arial; text-align: center; padding: 50px;">
                            <h1 style="color: red;">❌ 备案失败</h1>
                            <p>错误信息: {error_msg}</p>
                            <p>PID: {pid}</p>
                        </body>
                    </html>
                    """

        # 返回成功响应
        return f"""
            <html>
                <head><title>授权成功</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: #4CAF50;">🎉 授权成功!</h1>
                    <p>授权码: <code>{auth_code}</code></p>
                    <p>状态值: <code>{state}</code></p>
                    <p>请关闭此页面并返回应用程序</p>
                </body>
            </html>
            """
    except Exception as e:
        error_msg = f"备案请求时发生异常: {str(e)}"
        print(error_msg)
        return f"<h1>备案请求失败</h1><p>{error_msg}</p>", 500

def run_server():
    """运行服务器的主函数"""
    # 启动flask服务,启动前打印提示信息
    print("正在启动Flask服务...")
    try:
        print("服务器正在运行...")
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
        # app.run(host='0.0.0.0', port=8080, debug=True)
        print("服务启动成功!")
    except Exception as e:
        print(f"服务启动失败: {str(e)}")
        import traceback
        traceback.print_exc()

def run_flask_in_thread():
    # 单开一个线程运行flask
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    print("Flask服务线程已启动 !")
    server_thread.start()


# ------------------------以下为生成授权链接等部分-------------------------------------------
def generate_pid_auth_link(client_id, pid, redirect_uri, custom_params=None):
    """
    生成多多进宝PID电脑端备案授权链接
    :param client_id: 开放平台应用Client ID
    :param pid: 推广位PID (格式: xxxxx_xxxxx)
    :param redirect_uri: 回调地址
    :param custom_params: 自定义参数 (可选字典)
    :return: 电脑端授权链接
    """
    # 基础参数设置
    base_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": "pdd_pid_auth",
        "view": "web",  # 强制使用电脑端视图
        "pid": pid
    }

    # 添加自定义参数（如果提供）
    if custom_params:
        base_params["custom_parameters"] = json.dumps(custom_params)

    # 构造授权链接
    auth_url = f"https://jinbao.pinduoduo.com/open.html?{urlencode(base_params)}"

    return auth_url


def check_pid_auth(pid, access_token=None):
    """
    查询PID备案状态
    :param pid: 要查询的PID
    :param access_token: 使用PID授权流程获取的token
    """
    if not access_token:
        print("错误: 需要提供access_token")
        return

    url = "https://gw-api.pinduoduo.com/api/router"
    timestamp = str(int(time.time()))

    params = {
        "type": "pdd.ddk.member.authority.query",
        "client_id": CLIENT_ID,
        "access_token": access_token,
        "timestamp": timestamp,
        "pid": pid
    }

    # 生成签名
    param_str = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    sign_str = f"{CLIENT_SECRET}{param_str}{CLIENT_SECRET}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    params["sign"] = sign

    try:
        response = requests.post(url, data=params)
        result = response.json()

        print(f"\nPID: {pid} 备案状态查询结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if "authority_query_response" in result:
            auth_info = result["authority_query_response"]
            status = "已备案" if auth_info.get("bind", 0) == 1 else "未备案"
            print(f"备案状态: {status}")
            return auth_info
        else:
            print("查询失败:", result.get("error_response", {}))
            return None

    except Exception as e:
        print(f"查询时发生错误: {str(e)}")
        return None

def main():

    # 可选: 自定义参数 (用于标识推手)
    # 格式: {"uid": "12345", "source": "website"}
    CUSTOM_PARAMS = None

    # ====== 生成授权链接 ======
    auth_link = generate_pid_auth_link(
        client_id=CLIENT_ID,
        pid=PID,
        redirect_uri=REDIRECT_URI,
        custom_params=CUSTOM_PARAMS
    )

    # ====== 控制台输出结果 ======
    print("\n" + "=" * 60)
    print("多多进宝PID备案授权链接生成结果")
    print("=" * 60)
    print(f"\n💻 电脑端授权链接:")
    print(auth_link)

    print("\n" + "-" * 60)
    print("操作说明:")
    print("1. 将此链接复制到电脑浏览器中打开")
    print("2. 使用已实名认证的多多进宝账号登录")
    print("3. 确认授权完成PID备案")
    print("=" * 60)

    # 可选：自动在浏览器中打开链接
    open_in_browser = input("\n是否要在浏览器中打开此授权链接? (y/n): ").lower()
    if open_in_browser == 'y':
        webbrowser.open(auth_link)
        print("已在浏览器中打开授权链接...")


if __name__ == "__main__":
    run_flask_in_thread()
    main()

    # 等待用户完成授权
    print("\n等待授权回调...")
    print("完成授权后，可以按Ctrl+C停止程序")

    try:
        while True:
            # 每10秒检查一次是否获取到token
            time.sleep(10)

            if PID_ACCESS_TOKEN:
                print(f"\n获取到PID授权token: {PID_ACCESS_TOKEN}")

                # 查询备案状态
                print("\n正在查询备案状态...")
                auth_info = check_pid_auth(PID, PID_ACCESS_TOKEN)

                if auth_info and auth_info.get("bind") == 1:
                    print("✅ PID备案成功!")
                else:
                    print("❌ PID备案未成功，请检查错误信息")

                # 提供API端点查看token
                print(f"\n您可以通过以下URL获取token: http://localhost:8080/get_token")

                # 退出等待循环
                break

    except KeyboardInterrupt:
        print("\n程序已终止")
