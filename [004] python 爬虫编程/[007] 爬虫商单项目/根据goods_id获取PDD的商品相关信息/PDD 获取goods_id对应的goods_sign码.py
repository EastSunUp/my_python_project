import time
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# ======== 配置参数 ========
app_key = '237bfc3d5f4d472b93b2dcb44439dff8'
app_secret = '9261a22eb6b31a0ed0ddde2f6b4fb5095519c1d5'
access_token = '92ff137bb298427abbb66a46696f5c13dfb97c6c'
goods_id = "62262510595"
pid = "43211858_307667234"


# ======== 浏览器设置 ========
def setup_driver():
    """配置并返回Chrome浏览器驱动"""
    chrome_options = Options()

    # 设置移动设备模拟
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # 其他选项
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=zh-CN")

    # 设置无头模式（如果需要）
    # chrome_options.add_argument("--headless")

    # 设置WebDriver路径（需要根据实际路径修改）
    driver_path = "chromedriver.exe"  # 替换为你的chromedriver路径

    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except WebDriverException as e:
        print(f"无法启动浏览器驱动: {str(e)}")
        print("请确保已安装Chrome浏览器并下载对应版本的chromedriver")
        print("下载地址: https://sites.google.com/chromium.org/driver/")
        return None


# ======== 提取函数 ========
def extract_goods_sign_from_script(driver):
    """从页面脚本中提取goods_sign"""
    try:
        # 尝试获取window.rawData
        raw_data = driver.execute_script("return window.rawData;")
        if raw_data:
            # 尝试多种可能的路径
            paths = [
                ["store", "initDataObj", "goods", "goodsSign"],
                ["detail", "goods", "goodsSign"],
                ["goods", "goodsSign"],
                ["initDataObj", "goods", "goodsSign"]
            ]

            for path in paths:
                try:
                    value = raw_data
                    for key in path:
                        value = value.get(key)
                    if value:
                        return value
                except (TypeError, AttributeError):
                    continue

        # 尝试获取window.ssrData
        ssr_data = driver.execute_script("return window.ssrData;")
        if ssr_data:
            paths = [
                ["detail", "goods", "goodsSign"],
                ["goods", "goodsSign"],
                ["store", "goods", "goodsSign"]
            ]

            for path in paths:
                try:
                    value = ssr_data
                    for key in path:
                        value = value.get(key)
                    if value:
                        return value
                except (TypeError, AttributeError):
                    continue

        # 尝试从全局变量中获取
        goods_sign = driver.execute_script("""
            if (window.goodsSign) return window.goodsSign;
            if (window.GOODS_SIGN) return window.GOODS_SIGN;
            return null;
        """)
        if goods_sign:
            return goods_sign

        # 尝试从meta标签获取
        meta_element = driver.find_element(By.CSS_SELECTOR, 'meta[name="goods-sign"]')
        if meta_element:
            return meta_element.get_attribute("content")

    except Exception as e:
        print(f"脚本提取失败: {str(e)}")

    return None


def extract_goods_sign_from_network(driver):
    """从网络请求中提取goods_sign"""
    try:
        # 获取所有网络请求
        performance_log = driver.get_log('performance')

        # 搜索包含商品信息的响应
        for entry in performance_log:
            message = json.loads(entry['message'])['message']

            # 只处理响应接收事件
            if message['method'] == 'Network.responseReceived':
                url = message['params']['response']['url']

                # 检查是否是商品API
                if 'api/mall' in url or 'goods/detail' in url or 'goods/info' in url:
                    request_id = message['params']['requestId']

                    # 获取响应内容
                    response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})

                    if response_body and 'body' in response_body:
                        body = response_body['body']

                        # 尝试解析JSON
                        try:
                            data = json.loads(body)

                            # 搜索goods_sign
                            def search_json(obj):
                                if isinstance(obj, dict):
                                    for key, value in obj.items():
                                        if key.lower() in ['goods_sign', 'goodssign', 'goodssign']:
                                            return value
                                        result = search_json(value)
                                        if result:
                                            return result
                                elif isinstance(obj, list):
                                    for item in obj:
                                        result = search_json(item)
                                        if result:
                                            return result
                                return None

                            goods_sign = search_json(data)
                            if goods_sign:
                                return goods_sign

                        except json.JSONDecodeError:
                            # 如果不是JSON，尝试搜索文本
                            if 'goods_sign' in body:
                                # 尝试提取类似 "goods_sign": "value" 的格式
                                match = re.search(r'"goods_sign"\s*:\s*"([^"]+)"', body)
                                if match:
                                    return match.group(1)

    except Exception as e:
        print(f"网络请求分析失败: {str(e)}")

    return None


# ======== 主函数 ========
def get_goods_sign_with_selenium(goods_id):
    """使用Selenium获取goods_sign"""
    print("启动浏览器模拟...")
    driver = setup_driver()

    if not driver:
        print("无法启动浏览器,请检查配置")
        return None

    try:
        # 打开商品页面
        url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
        print(f"访问页面: {url}")
        driver.get(url)

        # 等待页面加载完成
        print("等待页面加载...")
        try:
            # 等待商品标题出现
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".goods-title")))
        except TimeoutException:
            print("页面加载超时，但继续尝试提取数据...")

        # 方法1：从页面脚本中提取
        print("尝试从页面脚本提取goods_sign...")
        goods_sign = extract_goods_sign_from_script(driver)
        if goods_sign:
            print(f"成功从脚本获取goods_sign: {goods_sign}")
            return goods_sign

        # 方法2：从网络请求中提取
        print("尝试从网络请求提取goods_sign...")
        goods_sign = extract_goods_sign_from_network(driver)
        if goods_sign:
            print(f"成功从网络请求获取goods_sign: {goods_sign}")
            return goods_sign

        # 方法3：保存页面供手动分析
        save_page_for_analysis(driver, goods_id)

        print("无法自动提取goods_sign，请查看保存的页面进行分析")
        return None

    except Exception as e:
        print(f"浏览器操作失败: {str(e)}")
        return None
    finally:
        print("关闭浏览器...")
        driver.quit()


def save_page_for_analysis(driver, goods_id):
    """保存页面内容供后续分析"""
    debug_dir = "selenium_debug"
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    # 保存HTML
    html_path = os.path.join(debug_dir, f"goods_{goods_id}_{int(time.time())}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"已保存页面HTML到: {html_path}")

    # 保存截图
    screenshot_path = os.path.join(debug_dir, f"goods_{goods_id}_{int(time.time())}.png")
    driver.save_screenshot(screenshot_path)
    print(f"已保存页面截图到: {screenshot_path}")


# ======== 执行获取 ========
if __name__ == "__main__":
    print("=" * 50)
    print(f"开始获取商品ID: {goods_id} 的goods_sign")
    print("=" * 50)

    start_time = time.time()
    result = get_goods_sign_with_selenium(goods_id)

    if result:
        print("\n" + "=" * 50)
        print(f"✅ 成功获取 goods_sign: {result}")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 未能获取 goods_sign，请查看保存的调试文件")
        print("=" * 50)

    print(f"总耗时: {time.time() - start_time:.2f}秒")