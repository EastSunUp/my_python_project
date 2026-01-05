from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time
import os
import random

'''
# 设置Chrome选项
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 最大化窗口
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示

'''
# TODO 这份代码已经不管用了,好用了一天不到,目前京东的封禁策略暂时未知..
# 使用WebDriver Manager自动管理驱动（需先安装：pip install webdriver-manager）
from webdriver_manager.chrome import ChromeDriverManager

# # 初始化浏览器
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()),
#     options=options
# )

# self
def get_real_edge_user_agent():
    """获取当前系统的真实Edge User-Agent"""
    try:
        # 方法1: 通过注册表获取版本号
        result = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version',
            shell=True
        )
        version = result.decode().split()[-1]
        return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{version}"
    except:
        # 方法2：默认值（2025年7月最新）
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/125.0.0.0"


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

# 随机User-Agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
]
# 配置options()
# edge_options = webdriver.EdgeOptions()
edge_options = Options()
# 在Edge选项设置中添加以下修改(关闭web安全模式) # 2025/07/24 日新增
# edge_options.add_argument("--disable-web-security")
# edge_options.add_argument("--disable-site-isolation-trials")  # 禁用同源策略（危险特征）
# edge_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
# edge_options.add_argument("--disable-blink-features=AutomationControlled")
# 忽略安全证书相关内容、运行运行不安全内容
# edge_options.add_argument('--ignore-certificate-errors')
# edge_options.add_argument('--allow-running-insecure-content')
# 禁用自动化特征
edge_options.add_argument("--disable-blink-features=AutomationControlled")
# edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# edge_options.add_experimental_option('useAutomationExtension', False)
# 添加反检测参数 (即使未用无头模式也要添加)
# edge_options.add_argument('--disable-infobars')
edge_options.add_argument('--disable-gpu')    # 禁用GPU加速
edge_options.add_argument('--no-sandbox')
# 基本反检测设置
# edge_options.add_argument("--disable-blink-features=AutomationControlled")
# edge_options.add_argument('--disable-infobars')
# edge_options.add_argument('--disable-gpu')
# edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')
# 反自动化检测
# edge_options.add_argument('--disable-popup-blocking')
# edge_options.add_argument('--disable-notifications')
# edge_options.add_argument('--disable-background-networking')
# edge_options.add_argument('--disable-background-timer-throttling')
# edge_options.add_argument('--disable-client-side-phishing-detection')
# edge_options.add_argument('--disable-component-update')
# edge_options.add_argument('--disable-default-apps')
# edge_options.add_argument('--disable-domain-reliability')
# edge_options.add_argument('--disable-sync')
# edge_options.add_argument('--metrics-recording-only')
# edge_options.add_argument('--safebrowsing-disable-auto-update')
# edge_options.add_argument('--password-store=basic')
# edge_options.add_argument('--use-mock-keychain')
# edge_options.add_argument('--disable-session-crashed-bubble')
# 窗口设置
# edge_options.add_argument("--window-size=1200,800")
edge_options.add_argument("--start-maximized")
# 语言和位置设置
edge_options.add_argument("--lang=zh-CN")
# edge_options.add_argument("--geolocation=china")
# 添加真实用户配置文件
# edge_options.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default")
# edge_options.add_argument("profile-directory=Default")
# 获取电脑真实的user-agent
user_agent=get_real_edge_user_agent()
# 指定user-agent  # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
# edge_options.add_argument(f"--user-agent={user_agent}") # {user_agent} # random.choice(user_agents)
# 在可视化模式下保持浏览器打开直到手动关闭
edge_options.add_experimental_option("detach", True)
# 使用IP代理轮换(暂时不使用这个技术)
# edge_options.add_argument("--proxy-server=http://your-proxy-ip:port")

# 查找edge_driver路径
edge_driver_path = get_edge_driver_path()
if not edge_driver_path:
    print("❌ 无法找到或下载Microsoft Edge WebDriver")
    # return False
# 设置浏览器driver
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

"""
# 执行JavaScript隐藏自动化特征
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 设置广州番禺区地理位置
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": 22.9378,
    "longitude": 113.3540,
    "accuracy": 50
})

# 设置时区
driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": "Asia/Shanghai"})

# 设置本地化信息
driver.execute_cdp_cmd("Emulation.setLocaleOverride", {"locale": "zh-CN"})

"""

'''
# 使用真实浏览器指纹
driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {
    'timezoneId': 'Asia/Shanghai'
})

# 在浏览器启动后执行这些脚本
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        // 隐藏WebDriver特征
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // 伪装进程列表
        const originalQuery = window.Query;
        window.Query = function(selector) {
            if(selector === 'process') {
                return [
                    {name: 'System.exe', pid: 1001},
                    {name: 'explorer.exe', pid: 1002},
                    {name: 'svchost.exe', pid: 1003}
                ];
            }
            return originalQuery.apply(this, arguments);
        };

        // 伪装端口连接
        window.originalFetch = window.fetch;
        window.fetch = function(url, options) {
            if(url.includes('localhost') && url.includes('9515')) {
                return new Promise(resolve => resolve({
                    json: () => ({}),
                    text: () => "",
                    status: 404
                }));
            }
            return window.originalFetch(url, options);
        };
    """
})

# 修改浏览器性能特征
driver.execute_cdp_cmd("Performance.enable", {})
# driver.execute_cdp_cmd("Performance.setTimeDomain", {
#     "timeDomain": "timeTicks"
# })

# 注入WebDriver隐藏脚本
driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    // 删除所有自动化标志
                    const newProto = navigator.__proto__;
                    delete newProto.webdriver;
                    navigator.__proto__ = newProto;

                    // 模拟 localStorage 和 sessionStorage
                    if (!window.localStorage) {
                        window.localStorage = {
                            getItem: function() { return null; },
                            setItem: function() {},
                            removeItem: function() {},
                            clear: function() {},
                            length: 0
                        };
                    }
                    if (!window.sessionStorage) {
                        window.sessionStorage = {
                            getItem: function() { return null; },
                            setItem: function() {},
                            removeItem: function() {},
                            clear: function() {},
                            length: 0
                        };
                    }

                    // 修改插件数组
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [{
                            name: 'Chrome PDF Plugin',
                            filename: 'internal-pdf-viewer',
                            description: 'Portable Document Format',
                            '0': {
                                type: 'application/pdf',
                                suffixes: 'pdf',
                                description: 'Portable Document Format'
                            }
                        }],
                        configurable: true
                    });

                    // 修改语言属性
                    Object.defineProperty(navigator, 'language', {
                        get: () => 'zh-CN',
                        configurable: true
                    });

                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['zh-CN', 'zh'],
                        configurable: true
                    });

                    // 修改屏幕属性
                    Object.defineProperty(screen, 'width', {
                        get: () => 1920,
                        configurable: true
                    });

                    Object.defineProperty(screen, 'height', {
                        get: () => 1080,
                        configurable: true
                    });

                    // 修改硬件并发数
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 4,
                        configurable: true
                    });

                    // 修改WebGL属性
                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) {
                            return 'Google Inc. (NVIDIA)';
                        }
                        if (parameter === 37446) {
                            return 'NVIDIA GeForce RTX 3080/PCIe/SSE2';
                        }
                        return getParameter(parameter);
                    };

                    // 修改Canvas指纹
                    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
                    HTMLCanvasElement.prototype.toDataURL = function(type, ...args) {
                        if (type === 'image/webp') {
                            return toDataURL.call(this, 'image/jpeg', ...args);
                        }
                        return toDataURL.call(this, type, ...args);
                    };

                    // 修改音频指纹
                    const oldGetChannelData = AudioBuffer.prototype.getChannelData;
                    AudioBuffer.prototype.getChannelData = function() {
                        const result = oldGetChannelData.apply(this, arguments);
                        // 添加微小扰动
                        for (let i = 0; i < result.length; i += 100) {
                            result[i] += 0.0001 * Math.random();
                        }
                        return result;
                    };

                    // 覆盖其他自动化检测点
                    window.navigator.chrome = {
                        runtime: {},
                        // 添加其他属性
                    };

                    // 覆盖permissions属性
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );

                    // 覆盖driver属性
                    Object.defineProperty(window, 'driver', {
                        value: undefined,
                        writable: false
                    });

                    // 覆盖selenium属性
                    Object.defineProperty(window, 'selenium', {
                        value: undefined,
                        writable: false
                    });

                    // 覆盖$cdc_asdjflasutopfhvcZLmcfl_属性
                    Object.defineProperty(document, '$cdc_asdjflasutopfhvcZLmcfl_', {
                        value: undefined,
                        writable: false
                    });

                    // 覆盖京东特定的检测点
                    Object.defineProperty(window, '__$jdc', {
                        value: undefined,
                        writable: false
                    });

                    // 覆盖京东的检测变量
                    Object.defineProperty(window, 'JD_Detection', {
                        value: undefined,
                        writable: false
                    });

                    // 覆盖常见的自动化检测点
                    Object.defineProperty(window, '_Selenium_IDE_Recorder', {
                        value: undefined,
                        writable: false
                    });
                """
            }
        )
# 禁用自动化特征
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})
# 使用CDP命令覆盖自动化特征
driver.execute_cdp_cmd("Network.setUserAgentOverride", {
    "userAgent": user_agent,
    "platform": "Win32"
})

driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": False})
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": 39.9042,
    "longitude": 116.4074,
    "accuracy": 100
})

driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": "Asia/Shanghai"})
driver.execute_cdp_cmd("Emulation.setLocaleOverride", {"locale": "zh-CN"})


'''

"""
# 设置更真实的屏幕参数
driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
    "width": 1920,
    "height": 1080,
    "deviceScaleFactor": 1,
    "mobile": False,
    "screenOrientation": {
        "angle": 0,
        "type": "portraitPrimary"
    }
})

# 只保留核心反检测功能
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        // 核心反检测脚本
        delete navigator.webdriver;

        // 设置中国标准时间
        try {
            Intl.DateTimeFormat().resolvedOptions().timeZone = 'Asia/Shanghai';
        } catch (e) {}
    '''
})
"""


"""
# 执行反检测脚本内容
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        // 广州番禺区时区设置
        try {
            Intl.DateTimeFormat().resolvedOptions().timeZone = 'Asia/Shanghai';
        } catch (e) {}
    
        // 核心反检测脚本
        delete navigator.webdriver;

        // 更安全的插件模拟
        const originalPlugins = navigator.plugins;
        Object.defineProperty(navigator, 'plugins', {
            get: () => originalPlugins.length > 0 ? originalPlugins : [{
                name: 'Microsoft Edge PDF Viewer',
                filename: 'internal-pdf-viewer',
                description: 'Portable Document Format'
            }],
            configurable: false
        });

        //Object.defineProperty(navigator, 'plugins', {
        //    get: () => [1, 2, 3],
        //});
        //Object.defineProperty(navigator, 'languages', {
        //    get: () => ['zh-CN', 'zh'],
        //});

        //window.navigator.chrome = { runtime: {} };
        // 改进的chrome属性处理
        if (!navigator.chrome) {
            Object.defineProperty(navigator, 'chrome', {
                value: {
                    runtime: {},
                    app: { isInstalled: false },
                    webstore: {},
                    _edge: true,
                    _edgeVersion: '125.0.0.0'
                },
                configurable: true,
                enumerable: true
            });

        // 语言设置
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en-US', 'en'],
            configurable: false
        });

        // Object.defineProperty(navigator, 'msMaxTouchPoints', {get: () => undefined});
        // Object.defineProperty(navigator, 'msManipulationViewsEnabled', {get: () => undefined});
    '''
})
"""


try:
    time.sleep(random.uniform(2, 3.8))  # 随机等待
    # 打开京东首页
    driver.get("https://www.jd.com")
    print("已打开京东首页...")
    # driver.get("https://www.taobao.com")  #"https://www.jd.com"
    # print("已打开淘宝首页...")
    time.sleep(random.uniform(1.5, 3.8))  # 随机等待
    # 等待结果加载
    time.sleep(5)
    # driver.refresh()
    time.sleep(random.uniform(3, 5))  # 随机等待
    # # 定位搜索框并输入关键词
    # search_box = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "key"))
    # )
    # time.sleep(random.uniform(0.2, 1.5))  # 点击前延迟
    # search_box.clear()
    # search_box.send_keys("笔记本电脑")
    time.sleep(180)
    while True:
        user_input = input("请完成登录后按回车键继续...")
        if user_input == '':
            print("检测到回车键,程序继续执行！")
            break
        else:
            print(f"您输入了: '{user_input}',但程序需要您直接按回车键!")
            continue
    time.sleep(random.uniform(0.2, 1.1))  # 点击前延迟
    # search_box.send_keys(Keys.RETURN)
    print("已搜索'笔记本电脑'...")


    '''
    # 等待结果加载
    time.sleep(5)
    while True:
        user_input = input("请完成登录后按回车键继续...")
        if user_input == '':
            print("检测到回车键,程序继续执行！")
            break
        else:
            print(f"您输入了: '{user_input}',但程序需要您直接按回车键!")
            continue
    '''

    '''
    '''
    # 等待商品列表出现
    WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-item")))
    print("商品列表已加载...")
    time.sleep(random.uniform(1, 3))
    # 获取前5个商品信息
    products = driver.find_elements(By.CSS_SELECTOR, ".gl-item")[:5]

    print("\n=== 搜索结果前3个商品 ===")
    for i, product in enumerate(products, 1):
        try:
            # 获取商品名称
            name = product.find_element(By.CSS_SELECTOR, ".p-name em").text.strip()
            # 获取商品价格
            price = product.find_element(By.CSS_SELECTOR, ".p-price i").text.strip()
            time.sleep(3)
            print(f"商品{i}: {name}")
            print(f"价格: ￥{price}")
            print("-" * 50)
        except:
            print(f"获取第{i}个商品信息失败")

    print("爬取完成!")

finally:
    # 关闭浏览器
    driver.quit()
    print("浏览器已关闭")

