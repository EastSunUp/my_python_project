
from flask import Flask, request

'''
    在使用本代码前需要确定使用的是空闲端口,
    请在使用前先检查电脑空闲端口.
'''
# pdd_callback
# client_id 237bfc3d5f4d472b93b2dcb44439dff8
# client_secret 9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5
# 我的回调地址:http://localhost:8080/pdd_callback
# 花生壳中转网址:https://11nqpe1304236.vicp.fun/pdd_callback   # 2025/07/18 (2:26)
# 内网主机:127.0.0.1    端口: 8080
# 用于生成获取电商网站开发者API授权code获取时的中转网址(然后转发到本地)
app = Flask(__name__)
# 重点配置 👇 端口=8080, 路径=/pdd_callback
@app.route('/pdd_callback')  # 这里定义路径
def callback():
    # auth_code指的是授权码
    auth_code = request.args.get('code')
    # 验证state参数防止CSRF攻击
    returned_state = request.args.get('state')
    original_state = "random_security_token_123"  # 应从会话中获取原始state
    if returned_state != original_state:
        return "安全验证失败", 403

    if not auth_code:
        return "未收到授权码", 400

    print(f"成功获取授权码: {auth_code}")
    return "授权完成!请关闭窗口."

if __name__ == '__main__':
    # 这里设置端口号
    app.run(port=8080, debug=True)  # 端口设为8080

