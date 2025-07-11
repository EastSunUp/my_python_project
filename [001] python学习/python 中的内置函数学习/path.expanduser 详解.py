
'''
关于os.path.expanduser("~/Downloads")的解释说明:
    # 当你在代码中写:
    self.save_path = os.path.expanduser("~/Downloads")

    实际上路径已经被正确设置了,只是你看不到它,因为:
        Python变量存储的是字符串,不是实际路径.
        self.save_path 存储的是类似 "C:/Users/你的用户名/Downloads" 的文本
        除非你主动打印它，否则在IDE中不会直观显示
    代码编辑器只显示变量名,不显示内容
        # 在编辑器中你看到的是：
        self.save_path = ...  # 看不到实际值
        # 实际内存中存储的是：
        self.save_path = "C:/Users/zhangsan/Downloads"  # 但你看不到这个
'''

import os

class SetMyFilePath(object):

    def __init__(self):
        self.save_path = os.path.expanduser("~/Downloads")
        pass

    def check_the_path(self):
        # 设置路径
        self.save_path = os.path.expanduser("~/Downloads")
        # 打印验证
        print("下载路径设置为:", self.save_path)  # 关键！查看实际路径
        print("路径是否存在?", os.path.exists(self.save_path))  # 检查物理存在

'''
    # 使用更可靠方法下载目录
    from pathlib import Path

    # 方法1：直接拼接
        downloads_path = Path.home() / "Downloads"
    
    # 方法2：兼容不同语言系统（Windows）
        if os.name == 'nt':  # Windows系统
            import ctypes
            buf = ctypes.create_unicode_buffer(1024)
            ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)  # 5代表Downloads
            self.save_path = buf.value
        else:
            self.save_path = os.path.expanduser("~/Downloads")
    
'''

'''
# 正确使用示例
import os
from pathlib import Path

class FileDownloader:
    def __init__(self):
        # 设置下载路径
        self.save_path = os.path.expanduser("~/Downloads")
        
        # 自动创建目录（如果不存在）
        os.makedirs(self.save_path, exist_ok=True)
        
        # 验证路径
        print(f"文件将保存到: {self.save_path}")
        print(f"目录内容示例: {os.listdir(self.save_path)[:3]}")  # 显示前3个文件

# 使用示例
downloader = FileDownloader()
'''
# 如果该页作为主程序运行时,则运行下面这段代码:
if __name__== "__main__":
    Run=SetMyFilePath()
    Run.check_the_path()




