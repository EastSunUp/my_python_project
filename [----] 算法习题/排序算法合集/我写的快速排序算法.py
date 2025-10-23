
'''
    快速排序的核心逻辑:
        大的排左边,小的排右边.
        迭代、递归!
'''

# from contextlib import nullcontext

# 请使用python实现快速排序算法!
arr = [1,2,6,8,6,2,9,10,8,8,2,4,3]
data_process = []

def quick_sort(data, index_a, index_b):
    temp_list = []
    # set_a = None # set_b = None
    set_a , set_b, ref_index, ref_val = index_a , index_b, None, data[index_b]
    print("\n")
    print(f"index_a:{index_a}, index_b:{index_b}")
    if set_a >= set_b or set_b <= set_a:
        print("set_a >= set_b or set_b <= set_a, return!")
        return

    # 小于参考值放左边
    for i in range(index_a, index_b+1):
        if data[i] <= ref_val:
            temp_list.append(data[i])
        print(f"i: {i}") # i最大遍历到 b-1处
    # 大于参考值放右边(这里存在开销浪费)
    for i in range(index_a, index_b+1):
        if data[i] > ref_val:
            temp_list.append(data[i])

    # 拷贝data数据!
    for k in range(index_a, index_b+1):
        print(f"遍历 k: {k}, len_arr:{len(arr)}")
        data_process[k] = temp_list[k - index_a]
    for k in range(index_a, index_b+1):    # k in range(len(data)):
        if data[k] == ref_val:
            ref_index = k

    print(f"arr: {data_process}")
    print(f"set_a:{set_a}, set_b: {set_b}, ref_index:{ref_index}")
    quick_sort(data=data_process, index_a=set_a, index_b=ref_index-1)
    quick_sort(data=data_process, index_a=ref_index+1, index_b=set_b)


data_process = arr.copy() # 拷贝目标数据用于排序
# 进行快速排序
quick_sort(data=data_process, index_a=0, index_b=12)
arr = data_process.copy()
data_process.clear() # 用完之后,清除用于排序的列表
print(f"arr:{arr}")


# 字符串拼接(列表、元组、字典, 及其常用方法)
# 多个字符串放在列表中, 找公有字符
# 元类做新类型的开发?

