from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import traceback
import re
import random
import json

# 确保路径正确 - 使用原始字符串避免转义问题
EDGE_DRIVER_PATH = r"F:\My_python_project\msedgedriver.exe"


# 京东页面结构检测器
class JDStructureDetector:
    def __init__(self, driver):
        self.driver = driver
        self.page_source = driver.page_source
        self.current_url = driver.current_url

    def is_search_page(self):
        """检测当前是否在搜索结果页面"""
        if "search" in self.current_url and "keyword" in self.current_url:
            return True
        return False

    def detect_search_container(self):
        """检测搜索结果容器"""
        # 尝试多种可能的容器选择器
        container_selectors = [
            "#J_goodsList",
            ".goods-list",
            ".gl-warp",
            ".search-list",
            ".m-list",
            ".product-list",
            ".list-h"
        ]

        for selector in container_selectors:
            try:
                container = self.driver.find_element(By.CSS_SELECTOR, selector)
                return container
            except:
                continue
        return None

    def detect_product_pattern(self):
        """检测商品元素模式"""
        # 尝试多种可能的商品选择器
        product_selectors = [
            ".gl-item",
            ".goods-item",
            ".j-sku-item",
            ".product-item",
            ".search-item",
            ".item[data-sku]",
            ".item",
            ".product",
            ".pro-item",
            ".p-item"
        ]

        for selector in product_selectors:
            try:
                products = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if products and len(products) > 0:
                    # 验证第一个商品是否包含价格元素
                    sample = products[0]
                    price_elems = sample.find_elements(By.XPATH,
                                                       ".//*[contains(text(), '¥') or contains(text(), '￥') or contains(text(), '元')]")
                    if price_elems:
                        return selector
            except:
                continue
        return None

    def detect_page_type(self):
        """检测页面类型"""
        if self.is_search_page():
            return "search"
        elif "jd.com" in self.current_url:
            return "home"
        elif "passport.jd.com" in self.current_url:
            return "login"
        elif "item.jd.com" in self.current_url:
            return "product"
        return "unknown"


# 人类化操作模拟
def human_type(element, text, delay_range=(0.05, 0.2)):
    """模拟人类输入速度"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))


def human_scroll(driver, scroll_distance):
    """模拟人类滚动行为"""
    scroll_steps = max(5, int(scroll_distance / 200))
    current_position = 0

    for _ in range(scroll_steps):
        step = random.randint(100, 300)
        current_position += step
        if current_position > scroll_distance:
            current_position = scroll_distance

        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(random.uniform(0.1, 0.5))

    return current_position


# 智能商品信息提取器
class SmartProductExtractor:
    def __init__(self, product_element):
        self.element = product_element
        self.html = product_element.get_attribute('outerHTML')

    def extract_with_patterns(self, patterns, is_text=True):
        """通用模式提取方法"""
        for pattern in patterns:
            try:
                if isinstance(pattern, tuple):
                    # CSS选择器 + 属性名
                    element = self.element.find_element(By.CSS_SELECTOR, pattern[0])
                    value = element.get_attribute(pattern[1]) if pattern[1] else element.text
                else:
                    # 直接CSS选择器
                    element = self.element.find_element(By.CSS_SELECTOR, pattern)
                    value = element.text

                if value and value.strip():
                    return value.strip()
            except:
                continue

        # 尝试从整个元素HTML中提取
        if is_text:
            all_text = self.element.text.strip()
            if all_text:
                # 过滤掉空行和非商品信息
                valid_lines = [line for line in all_text.split('\n') if line.strip() and len(line) > 2]
                if valid_lines:
                    return valid_lines[0]

        return None

    def extract_name(self):
        """智能提取商品名称"""
        name_patterns = [
            (".p-name em", None),
            (".sku-name", None),
            (".p-name a", "title"),
            (".name a", "title"),
            (".p-name", None),
            (".name", None),
            ("[title]", "title"),
            ("img", "alt"),
            (".p-name a", None),
            (".name a", None)
        ]

        name = self.extract_with_patterns(name_patterns)
        return name or "未知商品"

    def extract_price(self):
        """智能提取商品价格"""
        price_patterns = [
            ".p-price i",
            ".p-price strong",
            ".J_price",
            ".jd-price",
            ".price",
            ".p-price",
            ".price-box"
        ]

        price = self.extract_with_patterns(price_patterns)

        # 正则表达式提取价格
        if not price:
            price_patterns_re = [
                r'¥\s*([\d,]+\.\d{2})',
                r'￥\s*([\d,]+\.\d{2})',
                r'price:\s*"([\d,]+\.\d{2})"',
                r'<i>([\d,]+\.\d{2})</i>',
                r'[\d,]+\.\d{2}元'
            ]
            for pattern in price_patterns_re:
                matches = re.findall(pattern, self.html)
                if matches:
                    # 取第一个匹配的价格
                    price_value = matches[0].replace(',', '')
                    return f"¥{price_value}"

        return price or "未知价格"

    def extract_shop(self):
        """智能提取店铺信息"""
        shop_patterns = [
            (".p-shop a", None),
            (".shop a", None),
            (".J_im_icon", None),
            (".store a", None),
            (".seller a", None),
            ("a[href*='shop']", None),
            (".shopname", None),
            (".shop-link", None),
            (".store-name", None)
        ]

        shop = self.extract_with_patterns(shop_patterns)
        return shop or "未知店铺"

    def extract_comments(self):
        """智能提取评论信息"""
        comment_patterns = [
            ".p-commit a",
            ".comment a",
            ".evaluate a",
            ".count",
            ".comment-num",
            ".comment-con",
            ".evaluate-count"
        ]

        comments = self.extract_with_patterns(comment_patterns)

        # 正则表达式提取评论数
        if not comments:
            comment_patterns_re = [
                r'评价(\d+)',
                r'(\d+)条评价',
                r'comment:\s*"(\d+)"',
                r'已有(\d+)人评价',
                r'(\d+)人评价'
            ]
            for pattern in comment_patterns_re:
                matches = re.findall(pattern, self.html)
                if matches:
                    return f"{matches[0]}条评论"

        return comments or "0条评论"


# 京东爬虫主类
class JDCrawler:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None
        self.structure_detector = None
        self.debug_info_saved = False

    def init_driver(self):
        """初始化浏览器驱动"""
        edge_options = Options()

        # 反检测设置
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--lang=zh-CN")
        edge_options.add_argument("--disable-web-security")
        edge_options.add_argument("--allow-running-insecure-content")

        # 伪装真实浏览器
        edge_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)

        # 创建服务并启动浏览器
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Edge(service=service, options=edge_options)
        self.driver.set_page_load_timeout(60)

        # 隐藏自动化特征
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.navigator.chrome = {
                    runtime: {},
                };
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            '''
        })

    def open_jd(self):
        """打开京东并等待加载完成"""
        print("正在打开京东搜索页面...")
        # 直接打开搜索页面，避免首页加载问题
        self.driver.get("https://search.jd.com/Search?keyword=笔记本电脑")
        print("✅ 京东搜索页面已打开")

        # 等待页面完全加载
        print("等待页面完全加载...")
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("✅ 页面加载完成")

        # 初始化页面结构检测器
        self.structure_detector = JDStructureDetector(self.driver)

        # 模拟人类行为触发完整加载
        print("模拟人类行为触发完整加载...")
        window_size = self.driver.get_window_size()
        for _ in range(3):
            x = random.randint(0, window_size['width'])
            y = random.randint(0, window_size['height'])
            self.driver.execute_script(f"window.scrollTo({x}, {y});")
            time.sleep(random.uniform(0.3, 1.0))

        human_scroll(self.driver, 800)
        time.sleep(1)
        human_scroll(self.driver, 0)
        time.sleep(1)
        print("✅ 模拟行为完成")

    def wait_for_user_action(self):
        """等待用户操作"""
        print("\n" + "=" * 70)
        print("请手动完成以下操作:")
        print("1. 如果需要，请登录账号")
        print("2. 如果需要，请修改搜索内容")
        print("=" * 70 + "\n")

        input("完成以上操作后，按回车键继续执行搜索...")

        # 重新初始化页面结构检测器
        self.structure_detector = JDStructureDetector(self.driver)

    def ensure_search_page(self, default_search="笔记本电脑"):
        """确保当前在搜索结果页面"""
        current_url = self.driver.current_url
        print(f"当前URL: {current_url}")

        # 检测是否已在搜索结果页面
        if self.structure_detector.is_search_page():
            print("✅ 已经在搜索结果页面")
            return True

        # 尝试定位搜索框
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "key"))
            )
            print("✅ 找到搜索框")

            # 获取搜索词或使用默认值
            search_term = search_box.get_attribute('value').strip()
            if not search_term:
                search_term = default_search
                print(f"⚠️ 未检测到搜索内容，使用默认搜索词'{search_term}'")
                search_box.clear()
                human_type(search_box, search_term)
            else:
                print(f"✅ 检测到搜索内容: {search_term}")

            # 执行搜索
            print("正在执行搜索...")
            search_box.send_keys(Keys.RETURN)
            print("✅ 搜索已完成")

            # 等待搜索页面加载
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#J_goodsList, .goods-list, .gl-warp"))
            )
            print("✅ 商品列表容器已加载")

            # 重新初始化页面结构检测器
            self.structure_detector = JDStructureDetector(self.driver)
            return True
        except:
            print("❌ 无法定位搜索框或搜索结果未加载")
            self.save_debug_info("search_error")
            return False

    def locate_products(self):
        """定位商品元素"""
        print("\n" + "=" * 70)
        print("定位商品元素...")
        print("=" * 70)

        # 检测页面类型
        page_type = self.structure_detector.detect_page_type()
        print(f"检测到页面类型: {page_type}")

        # 执行滚动确保所有商品加载
        print("执行滚动确保所有商品加载...")

        # 滚动到页面底部并返回顶部，确保加载所有商品
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # 模拟人类滚动行为
        scroll_position = human_scroll(self.driver, 1500)
        time.sleep(1)
        scroll_position = human_scroll(self.driver, scroll_position + 1000)
        time.sleep(1)
        scroll_position = human_scroll(self.driver, scroll_position + 1000)
        time.sleep(1)

        # 等待商品列表加载
        print("等待商品列表加载...")
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-item, .goods-item, .j-sku-item"))
            )
            print("✅ 商品元素已加载")
        except:
            print("⚠️ 商品元素加载超时，继续尝试定位")

        # 尝试定位商品容器
        container = self.structure_detector.detect_search_container()
        product_selector = self.structure_detector.detect_product_pattern()

        products = []

        if container and product_selector:
            print(f"✅ 找到商品容器，使用选择器: {product_selector}")
            try:
                products = container.find_elements(By.CSS_SELECTOR, product_selector)
                if products:
                    print(f"在容器内找到 {len(products)} 个商品")
            except:
                print(f"❌ 无法在容器内找到商品元素")

        if not products and product_selector:
            print(f"✅ 直接使用选择器查找商品: {product_selector}")
            try:
                products = self.driver.find_elements(By.CSS_SELECTOR, product_selector)
                if products:
                    print(f"直接找到 {len(products)} 个商品")
            except:
                print(f"❌ 无法找到商品元素")

        # 最后尝试：使用通用商品特征查找
        if not products:
            print("⚠️ 使用通用商品特征查找...")
            try:
                # 查找包含价格元素的商品
                price_elements = self.driver.find_elements(By.XPATH,
                                                           "//*[contains(text(), '¥') or contains(text(), '￥') or contains(text(), '元') or contains(text(), '价格')]")
                print(f"找到 {len(price_elements)} 个价格元素")

                for price_elem in price_elements:
                    # 向上查找商品容器
                    product = self.find_product_container(price_elem)
                    if product and product not in products:
                        # 验证是否是真实商品（排除非商品元素）
                        html = product.get_attribute('outerHTML')
                        if "商品" in html or "item" in html or "product" in html:
                            products.append(product)

                if products:
                    print(f"✅ 通过价格元素找到 {len(products)} 个商品")
            except Exception as e:
                print(f"通用查找失败: {str(e)}")

        return products

    def find_product_container(self, element):
        """向上查找商品容器"""
        # 向上查找最多8层
        current = element
        for _ in range(8):
            try:
                current = current.find_element(By.XPATH, "./..")
                classes = current.get_attribute("class") or ""
                tag = current.tag_name.lower()

                # 检查常见商品特征
                if ("item" in classes or "product" in classes or "sku" in classes or
                        "pro" in classes or "goods" in classes):
                    return current

                # 检查是否包含图片元素
                images = current.find_elements(By.TAG_NAME, "img")
                if images:
                    return current

                # 检查是否包含商品链接
                links = current.find_elements(By.TAG_NAME, "a")
                if links and any("item.jd.com" in link.get_attribute("href") for link in links):
                    return current
            except:
                break
        return element

    def extract_product_info(self, products, max_products=5):
        """提取商品信息"""
        if not products:
            print("❌ 无法定位任何商品元素")
            self.save_debug_info("no_products")
            return False

        # 只获取前N个商品
        products = products[:max_products] if len(products) > max_products else products

        print(f"\n✅ 成功定位到 {len(products)} 个商品，开始提取信息...")
        print("=" * 70)

        for i, product in enumerate(products, 1):
            try:
                # 确保商品在视图中可见
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           product)
                time.sleep(0.5)

                # 创建智能提取器
                extractor = SmartProductExtractor(product)

                # 提取商品信息
                name = extractor.extract_name()
                price = extractor.extract_price()
                shop = extractor.extract_shop()
                comments = extractor.extract_comments()

                # 显示结果
                name_display = name[:50] + '...' if len(name) > 50 else name
                print(f"{i}. {name_display}")
                print(f"   价格: {price}")
                print(f"   店铺: {shop}")
                print(f"   评论: {comments}")
                print("-" * 70)

                # 保存商品HTML以便调试
                with open(f"product_{i}.html", "w", encoding="utf-8") as f:
                    f.write(extractor.html)
                print(f"✅ 已保存商品{i}的HTML: product_{i}.html")
            except Exception as e:
                print(f"{i}. 获取商品信息失败: {str(e)}")
                print(traceback.format_exc())

        return True

    def save_debug_info(self, prefix="debug"):
        """保存调试信息"""
        if self.debug_info_saved:
            return ""

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        debug_id = f"{prefix}_{timestamp}"

        try:
            # 保存截图
            self.driver.save_screenshot(f"{debug_id}.png")
            print(f"✅ 已保存截图: {debug_id}.png")

            # 保存页面源代码
            page_source = self.driver.page_source
            with open(f"{debug_id}.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            print(f"✅ 已保存页面源代码: {debug_id}.html")

            # 保存当前URL和标题
            with open(f"{debug_id}.txt", "w", encoding="utf-8") as f:
                f.write(f"URL: {self.driver.current_url}\n")
                f.write(f"Title: {self.driver.title}\n")

            self.debug_info_saved = True
            return debug_id
        except Exception as e:
            print(f"保存调试信息失败: {str(e)}")
            return ""

    def run(self):
        """运行爬虫"""
        try:
            # 初始化浏览器
            self.init_driver()

            # 打开京东搜索页面（直接打开避免首页问题）
            self.open_jd()

            # 等待用户操作（主要是登录）
            self.wait_for_user_action()

            # 确保在搜索结果页面
            if not self.ensure_search_page():
                print("❌ 无法确保在搜索结果页面，爬取终止")
                return

            # 定位商品
            products = self.locate_products()

            # 提取商品信息
            self.extract_product_info(products)

            print("\n✅ 爬取流程完成!")

        except Exception as e:
            print(f"❌ 程序运行出错: {str(e)}")
            print(traceback.format_exc())
            self.save_debug_info("error")

        finally:
            if self.driver:
                input("\n按回车键关闭浏览器...")
                self.driver.quit()
                print("✅ 浏览器已关闭")


# 主函数
def main():
    # 确保驱动路径正确
    if not os.path.exists(EDGE_DRIVER_PATH):
        print(f"❌ 错误: 未找到Edge驱动: {EDGE_DRIVER_PATH}")
        print("请下载并放置驱动到指定位置: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        input("按回车退出...")
        return

    print(f"✅ 使用Edge驱动: {EDGE_DRIVER_PATH}")

    # 创建并运行爬虫
    crawler = JDCrawler(EDGE_DRIVER_PATH)
    crawler.run()


if __name__ == "__main__":
    main()