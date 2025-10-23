
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

def complex_calculation(a, b):
    # 获取当前函数名用于日志
    func_name = complex_calculation.__name__
    logging.debug(f"在函数 {func_name} 中开始计算")

    try:
        result = a / b
        logging.debug(f"函数 {func_name} 计算完成")
        return result
    except Exception as e:
        logging.error(f"函数 {func_name} 中发生错误: {e}")
        raise

complex_calculation(10, 2)

