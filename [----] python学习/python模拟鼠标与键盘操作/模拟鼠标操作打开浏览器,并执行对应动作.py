from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# 在此之前需要对webdriver路径等进行配置.
driver = webdriver.Chrome()  # 需下载对应浏览器的 WebDriver
driver.get("https://www.baidu.com")  # 打开百度
search_box = driver.find_element(By.ID, "kw")  # 定位搜索框
search_box.send_keys("4399")  # 输入关键词
search_box.send_keys(Keys.ENTER)  # 按回车搜索
# 后续可点击结果中的链接 (如第一个结果)
first_result = driver.find_element(By.CSS_SELECTOR, "h3 a")
first_result.click()