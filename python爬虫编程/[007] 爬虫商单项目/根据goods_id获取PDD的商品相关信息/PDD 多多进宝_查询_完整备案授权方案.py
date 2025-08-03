import requests
import hashlib
import time
import json
import webbrowser

# 配置信息
app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
access_token = '92ff137bb298427abbb66a46696f5c13dfb97c6c'
pids = ["43202677_307657811", "43202677_307597861"]  # 您的推广位ID
redirect_uri = "https://11nqpe1304236.vicp.fun/pdd_callback"  # 您的回调地址


def generate_sign(params, app_secret):
    """生成API签名"""
    param_str = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    sign_str = f"{app_secret}{param_str}{app_secret}"
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()


def get_developer_mobile():
    """获取开发者绑定手机号（替代方法）"""
    print("请手动获取开发者绑定手机号：")
    print("1. 登录 https://open.pinduoduo.com")
    print("2. 点击右上角账号 → 账号设置 → 基本信息")
    print("3. 查看'联系手机'字段")
    return input("请输入您的开发者绑定手机号: ").strip()


def generate_auth_link(pid, mobile):
    """生成人工授权链接"""
    return (
        f"https://jinbao.pinduoduo.com/open.html?"
        f"client_id={app_key}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"state={pid}_{mobile}"
    )


def check_pid_auth(pid, retries=5, delay=30):
    """检查PID备案状态（带重试机制）"""
    print(f"\n正在检查 PID {pid} 的备案状态...")

    for i in range(retries):
        url = "https://gw-api.pinduoduo.com/api/router"
        timestamp = str(int(time.time()))

        params = {
            "type": "pdd.ddk.member.authority.query",
            "client_id": app_key,
            "access_token": access_token,
            "timestamp": timestamp,
            "pid": pid
        }

        # 生成签名
        params["sign"] = generate_sign(params, app_secret)

        try:
            response = requests.post(url, data=params, timeout=10)
            result = response.json()

            print(f"尝试 {i + 1}/{retries} - 响应: {json.dumps(result, ensure_ascii=False)}")

            if "authority_query_response" in result:
                auth_info = result["authority_query_response"]
                if auth_info.get("bind") == 1:
                    print(f"✅ PID {pid} 已成功备案!")
                    return True
        except Exception as e:
            print(f"查询出错: {str(e)}")

        if i < retries - 1:
            print(f"等待 {delay} 秒后重试...")
            time.sleep(delay)

    print(f"❌ PID {pid} 备案状态检查失败")
    return False


def main():
    print("=" * 50)
    print("拼多多PID备案解决方案")
    print("=" * 50)

    # 1. 获取开发者绑定手机号
    mobile = get_developer_mobile()
    print(f"\n开发者绑定手机号: {mobile}")

    # 2. 为每个PID执行备案流程
    for pid in pids:
        print("\n" + "=" * 50)
        print(f"处理 PID: {pid}")
        print("=" * 50)

        # 生成授权链接
        auth_link = generate_auth_link(pid, mobile)
        print(f"授权链接已生成: {auth_link}")

        # 自动打开浏览器（可选）
        open_browser = input("是否自动在浏览器中打开链接? (y/n): ").lower()
        if open_browser == 'y':
            webbrowser.open(auth_link)

        print("\n请按以下步骤完成授权:")
        print("1. 复制上方链接")
        print("2. 在微信中粘贴打开")
        print("3. 使用开发者绑定手机号登录拼多多")
        print("4. 完成授权确认")
        input("完成授权后，按回车键继续...")

        # 检查备案状态
        if check_pid_auth(pid):
            print(f"🎉 PID {pid} 备案成功!")
        else:
            print(f"⚠️ PID {pid} 备案未确认，请检查:")
            print("- 是否使用正确手机号登录?")
            print("- 是否完成最后一步授权确认?")
            print("- 稍后可在拼多多联盟后台查看备案状态")

    print("\n" + "=" * 50)
    print("所有PID处理完成！下一步:")
    print("1. 登录拼多多联盟后台 https://jinbao.pinduoduo.com")
    print("2. 进入'推广管理' → '推广位管理'")
    print("3. 确认PID的'备案状态'")
    print("=" * 50)


if __name__ == "__main__":
    main()