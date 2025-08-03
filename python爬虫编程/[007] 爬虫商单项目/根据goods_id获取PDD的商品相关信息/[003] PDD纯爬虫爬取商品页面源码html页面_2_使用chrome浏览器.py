from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
import re
import json
from fake_useragent import UserAgent
import sys


def save_cookies(driver, filename="pdd_cookies.json"):
    """保存当前浏览器的cookies到文件"""
    cookies = driver.get_cookies()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"✅ Cookies已保存至 {filename} ({len(cookies)}条)")


def load_cookies(driver, domain=".yangkeduo.com", filename="pdd_cookies.json"):
    """从文件加载cookies到浏览器"""
    if not os.path.exists(filename):
        print(f"⚠️ Cookies文件 {filename} 不存在")
        return False

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        # 先访问域名以设置cookies
        driver.get(f"https://{domain.strip('.')}")
        time.sleep(2)

        # 清除所有现有cookies
        driver.delete_all_cookies()
        time.sleep(1)

        # 添加新的cookies
        for cookie in cookies:
            # 修复cookies格式
            if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                del cookie['sameSite']
            if 'domain' not in cookie:
                cookie['domain'] = domain

            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"⚠️ 添加cookie失败: {cookie.get('name')} - {str(e)}")

        print(f"✅ 已加载 {len(cookies)} 条cookies")
        return True
    except Exception as e:
        print(f"❌ 加载cookies失败: {str(e)}")
        return False


def manual_login(driver, url):
    """引导用户手动登录"""
    print("\n" + "=" * 60)
    print("⚠️ 需要手动登录拼多多")
    print("=" * 60)
    print("1. 浏览器窗口将打开拼多多登录页面")
    print("2. 请使用手机号完成登录（可能需要短信验证码）")
    print("3. 登录成功后，请返回此控制台")
    print("4. 按回车键继续爬取...")
    print("=" * 60 + "\n")

    # 访问登录页面
    login_url = "https://mobile.yangkeduo.com/login.html"
    driver.get(login_url)

    # 等待用户手动登录
    input("请完成登录后按回车键继续...")

    # 保存登录状态
    save_cookies(driver)

    # 访问目标URL
    driver.get(url)
    return True


def save_html_source(url, save_path, headless=False):
    # 动态生成最新移动端User-Agent
    ua = UserAgent()
    mobile_ua = ua.random

    # 增强型设备模拟
    mobile_emulation = {
        "deviceMetrics": {
            "width": 375,
            "height": 812,
            "pixelRatio": 3.0,
            "touch": True
        },
        "userAgent": mobile_ua
    }

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")  # 使用新版headless模式

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--lang=zh-CN")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # 使用环境变量配置路径
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH", r"F:\My_python_project\chromedriver.exe")

    try:
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 彻底移除自动化特征
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
                window.chrome = {app: {isInstalled: false}};
                window.navigator.permissions = {query: () => Promise.resolve({state: 'granted'})};
                window.navigator.mediaDevices = {enumerateDevices: () => Promise.resolve([])};
            """
        })

        print(f"📱 使用设备UA: {mobile_ua}")
        print("🚀 正在模拟真实用户访问...")

        # 尝试加载cookies
        cookies_loaded = load_cookies(driver, ".yangkeduo.com")

        # 访问目标页面
        print(f"🌐 正在访问目标页面: {url}")
        driver.get(url)

        # 检查是否需要登录
        time.sleep(5)  # 等待页面初步加载
        if driver.find_elements(By.CSS_SELECTOR, "div.login-container, div.captcha-popup, div[class*='login-mask']"):
            print("🔒 检测到登录验证，尝试加载cookies...")
            if not cookies_loaded:
                print("⚠️ 无有效cookies，需要手动登录")
                if not headless:
                    manual_login(driver, url)
                else:
                    print("❌ 无头模式下无法手动登录，请先使用非无头模式获取cookies")
                    return False
            else:
                print("⚠️ cookies可能已过期，尝试重新登录")
                if not headless:
                    manual_login(driver, url)
                else:
                    print("❌ 无头模式下无法重新登录")
                    return False

        # 核心内容等待 - 使用更通用的选择器
        try:
            # 尝试多个可能的选择器
            WebDriverWait(driver, 300).until(
                EC.or_(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tag='goodsDetail']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.goods-detail")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='goods-detail-container']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.detail-container")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='detail-content']"))
                )
            )
            print("✅ 商品详情内容已加载")
        except:
            print("⚠️ 商品详情加载超时,尝试继续执行")
        # 增强型滚动模拟（解决懒加载）
        scroll_actions = [
            {"pos": 300, "wait": 1.5},
            {"pos": 800, "wait": 2.0},
            {"pos": 1500, "wait": 1.8},
            {"pos": "document.body.scrollHeight*0.7", "wait": 2.5},
            {"pos": "document.body.scrollHeight", "wait": 3.0}
        ]

        print("🔄 模拟用户滚动页面...")
        for action in scroll_actions:
            if isinstance(action["pos"], str):
                # 计算动态高度
                scroll_pos = driver.execute_script(f"return {action['pos']}")
            else:
                scroll_pos = action["pos"]

            driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            time.sleep(action["wait"])

            # 随机移动鼠标模拟真实行为
            driver.execute_script(f"""
                window.dispatchEvent(new MouseEvent('mousemove', {{
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    screenX: {random.randint(100, 300)},
                    screenY: {random.randint(200, 500)},
                    clientX: {random.randint(10, 200)},
                    clientY: {random.randint(50, 300)}
                }}));
            """)

        # 最终获取页面源码
        html_content = driver.page_source

        # 保存前清理自动化痕迹
        html_content = re.sub(r"window\._is_driver = true;", "", html_content)
        html_content = re.sub(r"selenium_\w+", "", html_content)

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"💾 源码已保存至: {save_path} (大小: {len(html_content) // 1024}KB)")

        # 调试用截图
        screenshot_path = save_path.replace(".html", ".png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 截图已保存: {screenshot_path}")

        return True

    except Exception as e:
        print(f"❌ 操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'driver' in locals():
            driver.quit()


def main():
    # 目标URL
    goods_id = "239952789828"  # 替换为您的商品ID
    url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"

    # 设置保存路径
    save_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(save_dir, f"pdd_goods_{goods_id}_source.html")

    print("=" * 60)
    print("🔥 拼多多商品页面爬取 - 登录解决方案")
    print("=" * 60)
    print(f"🛒 目标商品ID: {goods_id}")
    print(f"📁 保存路径: {save_path}")

    # 询问是否使用无头模式
    headless = False
    if len(sys.argv) > 1 and sys.argv[1].lower() == "headless":
        headless = True
        print("⚙️ 模式: 无头模式")
    else:
        print("⚙️ 模式: 可视化模式 (推荐首次使用)")

    print("\n开始爬取...")

    success = save_html_source(url, save_path, headless=headless)

    if success:
        print("\n✅ 操作成功！")
        print(f"📄 HTML文件: {save_path}")
        print(f"🖼️ 截图文件: {save_path.replace('.html', '.png')}")
    else:
        print("\n❌ 操作失败，请尝试以下解决方案:")
        print("1. 使用可视化模式首次运行: python script.py")
        print("2. 登录后保存cookies，然后使用无头模式: python script.py headless")
        print("3. 确保ChromeDriver版本与浏览器匹配")
        print("4. 检查网络连接")


if __name__ == "__main__":
    main()