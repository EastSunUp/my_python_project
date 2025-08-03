
'''
    公网用户 → 云服务器 (公网IP)
                ↓
            [Nginx] (反向代理)
                ↓
            [Gunicorn] (WSGI服务器)
                ↓
            [Flask App] (监听127.0.0.1:8000)
'''
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)


# =====================
# 🛠️ 路由调试工具
# =====================

@app.before_request
def debug_routes():
    """诊断所有传入请求的路由匹配情况"""
    # 获取所有已注册路由
    registered_routes = [rule.rule for rule in app.url_map.iter_rules()
                         if rule.rule != "/static/<path:filename>"]

    # 打印诊断信息
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\n🔍 [{timestamp}] 请求诊断 ================")
    print(f"🌐 客户端: {request.remote_addr}")
    print(f"📡 请求: {request.method} {request.path}")
    print(f"📋 注册路由: {', '.join(registered_routes)}")

    # 检查匹配
    match_found = any(request.path == rule.rule for rule in app.url_map.iter_rules())
    print(f"✅ 路由匹配: {'是' if match_found else '否'}")
    print("=" * 50)


# =====================
# 📡 示例路由
# =====================

@app.route('/')
def home():
    """首页路由"""
    print("🏠 主页路由执行中...")
    # href="/about 这里的意思是,点击这个,就会跳转到对应标签页面所对应的超链接,然后flask会执行这个超链接下对应的路由的函数
    return """
    <h1>Flask 路由诊断系统</h1>
    <p>可用端点:</p>
    <ul>
        <li><a href="/">/ - 首页</a></li>
        <li><a href="/about">/about - 关于页面</a></li>
        <li><a href="/api/data">/api/data - API 示例</a></li>
        <li><a href="/debug">/debug - 路由调试器</a></li>
        <li><a href="/missing">/missing - 缺失路由示例</a></li>
    </ul>
    """


@app.route('/about')
def about():
    """关于页面"""
    print("📖 关于页面路由执行中...")
    return "<h2>关于我们</h2><p>这是一个路由诊断演示应用</p>"


@app.route('/api/data')
def api_data():
    """API 数据端点"""
    print("📊 API 数据路由执行中...")
    return jsonify({"status": "success", "data": [1, 2, 3]})


# =====================
# 🧪 路由诊断面板
# =====================

@app.route('/debug')
def debug_routes():
    """显示所有路由的调试信息"""
    routes_info = []

    # 收集所有路由信息
    for rule in app.url_map.iter_rules():
        if rule.rule == "/static/<path:filename>":
            continue

        # 测试路由状态
        with app.test_client() as client:
            try:
                # 尝试访问路由
                response = client.get(rule.rule)
                status = f"{response.status_code} {response.status}"
            except:
                status = "⚠️ 测试失败（可能需要参数）"

        routes_info.append({
            "path": rule.rule,
            "methods": ", ".join(rule.methods),
            "status": status
        })

    # 生成HTML报告
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 路由诊断报告</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #2c3e50; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            th { background-color: #4CAF50; color: white; }
            .status-200 { color: green; }
            .status-404 { color: red; }
            .status-500 { color: orange; }
        </style>
    </head>
    <body>
        <h1>路由诊断报告</h1>
        <p>当前时间: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>

        <table>
            <tr>
                <th>路径</th>
                <th>支持的HTTP方法</th>
                <th>测试状态</th>
            </tr>
    """

    # 添加路由行
    for route in routes_info:
        status_class = ""
        if "200" in route["status"]:
            status_class = "status-200"
        elif "404" in route["status"]:
            status_class = "status-404"
        elif "500" in route["status"]:
            status_class = "status-500"

        html += f"""
            <tr>
                <td>{route['path']}</td>
                <td>{route['methods']}</td>
                <td class="{status_class}">{route['status']}</td>
            </tr>
        """

    html += """
        </table>

        <h2>如何使用</h2>
        <ol>
            <li>在浏览器中访问任何路由</li>
            <li>查看控制台输出的诊断信息</li>
            <li>检查上表中路由的状态</li>
            <li>红色状态表示路由存在问题</li>
        </ol>

        <h2>常见问题解决方案</h2>
        <ul>
            <li><strong>404 错误</strong>: 检查路由定义是否匹配请求路径</li>
            <li><strong>500 错误</strong>: 查看控制台错误堆栈</li>
            <li><strong>路由未执行</strong>: 确保路由定义在 <code>app.run()</code> 之前</li>
        </ul>
    </body>
    </html>
    """

    return html


# =====================
# 🚀 应用启动与诊断
# =====================

def print_startup_info():
    """打印启动信息"""
    print("\n" + "=" * 60)
    print("🚀 Flask 路由诊断系统已启动")
    print("=" * 60)
    print(f"📡 访问地址: http://localhost:5000")
    print(f"🐞 调试面板: http://localhost:5000/debug")

    # 打印所有注册路由
    print("\n🔧 已注册路由:")
    for rule in app.url_map.iter_rules():
        if rule.rule != "/static/<path:filename>":
            methods = ", ".join(rule.methods)
            print(f"→ {rule.rule} [{methods}]")

    print("\n💡 提示: 所有请求的详细诊断信息将显示在控制台")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    # 打印启动信息
    print_startup_info()

    # 启动服务器
    app.run(debug=True, port=5000)
