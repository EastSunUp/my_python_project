from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import os
import time

# 商品ID和URL
goods_id = "62262510595"
# url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
base_url = "https://movie.douban.com/top250?start={}&filter="   # 豆瓣网 # 豆瓣网可以爬取,但是PDD不行,有很强的反爬机制
# for page in range(0, 250, 25):
#     url = base_url.format(page)  # 每隔25页开始
url = base_url.format(0)  # 每隔25页开始

# 配置 Edge 选项
edge_options = Options()

# 关键设置：使用真实用户配置文件
USER_PROFILE_PATH = r"C:\Users\shuangwang.shen\AppData\Local\Microsoft\Edge\User Data"
edge_options.add_argument(f"user-data-dir={USER_PROFILE_PATH}")

# 其他重要设置
edge_options.add_argument("--disable-blink-features=AutomationControlled")
edge_options.add_argument("--disable-infobars")
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-extensions")
edge_options.add_argument("--disable-popup-blocking")
edge_options.add_argument("--disable-notifications")

# 初始化 Edge WebDriver
EDGEDRIVER_PATH = r"F:\My_python_project\msedgedriver.exe"
service = Service(executable_path=EDGEDRIVER_PATH)

try:
    # 启动浏览器
    driver = webdriver.Edge(service=service, options=edge_options)

    # 访问目标URL
    driver.get(url)

    # 等待页面完全加载
    time.sleep(5)  # 可根据需要调整等待时间

    # 直接获取页面源代码（这会获取渲染后的HTML）
    rendered_html = driver.page_source

    # 获取原始HTML的替代方法
    # 使用JavaScript获取document.documentElement.outerHTML
    original_html = driver.execute_script("return document.documentElement.outerHTML;")

    # 保存原始HTML
    save_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(save_dir, f"{goods_id}_original_source.html")

    with open(save_path, "w", encoding="utf-8") as f:
        # 选择使用哪种HTML内容
        # f.write(rendered_html)  # 渲染后的HTML
        f.write(original_html)  # 使用JavaScript获取的HTML

    print(f"HTML已保存至: {save_path}")

except Exception as e:
    print(f"发生错误: {str(e)}")
    import traceback

    traceback.print_exc()

finally:
    # 确保浏览器关闭
    if 'driver' in locals():
        driver.quit()
        print("浏览器已关闭")

