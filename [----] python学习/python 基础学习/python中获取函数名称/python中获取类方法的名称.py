

class MyClass:
    def my_method(self):
        # 获取当前方法名
        import inspect
        method_name = inspect.currentframe().f_code.co_name
        print(f"方法名: {method_name}")

        # 或者使用 self 和 __class__
        print(f"类名: {self.__class__.__name__}")
        print(f"完整方法名: {self.__class__.__name__}.{method_name}")


obj = MyClass()
obj.my_method()

