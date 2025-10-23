

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"正在调用函数: {func.__name__}")
        print(f"函数文档: {func.__doc__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def say_hello(name):
    """向某人打招呼"""
    print(f"Hello, {name}!")

say_hello("Alice")

