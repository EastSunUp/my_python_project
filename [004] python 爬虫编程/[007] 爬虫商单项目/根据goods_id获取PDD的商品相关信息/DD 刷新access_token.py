import requests
import json

app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
refresh_token = '81a91632883744abb756ab4a635e8b2c3d16dc30'  # 替换为您的refresh_token


def refresh_access_token():
    url = "https://open-api.pinduoduo.com/oauth/token"
    payload = {
        'client_id': app_key,
        'client_secret': app_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(url, data=payload)
    result = response.json()

    print("Token刷新响应:", json.dumps(result, indent=2))

    if 'access_token' in result:
        new_access_token = result['access_token']
        new_refresh_token = result['refresh_token']
        print(f"\n新access_token: {new_access_token}")
        print(f"新refresh_token: {new_refresh_token}")

        # 保存新token供后续使用
        with open('pdd_tokens.json', 'w') as f:
            json.dump({
                'access_token': new_access_token,
                'refresh_token': new_refresh_token
            }, f)

        return new_access_token
    else:
        error = result.get('error', '未知错误')
        raise Exception(f"刷新失败: {error}")


# 使用示例
try:
    access_token = refresh_access_token()
    # 更新全局变量
    access_token = access_token
except Exception as e:
    print(str(e))