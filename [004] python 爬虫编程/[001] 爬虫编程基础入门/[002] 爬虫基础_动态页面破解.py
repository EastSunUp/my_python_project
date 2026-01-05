
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 接单报价: 800-2000元/单
# 自动下载浏览器驱动
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.jd.com')

# 搜索商品并获取价格
search_box = driver.find_element('id', 'key')
search_box.send_keys('Python编程书籍')
search_box.submit()

# 等待结果加载
driver.implicitly_wait(5)  # 隐式等待

# 提取商品价格
prices = driver.find_elements('css selector', '.gl-price')
for price in prices[:5]:  # 前5个结果
    print(f'商品价格：{price.text}')

driver.quit()

