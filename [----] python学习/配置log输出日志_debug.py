
import logging
import os
import sys

# 配置日志 - 使用 UTF-8 编码解决字符问题
def configure_logging():
    # 创建 UTF-8 编码的文件处理器
    file_handler = logging.FileHandler('proxy_browser.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 配置主日志器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

# 配置报错信息(用于代码运行时的模拟仿真用)
mitm_path = "mitmproxy路径: 未知路径?"
error_info = "未定义错误类型"
port = "8888"
debug_info = "未定义debug_info!"

# 定义logger对象
logger = configure_logging()
# logger 有三种级别类型的输出日志报错说明
logger.info("mitmproxy 已安装: %s", mitm_path)
logger.error("检查 mitmproxy 时出错: %s", error_info)    # str(e)
logger.debug("端口 %d 不可用: %s", port, debug_info)    # str(e)