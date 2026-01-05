# ----------------------启用javascript动态验证---------------------------
# 使用javascript动态验证
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import os

goods_id = "62262510595"  # 替换为您的商品ID:239952789828
url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
# 配置 Chrome 选项
chrome_options = Options()
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# 初始化 WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get(f"{url}")

# 获取性能日志
logs = driver.get_log('performance')

# 查找并提取原始 HTML 响应
raw_html = None
for entry in logs:
    log = json.loads(entry['message'])
    message = log.get('message', {})

    if message.get('method') == 'Network.responseReceived':
        response = message.get('params', {}).get('response', {})
        if response.get('mimeType') == 'text/html':
            request_id = message['params']['requestId']
            # 获取响应体
            result = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            raw_html = result.get('body')
            break

if raw_html:
    print("成功获取原始 HTML")
    # 设置保存路径
    js_save_dir = os.path.dirname(os.path.abspath(__file__))
    js_save_path = os.path.join(js_save_dir, f"{goods_id}_log_.html")
    with open(js_save_path, "w", encoding="utf-8") as f:
        f.write(raw_html)
else:
    print("未找到原始 HTML 响应")

driver.quit()