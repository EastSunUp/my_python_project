
# 使用sys.argv实现一个计算器
# calculator.py
import sys

if len(sys.argv) != 4:
    print("用法: python calculator.py <数字1> <操作符> <数字2>")
    print("示例: python calculator.py 5 + 3")
    sys.exit(1)

num1 = float(sys.argv[1])
operator = sys.argv[2]
num2 = float(sys.argv[3])

if operator == '+':
    result = num1 + num2
elif operator == '-':
    result = num1 - num2
elif operator == '*':
    result = num1 * num2
elif operator == '/':
    result = num1 / num2
else:
    print("不支持的运算符")
    sys.exit(1)

print(f"{num1} {operator} {num2} = {result}")


