

# 在 Python 中,find() 是字符串(str)对象的内置方法,用于查找子字符串首次出现的索引位置.
# 如果未找到,则返回 -1.
# 以下是详细说明:

'''
    语法:
    str.find(sub[, start[, end]])

    sub:    要搜索的子字符串（必需）
    start:  搜索的起始索引（可选，默认为 0）
    end:    搜索的结束索引（可选，默认为字符串末尾）
    返回值:  子串首次出现的索引（int），未找到时返回 -1

    find()与index的区别:
    方法	        找到子串	   未找到子串
    find()	    返回索引	   返回 -1
    index()	    返回索引	   抛出异常 ValueError
    推荐使用      find()    避免异常处理。

    总结
    要点	        说明
    核心功能	    返回子串首次出现的索引
    未找到返回值	-1（安全无异常）
    大小写敏感	是
    搜索范围	    [start, end)（左闭右开）
    替代方法	    index()（未找到时抛异常）
    掌握         find() 方法能高效处理字符串搜索任务，建议优先使用它替代 index() 以避免异常中断程序。
'''

# 特性详情
text = "Hello World"
print(text.find("world"))  # 输出: -1 (大小写不匹配)
print(text.find("World"))  # 输出: 6

# 指定搜索范围（start 和 end）
text = "apple banana apple"
# 从索引 6 开始搜索
print(text.find("apple", 6))  # 输出: 13（第二个"apple"的位置）
# 在 [0, 12] 范围内搜索
print(text.find("apple", 0, 12))  # 输出: 0（第一个"apple"）

# 未找到返回 -1
text = "Python"
print(text.find("java"))  # 输出: -1

# 空字串的特殊情况
text = "Python"
print(text.find(""))  # 输出: 0（空串被视为存在于任何位置）

# 实际示例
s = "Learn Python programming"
# 基本查找
print(s.find("Python"))   # 输出: 6
# 指定范围查找
print(s.find("Python", 7, 20))  # 输出: -1（不在该范围内）
# 链式调用 (检查是否存在)
if s.find("Java") != -1:
    print("Found")
else:
    print("Not found")  # 输出: Not found

# --------------------------常见应用场景--------------------------------------------------
# 检查字串是否存在
if text.find("key") >= 0:
    print("Substring exists")
# 提取子串位置
start_index = text.find("[start]")
end_index = text.find("[end]")

# 注意事项
# 若需忽略大小写搜索,先将字符串转为统一大小写：
text_lower = text.lower()
print(text_lower.find("KEY".lower()))

# 若需查找所有出现位置,结合循环:
text = "ababab"
start = 0
while True:
    pos = text.find("ab", start)
    if pos == -1: break
    print(f"Found at index {pos}")
    start = pos + 1  # 继续向后搜索
# 输出: 0, 2, 4
