# from mitmproxy.tools.cmdline import mitmdump
import time

from mitmproxy.tools.main import mitmdump
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import mitmproxy
from mitmproxy import http, ctx
import json
import sys
import random


# 实现隐藏的方式: 协议流量混淆
class ProtocolObfuscator:
    def __init__(self):
        self.original_responses = {}

    def request(self, flow: http.HTTPFlow):
        """修改请求以混淆协议特征"""
        if '/session' in flow.request.path or '/wd/hub' in flow.request.path:
            # 随机化路径
            flow.request.path = flow.request.path.replace('/wd/hub', f'/api/v{random.randint(1, 3)}')

            # 添加随机头部
            flow.request.headers['X-Request-ID'] = f"req_{random.randint(100000, 999999)}"
            flow.request.headers['X-Client-Type'] = random.choice(['webapp', 'mobile', 'desktop'])

            # 修改内容类型
            if flow.request.content:
                try:
                    data = json.loads(flow.request.content)
                    # 添加噪声数据
                    data['_noise'] = ''.join(random.choices('abcdef0123456789', k=16))
                    flow.request.text = json.dumps(data)
                except:
                    pass

    def response(self, flow: http.HTTPFlow):
        """修改响应以隐藏WebDriver特征"""
        if '/session' in flow.request.path and flow.response:
            # 存储原始响应用于后续处理
            self.original_responses[flow.request.path] = flow.response.content

            # 创建混淆响应
            flow.response.headers['Server'] = 'nginx/1.18.0'
            flow.response.headers['X-Powered-By'] = 'Express'

            if flow.response.content:
                try:
                    data = json.loads(flow.response.content)

                    # 删除或修改特定字段
                    if 'value' in data:
                        if 'webdriver' in data['value']:
                            data['value']['webdriver'] = None
                        if 'chrome' in data['value']:
                            data['value']['chrome']['userDataDir'] = ""

                    # 添加随机字段
                    data['timestamp'] = int(time.time() * 1000)
                    data['requestId'] = f"res_{random.randint(1000000, 9999999)}"

                    flow.response.text = json.dumps(data)
                except:
                    pass


# 启动代理
addons = [ProtocolObfuscator()]
# mitmdump(['-s', __file__, '--listen-port', '8080', '--mode', 'upstream:http://proxy-ip'])
# 配置代理参数
args = [
    "-s", __file__,  # 使用当前文件作为脚本
    "--listen-port", "8888",
    "--mode", "regular",  # 或 "upstream:http://your-proxy"
    "--set", "block_global=false"  # 允许外部连接
]
# 启动 mitmdump
mitmdump(args)
# 配置WebDriver使用代理
capabilities = DesiredCapabilities.EDGE.copy()
capabilities['proxy'] = {
    'proxyType': 'MANUAL',
    'httpProxy': 'localhost:8888',
    'sslProxy': 'localhost:8888'
}

driver = webdriver.Edge(desired_capabilities=capabilities)
driver.get("https://www.jd.com")