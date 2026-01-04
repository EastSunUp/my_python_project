
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl, Property, Signal


class WebPageHandler(QObject):
    """处理与JavaScript通信的类"""

    # 定义一个信号用于发送数据到JavaScript
    dataChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._data = ""

    @Slot(str)
    def js_message(self, msg):
        """接收来自JavaScript的消息"""
        print(f"JavaScript说: {msg}")

    @Slot(str, result=str)
    def get_python_data(self, request):
        """返回数据给JavaScript"""
        response = f"Python数据: {request}"
        print(f"收到JavaScript请求: {request}，返回: {response}")
        return response

    @Slot(str)
    def set_data(self, value):
        """设置数据（可以被JavaScript调用）"""
        if self._data != value:
            self._data = value
            self.dataChanged.emit(value)

    @Slot(result=str)
    def get_data(self):
        """获取数据（可以被JavaScript调用）"""
        return self._data

    # 为数据属性创建getter和setter
    data = Property(str, get_data, set_data, notify=dataChanged)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 WebEngine示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建WebView
        self.webView = QWebEngineView(self)
        self.setCentralWidget(self.webView)

        # 设置WebChannel
        self.channel = QWebChannel()
        self.handler = WebPageHandler()

        # 注册对象, JavaScript中可以通过这个名称访问
        self.channel.registerObject("handler", self.handler)
        self.webView.page().setWebChannel(self.channel)

        # 连接加载完成信号
        self.webView.loadFinished.connect(self.on_loaded)

        # 创建HTML内容（包含qwebchannel.js的引用）
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>PySide6 WebChannel示例</title>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                button {
                    padding: 10px 15px;
                    margin: 5px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                }
                .result {
                    background-color: #f4f4f4;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>PySide6 WebChannel通信示例</h1>

                <div>
                    <button onclick="sendMessage()">发送消息到Python</button>
                    <button onclick="getDataFromPython()">从Python获取数据</button>
                    <button onclick="setData()">设置Python数据</button>
                    <button onclick="getData()">获取Python数据</button>
                </div>

                <div id="result" class="result">结果将显示在这里...</div>

                <script>
                    // 初始化WebChannel
                    var handler = null;
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        handler = channel.objects.handler;

                        // 监听Python端的数据变化
                        handler.dataChanged.connect(function(data) {
                            document.getElementById("result").innerHTML = 
                                "收到Python数据变化信号: " + data;
                        });

                        console.log("WebChannel初始化完成");
                    });

                    function sendMessage() {
                        if (handler) {
                            handler.js_message("来自JavaScript的问候!");
                            document.getElementById("result").innerHTML = 
                                "已发送消息到Python";
                        } else {
                            document.getElementById("result").innerHTML = 
                                "WebChannel未初始化";
                        }
                    }

                    function getDataFromPython() {
                        if (handler) {
                            handler.get_python_data("测试请求", function(response) {
                                document.getElementById("result").innerHTML = 
                                    "Python返回: " + response;
                            });
                        } else {
                            document.getElementById("result").innerHTML = 
                                "WebChannel未初始化";
                        }
                    }

                    function setData() {
                        if (handler) {
                            var data = "JavaScript设置的数据 " + new Date().toLocaleTimeString();
                            handler.set_data(data);
                            document.getElementById("result").innerHTML = 
                                "已设置数据: " + data;
                        }
                    }

                    function getData() {
                        if (handler) {
                            handler.get_data(function(data) {
                                document.getElementById("result").innerHTML = 
                                    "当前Python数据: " + data;
                            });
                        }
                    }
                </script>
            </div>
        </body>
        </html>
        '''

        # 加载HTML内容
        self.webView.setHtml(html_content)
        # 或者加载外部URL
        # self.webView.load(QUrl("http://example.com"))
        # 或者加载本地文件
        # self.webView.load(QUrl.fromLocalFile("/path/to/index.html"))

    def on_loaded(self, success):
        """网页加载完成回调"""
        if success:
            print("网页加载成功")
            # 可以通过JavaScript与页面交互
            self.webView.page().runJavaScript("console.log('页面加载完成，来自Python的消息')")
        else:
            print("网页加载失败")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置WebEngine的一些参数（可选）
    # 例如启用开发者工具
    # QWebEngineView.settings().setAttribute(QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

