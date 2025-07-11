
'''
    在 Python 中,strip() 是字符串（str）类型的内置方法,
    用于移除字符串开头和结尾的指定字符（默认为空白字符）.
    以下是详细说明：
'''
import os
import time

'''
    # 基本语法
    str.strip([chars])
    chars(可选参数): 指定要移除的字符集合 (字符串形式).
    如果省略或为 None,则默认移除空白字符 (空格、制表符 \t、换行符 \n 等).
    返回值: 返回移除两端指定字符后的新字符串 (原字符串不变).
    
    总结
    方法	            作用	                    示例
    str.strip()	    移除两端空白/指定字符	    " text ".strip() → "text"
    str.lstrip()	仅移除开头空白/指定字符	    "xxtext".lstrip('x') → "text"
    str.rstrip()	仅移除结尾空白/指定字符	    "textxx".rstrip('x') → "text"

'''
# 关键特性
# 默认行为（不传参）：
# 移除字符串开头和结尾的空白字符（包括： 、\t、\n、\r、\v、\f）。
# 不影响字符串中间的字符。
s = "  \t Hello, World! \n "
print(s.strip())  # 输出: "Hello, World!"

# 指定字符集合:
# 移除开头/结尾中所有出现在 chars 中的字符(按字符逐个匹配，非子字符串).
s = "**Hello, World!**"
print(s.strip('*!'))  # 输出: "Hello, World"

# 移除规则:
# 从两端向中间扫描,遇到第一个不在 chars 中的字符时停止移除.
s = "123abc321"
print(s.strip('123'))  # 输出: "abc"（开头"123"和结尾"321"被移除）

# 大小写敏感:
# 严格匹配字符大小写.
s = "ABCabcCBA"
print(s.strip('ac'))  # 输出: "ABCabcCB" (只移除小写 'a' 和 'c')


# 相关方法
# lstrip([chars])：仅移除开头的指定字符。
# rstrip([chars])：仅移除结尾的指定字符。
s = "xxHello, World!xx"
print(s.lstrip('x'))  # 输出: "Hello, World!xx"
print(s.rstrip('x'))  # 输出: "xxHello, World!"

# 清理用户输入
user_input = "  user@example.com  "
email = user_input.strip()  # 移除多余空格

# 处理文件内容
with open("data.txt") as f:
    lines = [line.strip() for line in f]  # 移除每行首尾空白

# 移除特定字符
s = "$$$Price: 100$$$"
clean = s.strip('$')  # 输出: "Price: 100"

# 处理标点符号
s = "【重要通知】"
print(s.strip('【】'))  # 输出: "重要通知"

# 注意事项:
# 不修改原字符串: 字符串在Python中不可变,strip() 返回新字符串.
# 中间字符不受影响:
s = "aabbaabbaa"
print(s.strip('a'))  # 输出: "bbaabb" (中间 'a' 保留)
# chars 是字符集合: 非子字符串匹配.
s = "mississippi"
print(s.strip('ips'))  # 输出: "mississ" (移除开头/结尾的 'i','p','s')







