

from functools import wraps

def repeat(num_times):
    """重复执行函数的装饰器"""
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
                print(f"result: {result}")
            return result
        return wrapper
    return decorator_repeat

# 使用带参数的装饰器
@repeat(num_times=3)
def greet(name):
    print(f"Hello, {name}!")
    return f"{name}"

greet("Alice")