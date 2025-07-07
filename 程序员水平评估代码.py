# 高水平示例
from collections import Counter

arr=[1,1,2,2,2,5,6,5,6,9]

# 低水平示例
def calc(arr):
    r = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j and arr[i] == arr[j]:
                r += 1
    return r  # 时间复杂度O(n²)


def calc_2(arr):
    count = Counter(arr)
    # for val in count.values():
    #     val=val * (val - 1)
    #     print(val)
    return sum(v*(v-1) for v in count.values())  # 时间复杂度O(n)


print(calc_2(arr))


