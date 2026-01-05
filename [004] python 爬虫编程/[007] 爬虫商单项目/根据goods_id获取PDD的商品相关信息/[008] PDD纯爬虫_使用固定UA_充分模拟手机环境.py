from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time
import random
import re
import json
import sys
import threading
import requests
from fake_useragent import UserAgent

# 配置文件路径
CONFIG_FILE = "pdd_config.json"

class MobileBrowserSimulator:
    def __init__(self, device_name="iPhone 12 Pro"):
        self.device_profiles = {
            "iPhone 12 Pro": {
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
                "resolution": "390,844",
                "platform": "iPhone",
                "hardware_concurrency": 4,
                "device_memory": 4,
                "max_touch_points": 5,
                "pixel_ratio": 3.0,
                "color_depth": 30,
                # 新增关键参数
                "device_model": "iPhone12,3",
                "os_version": "15.0",
                "app_version": "605.1.15",
                "connection_type": "wifi",
                "battery_level": random.uniform(0.7, 0.9),
                "fonts": ["-apple-system", "PingFang SC", "Helvetica Neue"]
            },
            "Samsung Galaxy S21": {
                "user_agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
                "resolution": "360,800",
                "platform": "Linux armv8l",
                "hardware_concurrency": 8,
                "device_memory": 8,
                "max_touch_points": 10,
                "pixel_ratio": 2.75,
                "color_depth": 24,
                "device_model": "SM-G991B",
                "os_version": "11",
                "app_version": "537.36",
                "connection_type": "4g",
                "battery_level": random.uniform(0.6, 0.8),
                "fonts": ["Roboto", "Noto Sans CJK SC", "Droid Sans"]
            }
        }

        if device_name not in self.device_profiles:
            raise ValueError(f"Unsupported device: {device_name}")

        self.device = self.device_profiles[device_name]
        self.driver = None

# "userAgent":"Mozilla\u002F5.0 (Windows NT 10.0; Win64; x64)

def save_config(data):
    """保存配置到文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_config():
    """从文件加载配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        "cookies": [],
        "user_agent": "",
        "last_goods_id": ""
    }


def save_cookies(driver, domain=".yangkeduo.com"):
    """保存当前浏览器的cookies到配置"""
    config = load_config()
    config["cookies"] = driver.get_cookies()
    save_config(config)
    print(f"✅ Cookies已保存 ({len(config['cookies'])}条)")


def load_cookies(driver, domain=".yangkeduo.com"):
    """从配置加载cookies到浏览器"""
    config = load_config()
    cookies = config.get("cookies", [])

    if not cookies:
        print(f"⚠️ 未找到保存的cookies")
        return False

    try:
        # 先访问域名以设置cookies
        driver.get(f"https://{domain.strip('.')}")
        time.sleep(2)

        # 清除所有现有cookies
        driver.delete_all_cookies()
        print("清除当前浏览器页面cookies.")
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
                print(f"添加cookie失败!\n报错内容: {cookie.get('name')} - {str(e)}")

        print(f"✅ 已加载 {len(cookies)} 条cookies")
        return True
    except Exception as e:
        print(f"❌ 加载cookies失败: {str(e)}")
        return False


# 增加登录后验证
def verify_login_success(driver):
    """检查是否成功登录"""
    try:
        try:
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class*='user-info'], div[class*='user-avatar'], div[class*='my-container']"))
            )
            print("✅ 方法1: 通过用户信息元素验证登录成功")
            return True
        except:
            pass

        # 方法2: 检查页面URL
        current_url = driver.current_url
        if "login" not in current_url and "verify" not in current_url:
            print("✅ 方法2: 通过URL验证登录成功")
            return True

        # 方法3: 检查cookies中关键会话值
        cookies = driver.get_cookies()
        session_cookies = [c for c in cookies if "session" in c['name'].lower() or "token" in c['name'].lower()]

        if len(session_cookies) > 0:
            print("✅ 方法3: 通过会话cookies验证登录成功")
            return True

        # 方法4: 执行JS检测登录状态
        is_logged_in = driver.execute_script(
            """
               try {
                   return !!window._pdd_user_info || 
                          !!window._pdd_token || 
                          !!document.cookie.match(/(PDD_TOKEN|_nano_fp)/);
               } catch(e) {
                   return false;
               }
           """)

        if is_logged_in:
            print("✅ 方法4: 通过JS验证登录成功")
            return True
    except Exception as e:
        print(f"❌ 登录状态验证异常: {str(e)}")

    print("❌ 所有登录验证方法均失败")
    return False


def manual_login(driver, url):
    """引导用户手动登录（确保浏览器保持打开）"""
    print("\n" + "=" * 60)
    print("本次无法自动登录,需要进行手动登录拼多多!")
    print("=" * 60)
    print("1. Microsoft Edge 窗口已打开")
    print("2. 请使用手机号完成登录（需要短信验证码）")
    print("3. 登录完成后，请返回此控制台")
    print("4. 按回车键继续爬取...")
    print("=" * 60 + "\n")

    time.sleep(3)  # 休眠等待页面加载
    '''
        # 访问目标URL前先访问首页 # 2025/07/24新增
        # driver.get("https://mobile.yangkeduo.com")

        # 访问登录页面
        login_url = "https://mobile.yangkeduo.com/login.html"
        driver.get(login_url)
        # 添加页面加载等待
        WebDriverWait(driver, 15).until(
            ec.any_of(
                ec.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")),
                ec.presence_of_element_located((By.CSS_SELECTOR, "div.login-container"))
            )
        )
    '''

    print("请在此浏览器窗口中完成登录...")

    # 添加提示: 确保用户知道浏览器不会自动关闭
    print("注意: Edge 浏览器窗口将保持打开状态,直到您完成登录并按回车键!")

    # 创建并启动一个线程来监控登录状态
    login_complete = threading.Event()

    def check_login_status():
        """检查用户是否已登录"""
        check_count = 0
        while not login_complete.is_set() and check_count < 60:  # 最多检查5分钟
            try:
                '''
                    # 增加登录状态验证  2025/07/24新增
                    if not verify_login_success(driver):
                        print("登录状态异常,请重新登录!")
                        return manual_login(driver, url)  # 递归重试
                '''
                '''
                    # 检查登录成功后的典型元素
                    if driver.current_url != login_url and not driver.current_url.startswith(
                            "https://mobile.yangkeduo.com/login"):
                        print("\n✅ 检测到您已成功登录！")
                        login_complete.set()
                        return
                '''
                if verify_login_success(driver):
                    print("✅ 登录状态验证成功！")
                    '''
                        # 登录后访问首页建立完整会话
                        driver.get("https://mobile.yangkeduo.com")
                        time.sleep(3)
                        # 模拟用户浏览行为
                        print("🛍️ 模拟用户浏览行为...")
                        for _ in range(2):
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.7)")
                            time.sleep(2)
                            driver.execute_script("window.scrollTo(0, 0)")
                            time.sleep(1.5)
                        login_complete.set()
                    '''
                    return
            except Exception as e:
                print(f"登录检查异常: {str(e)}")
            time.sleep(3)
            check_count += 1

    # 启动登录状态检查线程
    check_thread = threading.Thread(target=check_login_status)
    check_thread.daemon = True
    check_thread.start()

    # 等待用户手动输入回车
    while True:
        user_input = input("请完成登录后按回车键继续...")
        # 检测回车键: 空字符串表示只按了回车
        if user_input == "":
            print("检测到回车键,程序继续执行！")
            break
        else:
            print(f"您输入了: '{user_input}',但程序需要您直接按回车键!")
            continue

    # 最终验证登录状态
    if not verify_login_success(driver):
        print("最终登录验证失败,会话可能无效!")
        # choice = input("是否重新尝试登录? (y/n): ").lower()
        # if choice == 'y':
        #     return manual_login(driver, url)
        # else:
        #     print("⚠️ 继续操作可能获取异常页面")
        #     return False

    # 设置事件通知线程退出
    login_complete.set()
    # 保存登录状态 (保存cookies)
    save_cookies(driver)
    time.sleep(1)
    # 加载cookies
    load_cookies(driver, ".yangkeduo.com")
    # 访问目标URL前先等待
    time.sleep(2)
    # 打印会话信息用于调试
    print("\n会话信息:")
    print(f"当前URL: {driver.current_url}")
    print(f"Cookies数量: {len(driver.get_cookies())}")
    # # 访问目标URL
    print(f"\n🌐 正在访问目标商品: {url}")
    driver.get(url)
    time.sleep(3)
    # 开启检查商品是否售罄检查!
    check_product_status = True # 检查商品状态
    if check_product_status is True:
        # 检查商品是否售罄 (检查商品状态是否异常)
        if "已售罄" in driver.page_source:
            print("商品状态异常: 已售罄 !")
            print("尝试解决方案: 刷新页面...")
            '''
                choice = input("是否尝试重新访问? (y/n): ").lower()
                if choice == 'y':
                    driver.refresh()
                    time.sleep(3)
                else:
                    print("⚠️ 继续操作可能获取异常页面")
            '''
            try:
                driver.refresh()
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "div[data-tag='goodsDetail']"))
                )
            except Exception as e:
                print(f"网页刷新操作失败,报错如下:\n {str(e)}")
                import traceback
                traceback.print_exc()
                return False
    return True


def get_edge_driver_path():
    """获取Edge驱动的路径"""
    # 尝试常见安装位置
    possible_paths = [
        r"C:\Program Files\Microsoft\Edge\Application\msedgriver.exe",
        r"F:\My_python_project\msedgedriver.exe",
        os.path.join(os.environ.get("PROGRAMFILES", ""), "Microsoft", "Edge", "Application", "msedgedriver.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Microsoft", "Edge", "Application", "msedgedriver.exe")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # 如果找不到，尝试从网络下载
    print("⚠️ 未找到msedgedriver,尝试自动下载...")
    try:
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        return EdgeChromiumDriverManager().install()
    except ImportError:
        print("❌ 请先安装webdriver-manager: pip install webdriver-manager")
        return None

def config_edge(headless=False, mobile_ua=None):
    """ 配置Edge选项,对edge浏览器进行一些初始化设置 """
    edge_options = Options()
    if headless:
        edge_options.add_argument("--headless=new")  # 配置浏览器无头模式
    else:
        # 在可视化模式下保持浏览器打开直到手动关闭
        edge_options.add_experimental_option("detach", True)

    # 在Edge选项设置中添加以下修改(关闭web安全模式) # 2025/07/24 日新增
    edge_options.add_argument("--disable-web-security")
    edge_options.add_argument("--disable-site-isolation-trials")
    edge_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    # 设置移动设备模拟
    edge_options.add_argument("--window-size=575,812")
    edge_options.add_argument(f"user-agent={mobile_ua}")

    # 禁用自动化特征
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)

    # 获取Edge驱动路径(配置Edge_Driver)
    edge_driver_path = get_edge_driver_path()
    if not edge_driver_path:
        print("❌ 无法找到或下载Microsoft Edge WebDriver")
        return False
    # 设置浏览器driver
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    return edge_options ,driver

def save_html_source(url, save_path, headless=False):
    # 加载配置
    config = load_config()
    # 使用配置中的UA (如果存在)
    if config.get("user_agent"):
        mobile_ua = config["user_agent"]
    else:
        # 动态生成最新移动端 User-Agent
        ua = UserAgent()
        mobile_ua = ua.random

    # 设置重试次数,暂时设置为3次重试.
    retry_times = 3
    for try_times in range(1, retry_times + 1):
        # 配置edge浏览器(对浏览器做一些初始化设置)
        edge_options, driver = config_edge(headless=False, mobile_ua=None)

        try:
            # 彻底移除自动化特征 # 增强指纹隐藏(在CDP命令中添加) # 2025/07/24日新增
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source":
                    """
                        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                        Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
                        window.chrome = {app: {isInstalled: false}};
                        window.navigator.permissions = {query: () => Promise.resolve({state: 'granted'})};
                        window.navigator.mediaDevices = {enumerateDevices: () => Promise.resolve([])};
    
                        // 增强指纹隐藏 (在CDP命令中添加)
                       Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                       Object.defineProperty(navigator, 'plugins', {
                           get: () => [{
                               name: 'Chrome PDF Plugin',
                               filename: 'internal-pdf-viewer',
                               description: 'Portable Document Format'
                           }, {
                               name: 'Chrome PDF Viewer',
                               filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                               description: 'Portable Document Format'
                           }, {
                               name: 'Native Client',
                               filename: 'internal-nacl-plugin',
                               description: 'Native Client Executable'
                           }]
                       });
                       Object.defineProperty(navigator, 'languages', {
                           get: () => ['zh-CN', 'zh', 'en']
                       });
    
                       // 覆盖屏幕参数
                       Object.defineProperty(screen, 'width', {get: () => 375});
                       Object.defineProperty(screen, 'height', {get: () => 812});
                       Object.defineProperty(screen, 'availWidth', {get: () => 375});
                       Object.defineProperty(screen, 'availHeight', {get: () => 812});
    
                       // 随机化硬件并发数
                       Object.defineProperty(navigator, 'hardwareConcurrency', {
                           get: () => Math.random() > 0.5 ? 4 : 8
                       });
    
                       // WebGL指纹干扰
                       const getParameter = WebGLRenderingContext.prototype.getParameter;
                       WebGLRenderingContext.prototype.getParameter = function(parameter) {
                           if (parameter === 37445) return 'Intel Inc.'; // VENDOR
                           if (parameter === 37446) return 'Intel Iris OpenGL Engine'; // RENDERER
                           return getParameter.apply(this, [parameter]);
                       };
                    """
            })

            print(f"使用设备UA: {mobile_ua}")
            print("使用Microsoft Edge 进行模拟真实用户访问...")

            # 清除当前所有现有cookies,让浏览器自己生成.
            driver.delete_all_cookies()
            print("清除当前浏览器页面cookies.")
            time.sleep(1)

            # 尝试加载cookies # 暂时不加载cookies
            # cookies_loaded = load_cookies(driver, "mobile.yangkeduo.com")

            # 访问目标页面
            print(f"🌐 正在访问目标页面: {url}")
            driver.get(url)
            time.sleep(5)  # 等待页面初步加载

            # 检查是否需要登录 ----------------------------------------------------------------------
            login_detected = False
            # 检查各种可能的登录提示元素
            login_selectors = [
                "div.login-container",
                "div.captcha-popup",
                "div[class*='login-mask']",
                "div[class*='login-modal']",
                "div[class*='captcha-modal']",
                "div[class*='verify-bar']",
                "div[class*='phone-login']"
            ]

            for selector in login_selectors:
                if driver.find_elements(By.CSS_SELECTOR, selector):
                    login_detected = True
                    break

            # # 暂时不识别是否需要登录,暂时不做登录验证与手动登录操作
            # login_detected = False
            if login_detected:
                print("🔒 检测到登录验证")
                if not headless:
                    print("⚠️ 需要手动登录")
                    manual_login(driver, url)
                else:
                    print("❌ 无头模式下无法手动登录,请先使用非无头模式获取cookies")
                    return False
            else:
                print("🔓 未检测到登录验证")

            # 核心内容等待 - 使用更通用的选择器 -------------------------------------------------------------
            try:
                print("尝试加载商品详情内容...")
                # 尝试多个可能的选择器
                WebDriverWait(driver, 30).until(
                    ec.any_of(
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div[data-tag='goodsDetail']")),
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div.goods-detail")),
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div[class*='goods-detail-container']")),
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div.detail-container")),
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div[class*='detail-content']")),
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div[class*='goods-info']")),
                        # 添加更多Edge特有的选择器
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div[class*='product-detail']")),
                        ec.presence_of_element_located((By.CSS_SELECTOR, "div[class*='item-container']"))
                    )
                )
                print("商品详情内容加载完成!")
            except:
                if try_times < retry_times:
                    print(f"第{try_times}次,商品详情内容加载失败!")
                    print("关闭浏览器!")
                    driver.quit()  # 关闭浏览器
                    # 动态生成最新移动端User-Agent(如果出错,生成新的UserAgent然后重试)
                    ua = UserAgent()
                    mobile_ua = ua.random
                    print(f"随机生成UserAgent:{mobile_ua},进行第{try_times + 1}次重试")
                    continue
                else:
                    print(f"经过{retry_times}次重试后,仍然加载失败!")

            # 在原有位置替换滚动代码
            # print("🔄 模拟人类滚动行为...")
            # random_scroll(driver)  # 2025/07/24 新增    # 取消随机点击行为 2025/07/27

            # 最终获取页面源码 # 直接获取页面源代码 (这里获取渲染后的HTML)
            rendered_html = driver.page_source

            # 保存前清理自动化痕迹
            rendered_html = re.sub(r"window\._is_driver = true;", "", rendered_html)
            rendered_html = re.sub(r"selenium_\w+", "", rendered_html)

            # 获取原始HTML的替代方法
            # 使用JavaScript获取document.documentElement.outerHTML
            original_html = driver.execute_script("return document.documentElement.outerHTML;")

            with open(save_path, "w", encoding="utf-8") as f:
                # f.write(html_content)
                # 选择使用哪种HTML内容
                # f.write(rendered_html)  # 渲染后的HTML
                f.write(original_html)  # 使用JavaScript获取的HTML

            print(f"💾 源码已保存至: {save_path} (大小: {len(original_html) // 1024}KB)")

            # 调试用截图(不保存截图)
            # screenshot_path = save_path.replace(".html", ".png")
            # driver.save_screenshot(screenshot_path)
            # print(f"📸 截图已保存: {screenshot_path}")

            # 保存当前UA到配置
            config = load_config()
            config["user_agent"] = mobile_ua
            save_config(config)
            return True
        except Exception as e:
            print(f"❌ 操作失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 在可视化模式下,不自动关闭浏览器
            if headless and 'driver' in locals():
                driver.quit()


def main():
    # 目标URL
    goods_id = "62262510595"  # 替换为您的商品ID:  239952789828 62262510595
    url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"

    # 设置保存路径
    save_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(save_dir, f"pdd_goods_{goods_id}_source.html")

    print("=" * 60)
    print("运行拼多多商品信息爬虫,采用 Microsoft Edge 方案!")
    print("=" * 60)
    print(f"目标商品ID: {goods_id}")
    print(f"html文件保存路径: {save_path}")

    # 询问是否使用无头模式
    headless = False
    if len(sys.argv) > 1 and sys.argv[1].lower() == "headless":
        headless = True
        print("运行模式: 无头模式")
    else:
        print("运行模式: 可视化模式 (推荐首次使用)")
        print("注意: 在可视化模式下,Edge 窗口将保持打开直到您关闭它")

    print("\n开始爬取...")

    success = save_html_source(url, save_path, headless=headless)

    if success:
        print("\n✅ 操作成功！")
        print(f"📄 HTML文件: {save_path}")
        # print(f"🖼️ 截图文件: {save_path.replace('.html', '.png')}")
        # 验证内容
        print("\n请检查HTML文件中是否包含您需要的信息,特别是以下内容: ")
        print("1. 商品标题、2. 商品价格、3. 商品规格、4. 商品详情描述、5. 用户评价")
    else:
        print("\n❌ 操作失败，请尝试以下解决方案:")
        print("1. 使用可视化模式首次运行: python script.py")
        print("2. 登录后保存cookies,然后使用无头模式: python script.py headless")
        print("3. 确保Microsoft Edge已安装并更新到最新版本")
        print("4. 检查网络连接")


if __name__ == "__main__":
    # 检查并创建配置文件
    if not os.path.exists(CONFIG_FILE):
        save_config({
            "cookies": [],
            "user_agent": "",
            "last_goods_id": ""
        })

    main()
