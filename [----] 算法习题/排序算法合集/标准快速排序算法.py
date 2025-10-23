

# AI给出的标准的快速排序算法
def quick_sort_standard(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        print(f"\n arr: {arr}")
        quick_sort_standard(arr, low, pivot_index - 1)
        quick_sort_standard(arr, pivot_index + 1, high)

def partition(arr, low, high):
    pivot = arr[high]  # 选择最后一个元素作为基准
    i = low - 1
    # 小的放左边
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            print(f"i: {i}, j:{j}, arr: {arr}")
            arr[i], arr[j] = arr[j], arr[i]
            print(f"after switch arr: {arr}")
    # 大的放右边
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    print(f"after right switch arr: {arr}")

    # 返回大于的第一个坐标
    return i + 1

# 使用示例
arr = [1,2,6,8,6,2,9,10,8,8,2,4,3]
quick_sort_standard(arr, 0, len(arr)-1)
print(arr)

