
from functools import wraps
import time

def debug_decorator(func):
    """调试装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值: {result}")
        return result
    return wrapper

# 计时装饰器
def timer_decorator(func):
    @wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

# 同时使用多个装饰器
@debug_decorator
@timer_decorator
def factorial(n):
    """计算阶乘"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# 测试
result = factorial(5)
print(f"5的阶乘是: {result}")

