
'''
    map() 是 Python 的内置高阶函数，用于对可迭代对象（如列表、元组等）中的每个元素应用指定函数，
    并返回一个迭代器（Python 3 中）。其核心功能是批量处理数据，避免显式循环。

    # 基本语法
    map(function, iterable, ...)

    function: 应用的函数（可以是内置函数、lambda 函数、自定义函数）。
    iterable: 一个或多个可迭代对象（如列表、元组）。
    返回值: Python 3 中返回 map 迭代器对象（需用 list() 等转换为具体序列）。
'''
'''
    总结
    特性	                说明
    核心作用	            批量处理可迭代对象的元素
    输入	                函数 + 一个或多个可迭代对象
    输出（Python 3）	    迭代器 (需用 list()、tuple() 等转换)
    优势	                函数式编程风格,避免显式循环
    适用场景	            数据转换、数学运算、类型转换等批量操作
    替代方案	            列表推导式 (可读性更好，支持复杂逻辑)

'''
# -------------------------使用示例--------------------------------------------------
# 单个可迭代对象
# 将列表元素转为字符串
nums = [1, 2, 3, 4]
result = map(str, nums)
print(list(result))  # 输出: ['1', '2', '3', '4']

# 使用 lambda 计算平方
squares = map(lambda x: x**2, [1, 2, 3])
print(list(squares))  # 输出: [1, 4, 9]


# 多个可迭代对象（并行处理）
# 两个列表相加
a = [1, 2, 3]
b = [4, 5, 6]
sum_list = map(lambda x, y: x + y, a, b)
print(list(sum_list))  # 输出: [5, 7, 9]

# 长度不一致时，以最短的为准
c = [10, 20]
result = map(lambda x, y: x * y, a, c)
print(list(result))  # 输出: [10, 40]（只处理前两个元素）


# 使用自定义函数
def to_upper(s):
    return s.upper()

words = ["hello", "world"]
upper_words = map(to_upper, words)
print(list(upper_words))  # 输出: ['HELLO', 'WORLD']

'''
    与列表推导式的对比
    map() 的功能常可用列表推导式实现,但各有优劣:
        map() 优势: 函数式风格, 适合已定义函数或简单 lambda 操作.
        列表推导式优势: 可读性更高, 支持条件过滤 (如 [x*2 for x in lst if x>0]).
'''
# 使用 map()
map_result = map(lambda x: x*2, [1, 2, 3])

# 使用列表推导式
list_result = [x*2 for x in [1, 2, 3]]

# ---------------------注意事项------------------------------------------------
# 惰性求值（Python 3）:
m = map(str, [1, 2, 3])  # 不立即计算
print(next(m))  # '1'（按需生成）
print(list(m))  # ['2', '3']（剩余元素）

# 多参数函数:
# 需确保函数参数数量与 iterable 数量一致
def add(x, y, z):
    return x + y + z

result = map(add, [1, 2], [3, 4], [5, 6])
print(list(result))  # [9, 12]

# 与 filter() 结合:
# 先过滤偶数，再平方
nums = [1, 2, 3, 4, 5]
result = map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums))
print(list(result))  # [4, 16]

