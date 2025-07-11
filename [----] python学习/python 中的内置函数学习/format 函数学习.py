

# 相同类型的用法还有f{*******} 内容...

# 基础用法
# 位置参数
print("{} {}".format("Hello", "World"))  # 输出: Hello World
# 索引参数
print("{1} {0}".format("World", "Hello"))  # 输出: Hello World
# 关键字参数
print("{name} is {age} years old".format(name="Alice", age=30))
# 输出: Alice is 30 years old

# 类型转换
def type_convert():
    # !s - 调用 str()
    print("{!s}".format(50))  # '50'
    # !r - 调用 repr()
    print("{!r}".format("text"))  # "'text'"
    # !a - 调用 ascii()
    print("{!a}".format("é"))  # "'\\xe9'"

# 对齐与填充
def align_and_fill(self):
    # 左对齐 (宽度10)
    print("{:<10}".format("left"))      # 'left      '
    # 右对齐 (宽度10)
    print("{:>10}".format("right"))     # '     right'
    # 居中对齐 (宽度10)
    print("{:^10}".format("center"))    # '  center  '
    # 自定义填充字符
    print("{:*^10}".format("star"))     # '***star***'

# 数字格式化
def digital_formatting(self):
    # 整数
    print("{:d}".format(42))            # '42'
    # 二进制 (带前缀)
    print("{:#b}".format(10))           # '0b1010'
    # 十六进制 (大写)
    print("{:X}".format(255))           # 'FF'
    # 浮点数 (保留2位小数)
    print("{:.2f}".format(3.14159))     # '3.14'
    # 百分比格式
    print("{:.1%}".format(0.85))        # '85.0%'
    # 科学计数法
    print("{:.2e}".format(1234567))     # '1.23e+06'

# 特殊格式
def special_format():
    # 千位分隔符
    print("{:,}".format(1000000))       # '1,000,000'
    # 符号显示 (+/-)
    print("{:+d}".format(42))           # '+42'
    print("{:-d}".format(-42))          # '-42'
    print("{: d}".format(42))           # ' 42' (正数前加空格)
    # 固定宽度带前导零
    print("{:06d}".format(42))          # '000042'
    # 组合使用
    print("{:*>+,10.2f}".format(1234.567))  # '+1,234.57'
    # 解释: 右对齐(*) 宽度10 带符号 千位分隔 保留2位小数

# -------------------------------------format的高级用法---------------------------------------------------
# 用法一、嵌套字段
# 动态设置精度
value = 3.1415926
print("{:.{prec}f}".format(value, prec=3))  # '3.142'
# 字典格式化
person = {'name': 'Bob', 'age': 25}
print("{p[name]}'s age: {p[age]}".format(p=person))  # "Bob's age: 25"

# 用法二、(对象格式化)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __format__(self, spec):
        if spec == 'polar':
            import math
            r = math.sqrt(self.x ** 2 + self.y ** 2)
            theta = math.atan2(self.y, self.x)
            return f"({r:.2f}, {theta:.2f}rad)"
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print("Cartesian: {}".format(p))  # Cartesian: (3, 4)
print("Polar: {:polar}".format(p))  # Polar: (5.00, 0.93rad)

# 用法三、(日期格式化)
from datetime import datetime
now = datetime.now()
print("{:%Y-%m-%d %H:%M:%S}".format(now))  # 2025-07-06 10:30:00

# 对比 % 格式化
# 旧式 % 格式化
print("Name: %s, Age: %d" % ("Alice", 30))
# 新式 format()
print("Name: {}, Age: {}".format("Alice", 30))


# -----------------------------------其它的一些格式化实践---------------------------------------------------
#  f-string
name = "Alice"
print(f"Hello {name}")  # 直接嵌入变量
# 需要动态格式化时使用 format():
template = "Value: {:{width}.{prec}f}"
print(template.format(3.14159, width=10, prec=3))  # 'Value: 3.142'
# 复杂格式使用显式参数名提高可读性
"{name} scored {score:.1%} on {test}".format(
    name="Bob",
    score=0.875,
    test="Math"
)




