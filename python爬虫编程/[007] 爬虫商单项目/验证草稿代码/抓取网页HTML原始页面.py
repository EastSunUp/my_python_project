import requests
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


goods_id = "62262510595"  # 替换为您的商品ID:239952789828
url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
# url = "https://example.com"
response = requests.get(url)
raw_html = response.text  # 获得与手动查看源码相同的内容

# 设置保存路径
save_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(save_dir, f"{goods_id}_.html")

with open(save_path, "w", encoding="utf-8") as f:
    f.write(raw_html)




