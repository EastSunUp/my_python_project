

# 创建一个基类,让所有继承它的子类都自动被注册到一个中央仓库中,便于后续查找和使用,非常适合实现插件架构.

class PluginMeta(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace, **kwargs)
        # 跳过对基类 Plugin 本身的注册
        if not hasattr(cls, 'plugins'):
            cls.plugins = []  # 在基类上创建注册列表
        else:
            cls.plugins.append(cls)  # 将子类注册到列表中

class Plugin(metaclass=PluginMeta):
    pass

class MyPlugin1(Plugin):
    def run(self):
        print("Plugin 1 running")

class MyPlugin2(Plugin):
    def run(self):
        print("Plugin 2 running")

# 无需手动注册,所有插件已自动在 Plugin.plugins 中
for plugin_class in Plugin.plugins:
    plugin_instance = plugin_class()
    plugin_instance.run()
# 输出:
# Plugin 1 running
# Plugin 2 running