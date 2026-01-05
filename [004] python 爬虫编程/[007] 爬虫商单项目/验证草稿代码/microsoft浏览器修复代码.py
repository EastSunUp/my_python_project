from flask import Flask, make_response
import os

app = Flask(__name__)


# 模拟用户登录路由
@app.route('/login')
def login():
    # 创建响应对象
    response = make_response("登录成功！Cookie 已设置")

    # 设置安全 Cookie - 关键修复点
    response.set_cookie(
        'session_token',  # Cookie 名称
        'encrypted_session_data',  # Cookie 值 (实际应用中应加密)
        secure=True,  # 启用 Secure 标记 ✔️
        httponly=True,  # 推荐同时启用 HttpOnly
        samesite='Lax',  # 推荐设置 SameSite 策略
        max_age=3600  # 过期时间 (1小时)
    )

    return response


# 需要认证的路由
@app.route('/dashboard')
def dashboard():
    # 实际应用中这里会验证 cookie
    return "欢迎访问仪表盘！您的 Cookie 安全设置正确。"


if __name__ == '__main__':
    # 生产环境应使用真实证书
    ssl_context = ('server.crt', 'server.key') if os.path.exists('server.crt') else 'adhoc'

    # 启动 HTTPS 服务器（Secure Cookie 需要 HTTPS）
    app.run(
        ssl_context=ssl_context,  # 启用 HTTPS
        host='0.0.0.0',
        port=443,
        debug=True
    )