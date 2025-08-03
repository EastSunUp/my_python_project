import json
import os
import time
import random
import subprocess
import pyautogui
import pyperclip
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# TODO 该部分内容代码部分功能欠缺,请有空完成该部分内容的相关代码
goods_id = 62262510595
target_url = f'https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}' # 拼多多网页(手机浏览用的网页)
# target_url ='https://www.jd.com'

# 完整手机设备模拟类
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

    def get_real_edge_user_agent(self):
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

    def get_edge_driver_path(self):
        """获取Edge驱动的路径"""
        # 尝试常见安装位置
        possible_paths = [
            r"C:\Program Files\Microsoft\Edge\Application\msedgriver.exe",  # 这个路径是我自己下载对应的驱动后放置的
            r"F:\My_python_project\msedgedriver.exe",
            os.path.join(os.environ.get("PROGRAMFILES", ""), "Microsoft", "Edge", "Application", "msedgedriver.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Microsoft", "Edge", "Application",
                         "msedgedriver.exe")
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

    def config_mobile_edge(self,options):
        # 关键：启用移动仿真模式
        mobile_emulation = {
            "deviceMetrics": {"width": int(self.device["resolution"].split(',')[0]),
                              "height": int(self.device["resolution"].split(',')[1]),
                              "pixelRatio": float(self.device["pixel_ratio"])},
            "userAgent": self.device["user_agent"]
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        # 其他优化设置
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # 从代理服务商获取IP（以Smartproxy为例）
    def get_proxy(self):
        response = requests.get("https://api.smartproxy.com/v1/endpoint?type=residential")
        return response.json()['proxy']

    def start_browser(self):
        options = Options()
        # edge_options = Options()

        # 在可视化模式下保持浏览器打开直到手动关闭
        options.add_experimental_option("detach", True)

        # 隐藏自动化标志
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # 在Edge选项设置中添加以下修改(关闭web安全模式) # 2025/07/29 日新增
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        # 获取代理IP
        # proxy = self.get_proxy()
        # options.add_argument(f'--proxy-server={proxy}') # 配置代理IP
        # 配置住宅IP  # --proxy-server=http://user:pass@ip:port (使用代理IP技术)
        # options.add_argument('--proxy-server=http://123.45.67.89:8080')   # 先暂时不配置
        # 配置浏览器 (直接配置成真实的电脑浏览器)
        # REAL_UA = self.get_real_edge_user_agent()
        # print(f"使用真实 User-Agent: {REAL_UA}")
        # options = Options()
        # options.add_argument(f"user-agent={REAL_UA}")
        # options.add_argument("--start-maximized") # 哪种启动模式?

        # 基本设备配置
        # options.add_argument(f"user-agent={self.device['user_agent']}")
        # options.add_argument(f"window-size={self.device['resolution']}") # 暂时不配置这个页面大小

        # # 电脑浏览器模拟手机自动化设备配置
        self.config_mobile_edge(options=options) # 暂时不模拟

        # 获取edge浏览器驱动路径
        edge_driver_path = self.get_edge_driver_path()
        if not edge_driver_path:
            print("❌ 无法找到或下载Microsoft Edge WebDriver")
            return False
        # 启动浏览器
        # self.driver = webdriver.Chrome(options=options)
        # 设置浏览器driver
        service = Service(executable_path=edge_driver_path)
        self.driver = webdriver.Edge(service=service, options=options)
        # 彻底移除自动化特征 # 增强指纹隐藏(在CDP命令中添加) # 2025/07/24日新增
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
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

                    // 字体指纹欺骗
                    const originalFonts = window.queryLocalFonts;
                    window.queryLocalFonts = async () => {
                        const fonts = await originalFonts?.();
                        return fonts?.filter(font => 
                            ['Arial', 'Times New Roman', 'Courier New'].includes(font.postscriptName)
                        ) || [];
                    };
                
                    // Canvas指纹干扰
                    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                    HTMLCanvasElement.prototype.toDataURL = function(type, quality) {
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');
                        ctx.fillText('FingerprintProtection', 10, 10);
                        return originalToDataURL.call(this, type, quality);
                    };
                
                   // WebGL指纹干扰
                   const getParameter = WebGLRenderingContext.prototype.getParameter;
                   WebGLRenderingContext.prototype.getParameter = function(parameter) {
                       if (parameter === 37445) return 'Google Inc. (NVIDIA)'; // VENDOR
                       if (parameter === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)'; // RENDERER
                       return getParameter.apply(this, [parameter]);
                   };
                   
                   // AudioContext指纹干扰
                    const originalOscillator = window.OscillatorNode;
                    window.OscillatorNode = class PatchedOscillator extends originalOscillator {
                        constructor(context) {
                            super(context);
                            const realStart = this.start.bind(this);
                            this.start = (when = 0) => {
                                realStart(when + 0.0001 * Math.random());
                            };
                        }
                    };
                    
                    // 屏蔽ResizeObserver等高级API检测
                    window.ResizeObserver = class FakeResizeObserver {
                        observe() {}
                        unobserve() {}
                        disconnect() {}
                    };
                    
                    // 时区与地理位置欺骗
                    Object.defineProperty(Intl, 'DateTimeFormat', {
                        value: class PatchedDateTimeFormat {
                            constructor(locales, options) {
                                options = options || {};
                                options.timeZone = 'Asia/Shanghai';
                                return new Intl.DateTimeFormat(locales, options);
                            }
                        }
                    });
                """
        })
        # 修改JavaScript环境(模拟成手机使用环境)
        # self.modify_js_environment()  # 暂时不模拟手机使用环境

        return self.driver

    def modify_js_environment(self):
        # 覆盖webdriver属性
        self.driver.execute_script("""
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Open Source Technology Center';
                if (parameter === 37446) return 'Mesa DRI Intel(R) HD Graphics';
                return originalGetParameter.call(this, parameter);
            };
            
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            Object.defineProperty(document, 'hidden', {value: false});
            Object.defineProperty(document, 'visibilityState', {value: 'visible'});
            
            window.chrome = {app: {isInstalled: false}, webstore: {}};
            // "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        """
            )

        # 修改navigator属性
        js = f"""
            // 修改平台信息
            Object.defineProperty(navigator, 'platform', {{
                value: '{self.device["platform"]}',
                configurable: false,
                writable: false 
                }});
            
            // 添加设备型号
            Object.defineProperty(navigator, 'deviceModel', {{
                value: '{self.device.get("device_model", "")}',
                configurable: false
            }});
        
            // 模拟电池状态
            navigator.getBattery = function() {{
                return Promise.resolve({{
                    level: {self.device["battery_level"]},
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity
                }});
             }};
            
            // 模拟网络连接
            Object.defineProperty(navigator, 'connection', {{
                get: function() {{
                    return {{
                        downlink: 10,
                        effectiveType: '4g',
                        rtt: 100,
                        saveData: false,
                        type: '{self.device["connection_type"]}'
                    }};
                }}
            }});
            
            // 字体欺骗
            Object.defineProperty(document, 'fonts', {{
                value: new Set({json.dumps(self.device["fonts"])}),
                configurable: false
            }});
        
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: function() {{ return {self.device['hardware_concurrency']}; }}
            }});
            
            Object.defineProperty(navigator, 'deviceMemory', {{
                get: function() {{ return {self.device['device_memory']}; }}
            }});
            
            Object.defineProperty(navigator, 'maxTouchPoints', {{
                get: function() {{ return {self.device['max_touch_points']}; }}
            }});
            
            //修改屏幕大小 - 添加parseInt确保数值类型
            Object.defineProperty(screen, 'width', {{
                get: function() {{ return parseInt('{self.device['resolution'].split(",")[0]}');}}
            }});
            Object.defineProperty(screen, 'height', {{
                get: function() {{ return parseInt('{self.device['resolution'].split(",")[1]}'); }}
            }});
            Object.defineProperty(screen, 'availWidth', {{
                get: function() {{ return parseInt('{self.device['resolution'].split(",")[0]}'); }}
            }});
            Object.defineProperty(screen, 'availHeight', {{
                get: function() {{ return parseInt('{self.device['resolution'].split(",")[1]}'); }}
            }});
            
            // 修改屏幕属性
            Object.defineProperty(screen, 'pixelDepth', {{
                get: function() {{ return {self.device['color_depth']}; }}
            }});
            Object.defineProperty(screen, 'colorDepth', {{
                get: function() {{ return {self.device['color_depth']}; }}
            }});
            Object.defineProperty(window, 'devicePixelRatio', {{
                get: function() {{ return {self.device['pixel_ratio']}; }}
            }});
        """

        self.driver.execute_script(js)

        # 修改语言和时区
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'language', {
                get: function() { return 'zh-CN'; }
            });
            Object.defineProperty(navigator, 'languages', {
                get: function() { return ['zh-CN', 'zh', 'en']; }
            });
    
            const originalResolvedOptions = Intl.DateTimeFormat.prototype.resolvedOptions;
            Intl.DateTimeFormat.prototype.resolvedOptions = function() {
                const result = originalResolvedOptions.apply(this, arguments);
                result.timeZone = 'Asia/Shanghai';
                return result;
            };
        """)

        # 清除自动化痕迹:
        driver.execute_script("""
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        """)

    def close(self):
        if self.driver:
            self.driver.quit()
            print("退出页面")

# 使用示例
simulator = MobileBrowserSimulator("Samsung Galaxy S21")
driver = simulator.start_browser()
# 首次访问不要直接打开目标页面
# driver.get("https://mobile.yangkeduo.com/")
time.sleep(0.5)
driver.get(target_url)    # "https://whatismydevice.com/"
time.sleep(5)  # 等待页面初步加载


'''
# 目前这段代码不能加进去
# 等待用户手动输入回车 -------------------------------------------------
while True:
    user_input = input("请完成登录后按回车键继续...")
    # 检测回车键: 空字符串表示只按了回车
    if user_input == "":
        print("检测到回车键,程序继续执行！")
        break
    else:
        print(f"您输入了: '{user_input}',但程序需要您直接按回车键!")
        continue

time.sleep(30)  # 等待页面切换
print("请确保页面已经切换完成!")

# 模拟按下 Ctrl+U
pyautogui.hotkey('ctrl', 'u')
time.sleep(2)  # 等待源代码加载

# 全选并复制
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'c')
time.sleep(1)  # 确保复制完成

# 拷贝剪切板中的内容,保存为HTML内容
original_html = pyperclip.paste()
# 设置保存路径
save_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(save_dir, f"pdd_goods_{goods_id}_source.html")
with open(save_path, "w", encoding="utf-8") as f:
    # f.write(html_content)
    # 选择使用哪种HTML内容
    # f.write(rendered_html)  # 渲染后的HTML
    f.write(original_html)  # 使用JavaScript获取的HTML

print(f"💾 源码已保存至: {save_path} (大小: {len(original_html) // 1024}KB)")
'''

# 页面操作...
# simulator.close()



