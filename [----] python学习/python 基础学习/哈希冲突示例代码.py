

class BadHash:
    """这是一个总是返回相同哈希值的类，用于演示哈希冲突"""

    def __init__(self, value):
        self.value = value

    def __hash__(self):
        # 故意返回相同的哈希值来制造冲突
        return 1

    def __eq__(self, other):
        if isinstance(other, BadHash):
            return self.value == other.value
        return False

    def __repr__(self):
        return f"BadHash({self.value})"


# 创建多个具有相同哈希值的对象
obj1 = BadHash("apple")
obj2 = BadHash("banana")
obj3 = BadHash("cherry")

print(f"obj1 的哈希值: {hash(obj1)}")
print(f"obj2 的哈希值: {hash(obj2)}")
print(f"obj3 的哈希值: {hash(obj3)}")

# 创建一个字典并添加这些键值对
my_dict = {}
my_dict[obj1] = "Fruit 1"
my_dict[obj2] = "Fruit 2"
my_dict[obj3] = "Fruit 3"

print("\n字典内容:")
for key, value in my_dict.items():
    print(f"{key}: {value}")

# 测试检索值
print(f"\n获取 obj1 的值: {my_dict[obj1]}")
print(f"获取 obj2 的值: {my_dict[obj2]}")
print(f"获取 obj3 的值: {my_dict[obj3]}")

# 展示字典内部结构信息
print(f"\n字典大小: {len(my_dict)}")