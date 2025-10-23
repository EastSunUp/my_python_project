

import inspect

def my_function(x, y=10):
    """这是一个示例函数"""
    return x + y

# 获取函数名称
print(f"函数名: {my_function.__name__}")

# 获取完整信息
print(f"函数签名: {inspect.signature(my_function)}")
print(f"函数文档: {my_function.__doc__}")
print(f"模块名: {my_function.__module__}")
print(f"限定名: {my_function.__qualname__}")

# 获取源代码（如果可用）
try:
    print(f"源代码: {inspect.getsource(my_function)}")
except OSError:
    print("无法获取源代码")

