from flask import Flask, request, jsonify

# 我使用cmd执行python -m http.server 8080,然后刷新花生壳就可以用了
app = Flask(__name__)

# 在代码中添加服务状态检查
@app.route('/')
def service_status():
    return "Flask服务正常运行!", 200

if __name__ == '__main__':
    # 启动前打印提示信息
    print("正在启动Flask服务...")
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
        print("服务启动成功!")
    except Exception as e:
        print(f"服务启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
