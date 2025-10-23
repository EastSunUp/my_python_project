
def my_function():
    # 方法1: 使用 __name__
    print(f"函数名: {my_function.__name__}")

    # 方法2: 使用 sys._getframe()
    import sys
    current_function_name = sys._getframe().f_code.co_name
    print(f"当前函数名: {current_function_name}")

    # 方法3: 使用 inspect 模块
    import inspect
    current_function_name = inspect.currentframe().f_code.co_name
    print(f"当前函数名: {current_function_name}")

my_function()


