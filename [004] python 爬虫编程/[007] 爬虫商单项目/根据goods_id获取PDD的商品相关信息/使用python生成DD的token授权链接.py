
import urllib.parse

def generate_auth_url(app_key, redirect_uri, state=None):
    """
    生成拼多多授权URL

    参数:
        app_key (str): 应用Key
        redirect_uri (str): 授权回调地址(需在拼多多后台配置)
        state (str, 可选): 状态参数(用于防CSRF攻击)

    返回:
        str: 完整的授权URL
    """
    base_url = "https://fuwu.pinduoduo.com/service-market/auth"

    params = {
        "response_type": "code",
        "client_id": app_key,
        "redirect_uri": redirect_uri
    }

    if state:
        params["state"] = state

    return f"{base_url}?{urllib.parse.urlencode(params)}"

# 使用示例
app_key = "237bfc3d5f4d472b93b2dcb44439dff8"
redirect_uri = "http://localhost:8080/pdd_callback"  # 必须与开放平台配置一致
state = "random_security_token_123"  # 建议使用随机字符串增强安全性

auth_url = generate_auth_url(app_key, redirect_uri, state)
print("请访问以下URL进行授权:")
print(auth_url)
