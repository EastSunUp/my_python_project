import pyautogui
import time
import webbrowser
import pyperclip
# 以下这个包,用于获取网页源码HTML内容
from playwright.sync_api import sync_playwright
import os

goods_id = 62262510595
target_url = f'https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}'
# 本代码的作用是打开指定url网址的网页,并模拟键盘输入,查看(ctrl+u)查看该网页的页面源代码HTML格式内容
# 打开浏览器并导航到网页
webbrowser.open(target_url) # "https://www.baidu.com"
time.sleep(5)  # 等待浏览器打开

# 等待结果加载
time.sleep(5)
# while True:
#     user_input = input("请完成登录后按回车键继续...")
#     if user_input == '':
#         print("检测到回车键,程序继续执行！")
#         break
#     else:
#         print(f"您输入了: '{user_input}',但程序需要您直接按回车键!")
#         continue

# 模拟按下 Ctrl+U
pyautogui.hotkey('ctrl', 'u')
time.sleep(2)  # 等待源代码加载

# 全选并复制
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'c')
time.sleep(1)  # 确保复制完成

# 获取剪贴板内容
source_code = pyperclip.paste()
print("复制的源代码长度:", len(source_code))
print("前2000个字符:\n", source_code[:1000])
# print("复制的源代码:\n", source_code[:500])

# 关闭网页的几种方式（选择其中一种即可）

# 方式1：关闭当前标签页 (Ctrl+W)
# pyautogui.hotkey('ctrl', 'w')
# pyautogui.hotkey('ctrl', 'w')   # 打开了两个网页,关闭两次
# print("已关闭当前标签页")

# 方式2：关闭整个浏览器窗口 (Alt+F4)
# pyautogui.hotkey('alt', 'f4')
# print("已关闭浏览器窗口")

# 方式3：使用任务管理器关闭特定进程 (更彻底)
# 需要知道浏览器进程名,例如chrome.exe
# import os
# os.system("taskkill /f /im chrome.exe")  # Windows
# os.system("pkill -f chrome")  # Linux/Mac

# 添加额外等待确保操作完成
time.sleep(1)
'''
    # 获取渲染后的HTML网页源码内容
    with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page() # 设置为有头模式
    page.goto(f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}")
    time.sleep(1)
    original_html = page.content()  # 获取渲染后的完整HTML
    browser.close()
'''
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
    import win32com.client  # Windows系统

    # 通过IE浏览器获取 (仅Windows) (获取渲染后的HTML网页源码内容)
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = False
    ie.Navigate(target_url)
    while ie.ReadyState != 4:  # 等待加载完成
        pass
    html = ie.Document.documentElement.outerHTML
    ie.Quit()
'''

