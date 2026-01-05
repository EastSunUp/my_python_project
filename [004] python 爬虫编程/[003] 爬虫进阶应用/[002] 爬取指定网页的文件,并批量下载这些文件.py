import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 这里的文件统一指定的是下载PDF文件 ---------------------------------------------------------------------
# 配置参数
url = "https://example.com/files"  # 目标网页
download_dir = "./downloads"  # 下载目录
file_extension = ".pdf"  # 目标文件扩展名

# 创建下载目录
os.makedirs(download_dir, exist_ok=True)

# 1. 获取网页内容
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
    exit()

# 2. 解析文件链接
soup = BeautifulSoup(response.text, 'html.parser')
file_links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.endswith(file_extension):
        # 将相对URL转为绝对URL
        full_url = urljoin(url, href)
        file_links.append(full_url)

print(f"找到 {len(file_links)} 个文件")

# 3. 批量下载
for i, file_url in enumerate(file_links):
    try:
        # 获取文件名
        filename = os.path.join(download_dir, file_url.split('/')[-1])

        # 下载文件
        print(f"正在下载 ({i + 1}/{len(file_links)}): {filename}")
        file_response = requests.get(file_url, headers=headers, stream=True)
        file_response.raise_for_status()

        # 写入文件
        with open(filename, 'wb') as f:
            for chunk in file_response.iter_content(chunk_size=8192):   # PDF文件?
                f.write(chunk)

        print(f"✓ 下载成功: {filename}")

    except Exception as e:
        print(f"× 下载失败 {file_url}: {str(e)}")

print("所有文件下载完成！")
