
# 本代码仅作示例使用!
# 高水平示例
from collections import Counter

arr=[1,1,2,2,2,5,6,5,6,9]

# 低水平示例
def calc(arr):
    r = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j and arr[i] == arr[j]:
                print(f"arr[{i}]:{arr[i]} == arr[{j}]:{arr[j]}")
                r += 1
    return r  # 时间复杂度O(n²)


def calc_2(arr):
    count = Counter(arr)
    # count.values()函数的功能是统计各元素在数组中出现的次数
    # for val in count.values():
    #     val=val * (val - 1)
    #     print(val)
    return sum(v*(v-1) for v in count.values())  # 时间复杂度O(n)

# 哈希思想的精髓!
def calc_3(arr):
    count={}
    sum = 0
    for i in range(len(arr)):
        count[f'{arr[i]}'] = 0  # 使用这种方法给字典添加新值、新键
    for i in range(len(arr)):
        count[f'{arr[i]}'] = count[f'{arr[i]}']+1
        # count[arr[i]]=count[arr[i]]+1
    for key in count:
        sum = sum + count[key]*(count[key]-1)
    print(f"sum:{sum}")

# 这种方法有对剩余内存不必要的扫描,推荐方法calc_3()
def calc_4(arr):
    max_value = arr[0]  # 已知的最大索引值
    for i in range(len(arr)):
        if max_value < arr[i]:
            max_value = arr[i]
    # 创建初始化为0的列表（相当于malloc+初始化）
    count = [0] * (max_value + 1)  # +1 因为索引从0开始
    for i in range(len(arr)):
        count[arr[i]] = count[arr[i]]+1
    sum_val = sum(val*(val-1) for val in count)
    print(f"sum_val:{sum_val}")


print(calc(arr))
print(calc_2(arr))  # 高水平代码
calc_3(arr)
calc_4(arr)
