import time
import subprocess
import socket
import requests
import shutil
import os
import sys
import logging
import psutil
import traceback
import winreg
import re
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# 配置日志 - 使用 UTF-8 编码解决字符问题
def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 文件日志 (UTF-8编码)
    file_handler = logging.FileHandler('proxy_browser.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = configure_logging()


# ======== 1. 检查 mitmproxy 是否可用 ========
def is_mitmproxy_installed():
    """检查 mitmproxy 是否安装并可用"""
    try:
        mitm_path = shutil.which("mitmdump")
        if mitm_path:
            logger.info("mitmproxy 已安装: %s", mitm_path)
            return True
        else:
            logger.error("mitmproxy 未找到，请尝试: pip install mitmproxy")
            return False
    except Exception as e:
        logger.error("检查 mitmproxy 时出错: %s", str(e))
        return False


# ======== 2. 检测可用端口 ========
def find_available_port(start_port=8888, max_attempts=10):
    """查找可用的网络端口"""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                logger.info("找到可用端口: %d", port)
                return port
            except OSError as e:
                logger.debug("端口 %d 不可用: %s", port, str(e))
                continue
    logger.error("所有尝试的端口都被占用! 请手动释放端口")
    return None


# ======== 3. 代理测试函数 ========
def test_proxy_connection(port, max_retries=5, retry_delay=2):
    """测试代理连接是否正常，带重试机制"""
    for attempt in range(1, max_retries + 1):
        try:
            # 测试端口连接
            logger.info("尝试连接代理 (尝试 %d/%d)...", attempt, max_retries)
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(5)
            test_socket.connect(("127.0.0.1", port))
            test_socket.close()
            logger.info("代理端口 %d 连接成功", port)

            # 测试 HTTP 请求
            logger.info("测试代理请求 (尝试 %d/%d)...", attempt, max_retries)
            test_response = requests.get(
                "http://httpbin.org/ip",
                proxies={'http': f'http://127.0.0.1:{port}', 'https': f'http://127.0.0.1:{port}'},
                timeout=10
            )
            logger.info("代理测试成功! 返回IP: %s", test_response.json())
            return True
        except Exception as e:
            logger.warning("代理测试失败 (尝试 %d/%d): %s", attempt, max_retries, str(e))
            if attempt < max_retries:
                logger.info("等待 %d 秒后重试...", retry_delay)
                time.sleep(retry_delay)

    logger.error("所有 %d 次代理测试均失败", max_retries)
    return False


def install_mitm_certificate():
    """安装 mitmproxy 证书到系统"""
    try:
        # 获取用户主目录
        home_dir = os.path.expanduser("~")

        # 查找证书文件
        cert_path = os.path.join(home_dir, ".mitmproxy", "mitmproxy-ca-cert.cer")

        if not os.path.exists(cert_path):
            # 尝试不同扩展名的证书
            cert_path = os.path.join(home_dir, ".mitmproxy", "mitmproxy-ca-cert.pem")

        if os.path.exists(cert_path):
            logger.info("找到 mitmproxy 证书: %s", cert_path)
            return cert_path
        else:
            logger.warning("未找到 mitmproxy 证书")
            return None
    except Exception as e:
        logger.error("查找证书时出错: %s", str(e))
        return None


def run_mitmdump(cmd):
    """运行 mitmdump 并处理输出"""
    try:
        # 使用 UTF-8 编码启动进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            universal_newlines=True
        )

        # 等待进程启动
        time.sleep(3)

        if process.poll() is not None:
            # 读取错误输出
            stderr_output = process.stderr.read() if process.stderr else "无错误输出"
            logger.error("mitmdump 启动失败，错误信息:\n%s", stderr_output)
            return None, stderr_output
        else:
            logger.info("mitmdump 进程正在运行...")

            # 检查进程是否实际在监听端口
            port = int(cmd[cmd.index("--listen-port") + 1])
            listening = False

            # 重试检查端口监听状态
            for _ in range(10):  # 增加重试次数
                for conn in psutil.net_connections():
                    if conn.status == 'LISTEN' and conn.laddr.port == port:
                        logger.info("mitmdump 正在监听端口 %d", port)
                        listening = True
                        break
                if listening:
                    break
                time.sleep(1)  # 等待1秒再检查

            if not listening:
                logger.error("mitmdump 进程在运行但未监听指定端口 %d", port)
                # 读取进程输出以获取更多信息
                try:
                    stdout, stderr = process.communicate(timeout=2)
                    if stdout:
                        logger.info("mitmdump 输出:\n%s", stdout)
                    if stderr:
                        logger.error("mitmdump 错误输出:\n%s", stderr)
                except:
                    pass

                process.terminate()
                return None, "进程在运行但未监听端口"

            return process, None
    except Exception as e:
        logger.error("启动 mitmdump 时出错: %s", str(e))
        return None, str(e)


def is_port_in_use(port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return False
        except OSError:
            return True


def kill_processes_using_port(port):
    """结束占用指定端口的进程"""
    try:
        killed = False
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
                try:
                    proc = psutil.Process(conn.pid)
                    logger.info("结束占用端口 %d 的进程: %s (PID: %d)", port, proc.name(), proc.pid)
                    proc.terminate()
                    proc.wait(timeout=5)
                    killed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
                    logger.warning("结束进程时出错: %s", str(e))
        return killed
    except Exception as e:
        logger.error("检查端口占用时出错: %s", str(e))
        return False


def capture_browser_logs(driver):
    """捕获浏览器控制台日志"""
    try:
        logs = driver.get_log('browser')
        if logs:
            logger.info("===== 浏览器控制台日志开始 =====")
            for entry in logs:
                logger.info("[%s] %s", entry['level'], entry['message'])
            logger.info("===== 浏览器控制台日志结束 =====")
        else:
            logger.info("浏览器控制台无日志")
    except Exception as e:
        logger.warning("获取浏览器日志失败: %s", str(e))


def get_edge_version():
    """获取Edge浏览器版本"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        winreg.CloseKey(key)
        return version
    except Exception as e:
        logger.error("获取Edge版本失败: %s", str(e))
        return None


def check_edge_compatibility(edge_driver_path):
    """检查Edge浏览器和驱动版本兼容性"""
    try:
        # 获取浏览器版本
        edge_version = get_edge_version()
        if not edge_version:
            logger.warning("无法获取Edge浏览器版本，跳过兼容性检查")
            return True

        # 获取驱动版本
        driver_version_output = subprocess.check_output(
            [edge_driver_path, "--version"],
            text=True,
            stderr=subprocess.STDOUT
        )
        driver_version = re.search(r'(\d+\.\d+\.\d+\.\d+)', driver_version_output)

        if driver_version:
            driver_version = driver_version.group(1)
            logger.info("Edge 浏览器版本: %s", edge_version)
            logger.info("Edge 驱动版本: %s", driver_version)

            # 简化版本比较 (只比较主版本)
            if edge_version.split('.')[0] != driver_version.split('.')[0]:
                logger.warning("警告: 浏览器和驱动主版本不一致，可能导致兼容性问题!")
                logger.warning(
                    "建议下载匹配版本的驱动: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
                return False
            else:
                logger.info("浏览器和驱动版本兼容")
                return True
        else:
            logger.warning("无法解析驱动版本信息: %s", driver_version_output)
            return True
    except Exception as e:
        logger.error("版本检查失败: %s", str(e))
        return True  # 即使检查失败也继续运行


def test_website(driver, url, name="网站", timeout=60, max_retries=2):
    """测试网站访问，带超时处理和重试机制"""
    for attempt in range(1, max_retries + 1):
        try:
            logger.info("尝试 %d/%d: 访问 %s - %s", attempt, max_retries, name, url)
            start_time = time.time()    # 记录启动时的时间戳

            # 设置页面加载超时
            driver.set_page_load_timeout(timeout)

            # 访问网站
            driver.get(url)

            # 等待页面基本加载
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            load_time = time.time() - start_time
            logger.info("页面加载成功! 耗时: %.2f秒", load_time)
            logger.info("当前URL: %s", driver.current_url)
            logger.info("页面标题: %s", driver.title)

            # 捕获浏览器日志
            capture_browser_logs(driver)

            # 检查是否有错误页面
            if "502" in driver.title or "50" in driver.title:
                logger.warning("检测到错误页面: %s", driver.title)
                continue

            return True
        except TimeoutException:
            logger.error("%s 加载超时 (%d秒)", name, timeout)
        except Exception as e:
            logger.error("访问 %s 时出错: %s", name, str(e))

        # 如果不是最后一次尝试，则等待后重试
        if attempt < max_retries:
            logger.info("等待2秒后重试...")
            time.sleep(2)

    logger.error("所有 %d 次尝试均失败", max_retries)
    return False


def human_like_typing(element, text, min_delay=0.05, max_delay=0.3):
    """模拟人类输入行为"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


def main():
    logger.info("=" * 50)
    logger.info("开始代理浏览器测试")
    logger.info("=" * 50)

    if not is_mitmproxy_installed():
        return 1

    # 查找可用端口
    proxy_port = find_available_port()
    if proxy_port is None:
        return 1

    # 检查端口是否被占用
    if is_port_in_use(proxy_port):
        logger.warning("端口 %d 被占用,尝试结束占用进程...", proxy_port)
        if not kill_processes_using_port(proxy_port):
            logger.error("无法释放端口 %d，请手动关闭占用程序", proxy_port)
            logger.info("Windows 检查命令: netstat -ano | findstr :%d", proxy_port)
            return 1
        time.sleep(1)  # 等待进程结束

    # ======== 启动代理服务器 ========
    logger.info("启动代理服务器(端口:%d)...", proxy_port)

    # 优化 mitmproxy 命令 - 解决502错误问题
    mitm_cmd = [
        "mitmdump",
        "--listen-port", str(proxy_port),
        "--set", "block_global=false",
        "--set", "ssl_insecure=true",
        "--set", "keep_host_header=true",  # 保持主机头
        "--set", "connection_strategy=lazy",  # 延迟连接策略
        "--set", "stream_large_bodies=1",  # 流式传输大文件
        "--set", "flow_detail=0",  # 减少日志输出
        "--set", "http2=false",  # 禁用HTTP/2解决502错误
        "--set", "tls_version_client_min=UNBOUNDED",  # 解决TLS指纹问题
        "--set", "tls_version_server_min=UNBOUNDED",
        "--set", "cipher_suite_client=ALL",  # 允许所有密码套件
        "--no-http2",  # 确保禁用HTTP/2
        "--quiet"  # 静默模式
    ]

    # 启动代理进程
    proxy_process, error_output = run_mitmdump(mitm_cmd)

    if proxy_process is None:
        # 常见错误解决方案
        if error_output and "Address already in use" in error_output:
            logger.error("解决方案: 端口 %d 被占用，请关闭占用程序或更换端口", proxy_port)
            logger.info("检查命令: netstat -ano | findstr :%d", proxy_port)
        elif error_output and "No module named" in error_output:
            logger.error("解决方案: 请运行 'pip install mitmproxy' 重新安装")
        elif error_output and "Permission denied" in error_output:
            logger.error("解决方案: 请以管理员身份运行此脚本")
        else:
            logger.error("请尝试手动运行以下命令查看详细错误:")
            logger.error(" ".join(mitm_cmd))
        return 1

    # 给代理更多时间启动
    logger.info("等待代理完全启动...")
    time.sleep(8)  # 增加等待时间

    # 测试代理连接（带重试）
    if not test_proxy_connection(proxy_port, max_retries=5, retry_delay=3):
        logger.error("代理连接测试失败，终止进程")
        try:
            proxy_process.terminate()
            proxy_process.wait(timeout=5)
        except:
            pass
        return 1

    # ======== 配置浏览器 ========
    EDGE_DRIVER_PATH = r'F:\My_python_project\msedgedriver.exe' # 浏览器driver的路径位置

    # 检查浏览器和驱动版本兼容性
    if not check_edge_compatibility(EDGE_DRIVER_PATH):
        logger.warning("浏览器和驱动版本不兼容，可能影响运行稳定性")

    # 配置浏览器选项
    edge_options = EdgeOptions()

    # 使用无痕模式避免历史记录干扰
    edge_options.add_argument("--inprivate")

    # 使用单一可靠的代理设置方式
    proxy_settings = f'http://127.0.0.1:{proxy_port}'
    edge_options.add_argument(f'--proxy-server={proxy_settings}')
    logger.info("设置浏览器代理: %s", proxy_settings)

    # ========== 关键浏览器参数配置 ==========
    # 安全与证书设置
    edge_options.add_argument('--ignore-certificate-errors')
    edge_options.add_argument('--allow-running-insecure-content')
    edge_options.add_argument('--ignore-ssl-errors')
    edge_options.add_argument('--ignore-certificate-errors-spki-list')
    edge_options.add_argument('--disable-web-security')
    edge_options.add_argument('--allow-insecure-localhost')

    # 性能与资源设置
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-software-rasterizer')
    edge_options.add_argument('--disable-extensions')
    edge_options.add_argument(
        '--disable-features=IsolateOrigins,site-per-process,NetworkService,TranslateUI,BlinkGenPropertyTrees')
    edge_options.add_argument('--disable-site-isolation-trials')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_argument('--disable-infobars')
    edge_options.add_argument('--disable-browser-side-navigation')
    edge_options.add_argument('--disable-renderer-backgrounding')
    edge_options.add_argument('--disable-backgrounding-occluded-windows')
    edge_options.add_argument('--disable-ipc-flooding-protection')
    edge_options.add_argument('--disable-background-timer-throttling')
    edge_options.add_argument('--disable-hang-monitor')

    # 反自动化检测设置
    edge_options.add_argument('--disable-popup-blocking')
    edge_options.add_argument('--disable-notifications')
    edge_options.add_argument('--disable-background-networking')
    edge_options.add_argument('--disable-background-timer-throttling')
    edge_options.add_argument('--disable-client-side-phishing-detection')
    edge_options.add_argument('--disable-component-update')
    edge_options.add_argument('--disable-default-apps')
    edge_options.add_argument('--disable-domain-reliability')
    edge_options.add_argument('--disable-sync')
    edge_options.add_argument('--metrics-recording-only')
    edge_options.add_argument('--safebrowsing-disable-auto-update')
    edge_options.add_argument('--password-store=basic')
    edge_options.add_argument('--use-mock-keychain')
    edge_options.add_argument('--disable-session-crashed-bubble')

    # 功能禁用
    edge_options.add_argument('--disable-3d-apis')
    edge_options.add_argument('--disable-webgl')
    edge_options.add_argument('--disable-accelerated-2d-canvas')
    edge_options.add_argument('--disable-canvas-aa')
    edge_options.add_argument('--disable-2d-canvas-clip-aa')
    edge_options.add_argument('--disable-gl-drawing-for-tests')
    edge_options.add_argument('--disable-accelerated-jpeg-decoding')
    edge_options.add_argument('--disable-accelerated-mjpeg-decode')
    edge_options.add_argument('--disable-accelerated-video-decode')
    edge_options.add_argument('--disable-breakpad')
    edge_options.add_argument('--disable-component-extensions-with-background-pages')
    edge_options.add_argument('--disable-datasaver-prompt')
    edge_options.add_argument('--disable-device-discovery-notifications')
    edge_options.add_argument('--disable-file-system')
    edge_options.add_argument('--disable-ios-physical-web')
    edge_options.add_argument('--disable-local-storage')
    edge_options.add_argument('--disable-speech-api')
    edge_options.add_argument('--disable-translate')
    edge_options.add_argument('--disable-web-media-player-metrics')
    edge_options.add_argument('--no-experiments')
    edge_options.add_argument('--no-pings')
    edge_options.add_argument('--no-service-autorun')
    edge_options.add_argument('--no-wifi')
    edge_options.add_argument('--no-zygote')

    # 其他设置
    edge_options.add_argument('--start-maximized')
    edge_options.add_argument('--disable-automatic-tab-discarding')
    edge_options.add_argument('--disable-partial-raster')
    edge_options.add_argument('--disable-threaded-animation')
    edge_options.add_argument('--disable-threaded-scrolling')
    edge_options.add_argument('--disable-checker-imaging')
    edge_options.add_argument('--disable-image-animation-resync')
    # 需不需要屏蔽下面这条?
    # edge_options.add_argument('--blink-settings=imagesEnabled=false')  # 不要禁用图片
    # 设置用户代理 - 使用最新Edge版本
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    edge_options.add_argument(f'--user-agent={user_agent}')
    # 设置语言
    edge_options.add_argument('--lang=zh-CN')

    # 禁用自动化控制检测
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    # 设置接受不安全证书
    edge_options.set_capability('acceptInsecureCerts', True)
    # 设置页面加载策略为 "eager"（不等待所有资源）
    edge_options.set_capability("pageLoadStrategy", "eager")
    # 启用浏览器日志
    edge_options.set_capability("goog:loggingPrefs", {'browser': 'ALL', 'performance': 'ALL'})

    try:
        # 创建服务对象
        edge_service = Service(executable_path=EDGE_DRIVER_PATH)

        # 创建浏览器实例
        logger.info("启动浏览器...")
        driver = webdriver.Edge(service=edge_service, options=edge_options)
        logger.info("浏览器启动成功")

        # 设置各种超时时间
        driver.set_page_load_timeout(300)  # 5分钟
        driver.set_script_timeout(120)  # 2分钟

        # 隐藏WebDriver特征 - 使用更全面的隐藏方案
        logger.info("注入WebDriver隐藏脚本...")
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

        # 禁用自动化特征
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })

        # 验证浏览器代理设置
        logger.info("验证浏览器代理设置...")
        driver.get("chrome://version")
        time.sleep(2)  # 等待页面加载
        page_source = driver.page_source

        # 检查代理设置是否出现在页面中
        if f"--proxy-server={proxy_settings}" in page_source:
            logger.info("✅ 代理设置已成功应用: %s", proxy_settings)
        else:
            logger.error("❌ 代理设置未正确应用!")
            logger.debug("chrome://version 页面内容: %s", page_source[:500])
            logger.error("请手动检查浏览器代理设置")
            return 1

        # ======== 安装证书 ========
        logger.info("尝试自动安装证书...")
        cert_path = install_mitm_certificate()

        if cert_path:
            logger.info("请手动安装证书: %s", cert_path)
            logger.info("1. 双击证书文件")
            logger.info("2. 选择 '安装证书'")
            logger.info("3. 选择 '本地计算机' > '下一步'")
            logger.info("4. 选择 '将所有证书放入下列存储' > '浏览' > '受信任的根证书颁发机构'")
            logger.info("5. 完成安装后按Enter键继续...")
        else:
            logger.info("无法自动找到证书，请手动下载:")
            logger.info("1. 访问: http://mitm.it")
            logger.info("2. 下载 'Windows Proxy' 证书")
            logger.info("3. 安装到 '受信任的根证书颁发机构'")
            logger.info("4. 完成后按Enter键继续...")

        logger.info("重要提示: 安装完成后,请手动打开浏览器访问以下网站验证:")
        logger.info(" - https://example.com (应显示 'Example Domain')")
        logger.info(" - http://mitm.it (可能出现安全警告，这是正常现象)")
        logger.info("确保example.com没有证书警告后再继续!")

        input("按Enter继续...")

        # 访问空白页确保浏览器就绪
        logger.info("访问空白页确保浏览器就绪...")
        driver.get("about:blank")
        time.sleep(1)

        # ======== 测试代理工作 ========
        logger.info("开始代理测试...")

        # 使用优化的测试函数 - 更换HTTP测试网站解决502问题
        # test_website(driver, "http://httpbin.org/ip", "HTTP测试网站", timeout=60)
        # test_website(driver, "https://example.com", "HTTPS测试网站", timeout=60)
        # 京东网站增加超时时间和重试次数
        # test_website(driver, "https://www.jd.com", "京东网站", timeout=120, max_retries=3)
        '''
        # 添加京东搜索功能测试 - 使用更真实的用户行为
        logger.info("测试京东搜索功能...")
        try:
            # 定位搜索框
            search_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "key"))
            )

            # 清除搜索框并模拟人类输入
            search_box.clear()
            human_like_typing(search_box, "笔记本电脑")

            # 等待1-2秒模拟思考
            time.sleep(random.uniform(1, 2))

            # 定位搜索按钮
            search_button = driver.find_element("xpath", "//button[@class='button']")

            # 使用鼠标移动和点击模拟人类行为
            actions = ActionChains(driver)
            actions.move_to_element(search_button).pause(random.uniform(0.5, 1.5)).click().perform()

            # 等待搜索结果加载
            WebDriverWait(driver, 30).until(
                EC.url_contains("search")
            )

            # 等待页面完全加载
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # 等待商品列表出现
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "J_goodsList"))
            )

            # 检查是否跳转到搜索结果页
            if "search" in driver.current_url and "笔记本电脑" in driver.title:
                logger.info("✅ 京东搜索功能正常")
                # 滚动页面以加载图片
                for i in range(3):
                    driver.execute_script(f"window.scrollTo(0, {500 * (i + 1)});")
                    time.sleep(random.uniform(0.5, 1.5))
            else:
                logger.warning("⚠️ 京东搜索功能可能存在问题，当前URL: %s", driver.current_url)

            # 截图保存搜索结果
            driver.save_screenshot("jd_search_result.png")
            logger.info("已保存搜索结果截图: jd_search_result.png")

        except Exception as e:
            logger.error("京东搜索测试失败: %s", str(e))
            # 尝试备用搜索方法
            try:
                logger.info("尝试备用搜索方法...")
                driver.get("https://search.jd.com/Search?keyword=笔记本电脑")

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "J_goodsList"))
                )

                # 滚动加载图片
                for i in range(3):
                    driver.execute_script(f"window.scrollTo(0, {500 * (i + 1)});")
                    time.sleep(1)

                logger.info("备用搜索方法成功")
            except Exception as fallback_e:
                logger.error("备用搜索方法也失败: %s", str(fallback_e))
        '''

        # logger.info("测试淘宝网页的加载功能...")   # https://movie.douban.com/
        # test_website(driver, "https://www.taobao.com", "淘宝网站", timeout=120, max_retries=3)
        logger.info("测试豆瓣网,电影的加载功能...")
        test_website(driver, "https://movie.douban.com/", "淘宝网站", timeout=120, max_retries=3)
        # 添加手动测试点
        logger.info("测试完,您可以手动操作浏览器进行验证...")
        logger.info("按Enter键继续关闭程序...")
        input()

    except Exception as e:
        logger.error("发生错误: %s", str(e))
        logger.error(traceback.format_exc())
        return 1
    finally:
        logger.info("关闭浏览器...")
        try:
            if 'driver' in locals() and driver:
                driver.quit()
                logger.info("浏览器已关闭")
        except Exception as e:
            logger.warning("关闭浏览器时出错: %s", str(e))

        logger.info("停止代理服务器...")
        try:
            if proxy_process:
                proxy_process.terminate()
                proxy_process.wait(timeout=5)
                logger.info("代理服务器已停止")
        except Exception as e:
            logger.warning("停止代理服务器时出错: %s", str(e))

        logger.info("程序结束")
        logger.info("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())