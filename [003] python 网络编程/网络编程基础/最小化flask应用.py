
'''
    flask与公网服务交互的常见场景
    场景	Flask   角色	    实现方式
    提供公网API	服务端	定义路由返回JSON
    爬取公网数据	客户端	使用 requests 库
    第三方登录	中介	    OAuth2 流程处理
    支付回调	    服务端	接收支付平台回调
'''

from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/user/<username>')
def user_profile(username):
    return render_template('profile.html', user=username)


if __name__ == '__main__':
    app.run(debug=True)  # 启动开发服务器
