
"""
题目描述
    一个荒岛上有若干人，岛上只有一条路通往岛屿两端的港口，大家需要逃往两端的港口才可逃生。
    假定每个人移动的速度一样，且只可选择向左或向右逃生。
    若两个人相遇，则进行决斗，战斗力强的能够活下来，并损失掉与对方相同的战斗力；若战斗力相同，则两人同归于尽。
输入描述
    给定一行非 0 整数数组，元素个数不超过30000；
    正负表示逃生方向（正表示向右逃生，负表示向左逃生），绝对值表示战斗力，越左边的数字表示里左边港口越近，逃生方向相同的人永远不会发生决斗。
输出描述
    能够逃生的人总数,没有人逃生输出0,输入异常时输出-1。

示例1
    输入
        5 10 8 -8 -5
    输出
        2
说明
    第3个人和第4个人同归于尽,第2个人杀死第5个人并剩余5战斗力，第1个人没有遇到敌人。
"""

import ast

user_input=input("请输入逃生序列!\n")
if user_input is not isinstance(user_input,list):
    print(f"user_input:输入的逃生序列应该为列表形式!\n")
# user_list = user_input.split()
try:
    user_list = ast.literal_eval(user_input)
    if not isinstance(user_list, list):
        print("user_list is not list !")
        user_list = [user_list]
except (SyntaxError, ValueError):
    user_list = list(user_input)    # [user_input]

'''
'''
pop_list=[]*len(user_list)
for i, val in enumerate(user_list):
    # print(f"user_list[{i}]:{user_list[i]}")
    if val is not isinstance(val, int):
        # print(f"pop user_list[{i}]:{user_list[i]}")
        pop_list.append(i)
print(f"pop_list:{pop_list}")
# user_list.pop(i)   # 或: del user_input[i]
# user_input.remove(f"user_input[{i}]")

# user_list.pop(2)    # 删除第3个元素
print(f"user_input:{user_list[2]}")    # [2]


# 逃生算法处理核心计算函数
i = 0
user_list=[1,2,3,5,6,-5,6]
while i < range(len(user_list)):
    if user_list[i] > 0:
        i = i+1
        continue
    else:
        # 需要排除第一个元素小于0的情况.
        if i-1 >=0:
            if user_list[i-1]>0:
                user_list[i - 1] = user_list[i - 1] + user_list[i]
                user_list.pop(i)
                if user_list[i-1] < 0:
                    i=i-1
                    continue
                elif user_list[i-1] > 0:
                    continue
                else:
                    # 等于0时,两个元素都要删掉
                    user_list.pop(i-1)
                    continue
            else:
                i = i + 1
                continue
        else:
            i = i + 1
            continue

