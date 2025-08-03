
"""
题目描述
    存在一种虚拟IPv4地址，由4小节组成，每节的范围为0~255，以#号间隔，虚拟IPv4地址可以转换为一个32位的整数，例如：
        128#0#255#255，转换为32位整数的结果为2147549183（0x8000FFFF）
        1#0#0#0，转换为32位整数的结果为16777216（0x01000000）
    现以字符串形式给出一个虚拟IPv4地址，限制第1小节的范围为1128，
    即每一节范围分别为(1 128)#(0 255)#(0 255)#(0~255)，要求每个IPv4地址只能对应到唯一的整数上。
    如果是非法IPv4，返回invalid IP

输入描述
    输入一行，虚拟IPv4地址格式字符串
输出描述
    输出一行，按照要求输出整型或者特定字符
示例1
    输入
        100#101#1#5
    输出
        1684340997
示例2
    输入
        1#2#3
    输出
        invalid IP
    解释:
        因为给定的虚拟IP的长度小于4,这里只有3位

解题思路
虚拟IPv4地址由四个小节组成,每个小节用#号分隔。
在这个虚拟版本中用#替代。
每个小节代表一个整数，范围从0到255，但题目中特别指出第一小节的范围应为1到128。
地址的正确形式应该是四部分，例如 1#2#3#4。如果格式不正确或数值不在指定范围内，则视为非法IPv4，输出“invalid IP”。
"""
# 判断字符串是否为数字
def is_numeric(s):
    return s.isdigit()

# 获取输入的字符串
input_str = input()

# 将输入的字符串按照"#"分割成4个小节
ip_sections = input_str.split("#")

# 如果分割后的小节数量不等于4，则说明输入的IPv4地址格式不正确
if len(ip_sections) != 4:
    print("invalid IP")
else:
    valid = True
    # 遍历每个部分进行检查
    for section in ip_sections:
        if len(section) == 0 or not is_numeric(section):  # 检查是否为空或者是否每部分都是数字
            valid = False
            break
        if len(section) > 1 and section[0] == '0':  # 检查前导零的情况
            valid = False
            break

    if not valid:
        print("invalid IP")
    else:
        # 检查第一个小节的范围
        first_section = int(ip_sections[0])  # 将第一个小节转换为整数
        if first_section < 1 or first_section > 128:  # 如果第一个小节的值不在1~128的范围内
            print("invalid IP")
        else:
            # 检查其余3个小节的范围
            for i in range(1, 4):
                section_value = int(ip_sections[i])  # 将当前小节转换为整数
                if section_value < 0 or section_value > 255:  # 如果不在0~255范围内
                    print("invalid IP")
                    break
            else:
                # 计算最终的32位整数
                ip_value = 0
                for i in range(4):
                    ip_value = ip_value * 256 + int(ip_sections[i])  # 每个小节对应一个字节，计算最终的整数值
                print(ip_value)  # 输出最终的32位整数
