

# ORM（对象关系映射）框架
# 这是元类最著名的应用之一.
# 例如,Django ORM 和 SQLAlchemy 的核心都大量使用了元类.
# 元类可以读取你定义的类属性（如 name = Column(String)）,并根据这些信息动态地构建出复杂的 SQL 查询语句和表结构.

# 一个极度简化的 ORM 示例
class Field:
    def __init__(self, field_type):
        self.field_type = field_type

class ModelMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        # 收集所有 Field 实例
        fields = {}
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value

        # 将这些信息存储在一个特殊的属性（如 _fields）中
        namespace['_fields'] = fields
        return super().__new__(mcls, name, bases, namespace, **kwargs)

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    name = Field(str)
    age = Field(int)

# visa()

# 元类自动为我们处理了类定义
print(User._fields) # 输出: {'name': <__main__.Field object>, 'age': <__main__.Field object>}
# 之后,Model 类就可以使用这些 _fields 信息来生成 SQL 语句了，比如：
# INSERT INTO users (name, age) VALUES (?, ?)

