
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# -------------------------------基础方法 (使用requests + BeautifulSoup)
# 配置参数
url = "https://www.baidu.com/"  # 替换为目标网址/目标网页URL
save_dir = "F:\scraper_image_store"  # 图片保存目录
os.makedirs(save_dir, exist_ok=True)

# 1. 获取网页内容
response = requests.get(url)
response.raise_for_status()  # 检查请求状态

# 2. 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 3. 查找所有<img>标签
img_tags = soup.find_all('img')

# 4. 下载图片
for img in img_tags:
    img_url = img.get('src') or img.get('data-src')  # 处理不同属性
    if not img_url:
        continue

    # 处理相对路径
    img_url = urljoin(url, img_url)

    try:
        # 获取图片数据
        img_data = requests.get(img_url, stream=True).content
        # 生成文件名
        filename = os.path.join(save_dir, os.path.basename(img_url))
        # 保存图片
        with open(filename, 'wb') as f:
            f.write(img_data)
        print(f"下载成功: {img_url}")
    except Exception as e:
        print(f"下载失败 {img_url}: {str(e)}")
