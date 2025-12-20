

# 虽然 abc 模块可以做到,但用元类可以实现更复杂的验证逻辑.
# 例如,检查子类是否实现了特定前缀或后缀的方法.
class InterfaceMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        # 创建类之前，检查其命名空间中是否有 'execute' 方法
        if 'execute' not in namespace:
            raise TypeError(f"Class '{name}' must define an 'execute' method.")
        return super().__new__(mcls, name, bases, namespace, **kwargs)

class Task(metaclass=InterfaceMeta):
    pass

# 这个会报错：TypeError: Class 'MyTask' must define an 'execute' method.
class MyTask(Task):
    def do_something(self):
        pass

# 这个能正常创建
class MyValidTask(Task):
    def execute(self):
        print("Executing task")


