

def remove_twos(lst):
    """
    删除列表中的所有数字2

    参数:
        lst: 输入列表

    返回:
        删除所有数字2后的新列表
    """
    # 使用列表推导式过滤掉所有等于2的元素
    return [item for item in lst if item != 2]


# 测试
test_list = [1, 2, 3, 2, 4, 2, 5, 2]
result = remove_twos(test_list)
print(f"原始列表: {test_list}")
print(f"删除2后: {result}")
# 输出: [1, 3, 4, 5]


# 以下为错误代码,对于[2,2,2,2]等的列表情况会不适用
# test_list = [1, 2, 2, 3]
# for index, val in enumerate(test_list):
#     print(f"index={index}, val={val}, 当前列表={test_list}")
#     if val == 2:
#         del test_list[index]



