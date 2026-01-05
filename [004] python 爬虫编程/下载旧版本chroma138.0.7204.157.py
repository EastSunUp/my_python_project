
# Python 下载助手 (保存到当前目录)
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# 创建禁用更新的注册表项
import winreg as reg

version = "138.0.7204.157"
def download_chrome(ver):
    url = f"https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F{ver}%2Fchrome-win.zip?alt=media"

    with requests.get(url, stream=True) as r:
        with open("chrome-old.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print("下载完成,请解压使用!")

def ban_auto_update():
    key_path = r"SOFTWARE\Policies\Google\Chrome"
    try:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, key_path)
        reg.SetValueEx(key, "UpdateDefault", 0, reg.REG_DWORD, 0)
        reg.SetValueEx(key, "AutoUpdateCheckPeriodMinutes", 0, reg.REG_DWORD, 0)
        print("✅ 已禁用Chrome自动更新")
    except Exception as e:
        print(f"需要管理员权限: {str(e)}")

def check_version():
    # 检查降级后的版本(检擦浏览器版本与chromedriver版本是否匹配)
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\path\to\old\chrome.exe"  # 指向旧版

    driver = webdriver.Chrome(
        executable_path="C:/path/to/chromedriver_138.0.7204.157.exe",   # 指向旧版
        options=options
    )

    print("当前精确版本:", driver.capabilities['browserVersion'])
    # 应输出: 138.0.7204.157

def test_version_compatbility():
    # 指定你已有的 chromedriver 路径
    driver_path = "F:\My_python_project\chromedriver.exe"
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.google.com")
        print("✅ 成功使用 Chromedriver 138.0.7204.157 驱动 Chrome 138.0.7204.158")

        # 验证浏览器版本
        print("浏览器版本:", driver.capabilities['browserVersion'])
        print("驱动版本:", driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        print("尝试以下解决方案...")

test_version_compatbility()
# download_chrome(ver=version)    # 步骤一: 下载旧版本的chrome浏览器
# ban_auto_update()               # 步骤二: 禁止chrome浏览器自动更新
# check_version()                 # 步骤三: 检查校验安装后的chrome浏览器版本


