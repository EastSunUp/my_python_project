import time
import webbrowser
import os
from selenium import webdriver
from selenium.webdriver.edge import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options

# session cookie 会话 Set-Cookie设置详解: https://blog.csdn.net/zp357252539/article/details/147744097
# https://mobile.yangkeduo.com/goods.html?goods_id=62262510595
# 多多客开源项目: https://gitee.com/doodooke/doodoo
# 拼多多开发者开放平台: https://open.pinduoduo.com/application/home?redirectUrl=https%3A%2F%2Fopen.pinduoduo.com%2Fapplication%2Fmessage
# 拼多多接口介绍: https://zhuanlan.zhihu.com/p/644748353
# 拼多多接口官网说明文档网址(商品API): https://open.pinduoduo.com/application/document/api?id=pdd.mall.info.get
# Microsoft Edge WebDriver下载网址: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads
# Selenium网址: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/#sessionnotcreatedexception
# 豆瓣网网址: https://movie.douban.com/top250?start=0&filter=
# 目标URL
goods_id_list = ["62262510595","735163618154","734680521746",
                 "398739256384","619171793481"]  # 增加替换为您的商品ID:  239952789828

# 指定Microsoft Edge的安装路径 (常见路径)
edge_paths = [
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]


# 获取Edge驱动路径 --------------------------------------------------------------------------
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

    print("找不到msedgedriver !")
    '''
        # 如果找不到，尝试从网络下载
        print("⚠️ 未找到msedgedriver,尝试自动下载...")
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            return EdgeChromiumDriverManager().install()
        except ImportError:
            print("❌ 请先安装webdriver-manager: pip install webdriver-manager")
            return None
    '''

edge_driver_path = get_edge_driver_path()
if not edge_driver_path:
    print("❌ 无法找到或下载Microsoft Edge WebDriver")
# 配置Edge选项
edge_options = Options()
# 在可视化模式下保持浏览器打开直到手动关闭
edge_options.add_experimental_option("detach", True)
# 设置浏览器driver
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# 尝试找到有效的Edge路径
valid_path = None
for path in edge_paths:
    if os.path.exists(path):
        valid_path = path
        print(f'edge_paths: {valid_path}')
        break


enter_ask = True    # 默认进行回车咨询.
for goods_id in goods_id_list:
    target_url = f'https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}'
    print(f"正在打开商品:{goods_id}网址!")
    if enter_ask is True:
        while True:
            # 回车输入咨询
            user_input_1 = input("请输入回车键以继续")
            # 询问是否关闭回车咨询
            user_input_2 = input("是否继续保留输入查询动作?y/n")
            # 检测回车键: 空字符串表示只按了回车
            if user_input_2.lower() == "y":
                print("检测到回车键,程序继续执行！")
                enter_ask = True
                break
            elif user_input_2.lower() == "n":
                enter_ask = False
                break
            elif user_input_1 =='':
                break
            elif user_input_1 != '':
                print(f"您的输入内容: '{user_input_2}'")
                print("您没有输入回车键盘,输入无效!")
                continue
            else:
                print(f"您的输入内容: '{user_input_2}'")
                print("输入无效,请输入 y或n 以决定是否进行回车咨询动作!")
                continue
    if valid_path:
        # 注册浏览器路径
        webbrowser.register('edge', None, webbrowser.BackgroundBrowser(valid_path))
        # 使用Edge打开网址
        webbrowser.get('edge').open(target_url)
    else:
        print("Microsoft Edge未找到,尝试使用默认浏览器打开!")
        webbrowser.open(target_url)

    # 防止被识别到爬虫,反反爬识别延时.
    time.sleep(2)
    # 在方案1的try块中添加：
    try:
        WebDriverWait(driver, 60).until(
            lambda d: "refer_page_name=login" in d.current_url
        )
        print("检测到登录参数:", driver.current_url)
    except TimeoutError:
        print("未检测到登录参数")
print(f"本次共打开{len(goods_id_list)}个网址!")
