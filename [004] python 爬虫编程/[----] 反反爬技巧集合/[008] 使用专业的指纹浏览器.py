
# 示例：VMLogin API 调用（需先安装其 SDK）
from vmlogin import VMLogin # 这个包不知道为什么安装不了

# TODO 这个文件的代码运行不了,不知道缺少哪个包还是什么东西?

goods_id = 62262510595
target_url = f'https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}'
profile_id = "your_profile_id"

driver = VMLogin(profile_id).start()
driver.get(target_url)

# import undetected_chromedriver as uc
# import time
# from selenium.webdriver.common.action_chains import ActionChains
#
# options = uc.ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")
# driver = uc.Chrome(options=options)
#
# # 添加随机鼠标移动
# actions = ActionChains(driver)
# actions.move_by_offset(10, 20).pause(1).move_by_offset(-5, 10).perform()
#
# driver.get(target_url)

