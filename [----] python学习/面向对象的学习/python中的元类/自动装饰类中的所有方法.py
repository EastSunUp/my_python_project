

# 自动装饰类中的所有方法（例如：日志、权限检查）
# 如果你想为某个类的所有方法自动添加一些通用功能（比如日志记录）
# 可以在元类中遍历类的命名空间,找到所有可调用对象（方法）并装饰它们.

def log_method(func):
    def wrapper(*args, **kwargs):
        print(f"Calling method: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class LoggingMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        # 遍历命名空间中的每个成员
        for attr_name, attr_value in namespace.items():
            # 如果成员是可调用的方法（且不是魔术方法），就装饰它
            if callable(attr_value) and not attr_name.startswith('__'):
                namespace[attr_name] = log_method(attr_value)
        return super().__new__(mcls, name, bases, namespace, **kwargs)

class MyClass(metaclass=LoggingMeta):
    def method1(self):
        print("inside method1")

    def method2(self):
        print("inside method2")

obj = MyClass()
obj.method1()
obj.method2()
# 输出:
# Calling method: method1
# inside method1
# Calling method: method2
# inside method2