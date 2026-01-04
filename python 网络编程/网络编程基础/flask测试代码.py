from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# TODO 这段代码不完善,需要修改其中部分内容
@app.route('/')
def home():
    return "Flask 服务器正常运行! <a href='/pdd_callback?test=123'>测试回调</a>"

# @test_app.route('/test')
# def test_route():
#     return "测试路由被调用!"

@app.route('/pdd_callback')
def pdd_callback():
    params = request.args.to_dict()
    print(f"\n收到回调请求: {params}")
    return jsonify({
        "status": "success",
        "message": "回调处理成功",
        "received_params": params
    })


def run_server():
    """运行服务器的主函数"""
    print("服务器正在运行...")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)


if __name__ == '__main__':
    # 显示注册的路由
    print("可用路由:")
    for rule in app.url_map.iter_rules():
        print(f" - {rule}")

    # 创建新应用实例
    test_app = Flask(__name__)

    # @test_app.route('/')
    # def test_home():
    #     return "测试应用已启动!"

    print("\n运行测试应用...")
    test_app.run(host='0.0.0.0', port=5000, debug=True)

    # 启动服务器线程
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    # http://localhost:5000
