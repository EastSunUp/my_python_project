
'''
    在 Python 中, .join() 是字符串（str）类型的一个方法，
    用于将序列中的多个字符串元素连接成一个新的字符串，
    并通过指定的字符串作为分隔符。
    它是处理字符串拼接的高效方式。

    基本语法:
        "分隔符".join(可迭代对象)
        分隔符：任意字符串，用于插入到每个元素之间
        可迭代对象：包含字符串元素的序列（如列表、元组、集合、字符串本身等）

    总结
    场景	            示例	                        结果
    基础拼接	        "".join(["a","b"])	        "ab"
    添加分隔符	    "-".join(["a","b"])	        "a-b"
    处理非字符串元素	"".join(map(str, [1,2]))	"12"
    连接路径片段	    "/".join(["dir","sub"])	    "dir/sub"
    高效拼接大量字符串	"".join(big_list)	        避免内存碎片

    # join, 字符串拼接函数, 字符替代 (为什么不用+号做字符串拼接, 效率与内存问题)
'''

# 基本连接（无分隔符）
words = ["Hello", "World"]
result = "".join(words)  # 直接拼接
print(result)  # 输出: HelloWorld

# 添加分隔符
fruits = ["apple", "banana", "cherry"]
result = ", ".join(fruits)  # 用逗号+空格分隔
print(result)  # 输出: apple, banana, cherry

# 特殊分隔符
chars = ["A", "B", "C"]
result = " → ".join(chars)  # 使用箭头分隔
print(result)  # 输出: A → B → C

# 连接其它可迭代对象(元组)
path = ("usr", "local", "bin")
result = "/".join(path)
print(result)  # 输出: usr/local/bin

# 连接其它可迭代对象(字符串本身) (拆分为单个字符连接)
word = "Python"
result = "-".join(word)
print(result)  # 输出: P-y-t-h-o-n

# 集合
unique_chars = {"a", "b", "c"}
result = "|".join(unique_chars)  # 可能输出: a|c|b (顺序随机)
print(result)

'''
    注意事项:
        1.元素必须为字符串类型
            如果序列中包含非字符串元素（如整数、列表）,会触发 TypeError:
                numbers = [1, 2, 3]
                " ".join(numbers)  # ❌ TypeError!
            解决方案: 先转换为字符串:
                " ".join(str(x) for x in numbers)  # ✅ 输出: "1 2 3"
        2.空序列处理
            空列表返回空字符串:
                "X".join([])  # 输出: ""
            单元素列表返回元素本身 (不加分隔符):
                "~".join(["Alone"])  # 输出: "Alone"  
'''

'''
性能优势:
    相比于循环中使用 + 拼接字符串,.join() 效率更高.
    因为:
        + 每次拼接会创建新字符串对象，内存开销大
        .join() 预先计算总长度，一次性分配内存
'''
# 低效方式（避免在大数据量时使用）
s = ""
for char in ["a", "b", "c"]:
    s += char  # 每次循环创建新字符串
print(s)
# 高效方式
s = "".join(["a", "b", "c"])
print(s)

# -------------------------进阶用法----------------------------------
# 连接文件路径(跨平台安全)
import os
parts = ["home", "user", "docs"]
path = os.path.join(*parts)  # 推荐方式（自动处理路径分隔符）
# 但也可用字符串拼接： "/".join(parts)

# 生成特定格式文本
data = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
for row in data:
    print("| " + " | ".join(row) + " |")
# 输出表格：
# | Name | Age |
# | Alice | 30 |
# | Bob | 25 |

