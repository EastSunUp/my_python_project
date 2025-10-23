


class CountCalls:
    """记录函数调用次数的类装饰器"""

    def __init__(self, func):
        self.func = func
        class_fun(fun_name=func.__name__)   # 打印调用函数的名称
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"调用次数: {self.num_calls}")
        self.func(*args, **kwargs)
        return # self.func(*args, **kwargs)


def class_fun(fun_name):
    print(f"调用函数 {fun_name}!\n")

# 使用类装饰器,
# 类装饰器的意思是当运行这个函数时,会调用这个函数所对应的装饰器的类,
# 然后把这个函数作为参数传输给这个类,并运行对应的类中的__call__函数(首先会运行__init__函数)
@CountCalls
def say_hello():
    print("Hello!")

say_hello()
say_hello()
say_hello()

