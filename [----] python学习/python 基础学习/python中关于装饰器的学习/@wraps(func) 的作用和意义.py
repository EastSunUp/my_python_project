
"""
@wraps(func) 的作用和意义
@wraps(func) 是 Python 标准库 functools 模块中的一个装饰器，它的主要作用是保留被装饰函数的元数据。

为什么需要 @wraps
当使用装饰器包装一个函数时,实际上创建了一个新的函数（通常是装饰器内部的 wrapper 函数）。
这会导致原始函数的一些重要元信息丢失，例如:
    函数名称 (__name__)
    文档字符串 (__doc__)
    注解 (__annotations__)
    模块名 (__module__)
    其他属性
@wraps(func) 通过将原始函数的这些元数据复制到包装函数中来解决这个问题。
"""

# 示例对比
# 不使用 @wraps
def my_decorator(func):
    def wrapper(*args, **kwargs):
        """包装函数的文档字符串"""
        print("不使用@wraps 函数被调用")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example_function():
    """这是原始函数的文档字符串"""
    print("原始函数执行")

# 测试
print("函数名:", example_function.__name__)  # 输出: wrapper
print("文档字符串:", example_function.__doc__)  # 输出: 包装函数的文档字符串


# 使用 @wraps
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """包装函数的文档字符串"""
        print("使用@wraps 函数被调用")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example_function():
    """这是原始函数的文档字符串"""
    print("原始函数执行")

# 测试
print("函数名:", example_function.__name__)  # 输出: example_function
print("文档字符串:", example_function.__doc__)  # 输出: 这是原始函数的文档字符串