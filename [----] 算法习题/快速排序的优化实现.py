import random
from typing import List


def quick_sort_optimized(arr: List[int]) -> List[int]:
    """
    使用快速排序算法对整数列表进行排序（升序）。
    实现了原地排序和随机化pivot选择进行优化。

    Args:
        arr (List[int]): 待排序的整数列表

    Returns:
        List[int]: 排序后的列表
    """

    def _quick_sort(_arr: List[int], low: int, high: int) -> None:
        """快速排序的递归辅助函数"""
        # 小数组使用插入排序优化
        if high - low + 1 < 10:
            insertion_sort(_arr, low, high)
            return

        if low < high:
            # 分区操作,获取pivot的最终位置
            pi = partition(_arr, low, high)
            # 递归排序pivot左右两边的元素
            _quick_sort(_arr, low, pi - 1)
            _quick_sort(_arr, pi + 1, high)

    def partition(_arr: List[int], low: int, high: int) -> int:
        """
        分区操作：选择pivot，重新排列数组，使得小于pivot的元素在其左侧，
        大于pivot的元素在其右侧。

        Args:
            _arr: 待分区数组
            low: 分区起始索引
            high: 分区结束索引

        Returns:
            int: pivot的最终位置索引
        """
        # 随机选择pivot,避免最坏情况
        pivot_idx = random.randint(low, high)
        _arr[pivot_idx], _arr[high] = _arr[high], _arr[pivot_idx]
        pivot = _arr[high]

        i = low - 1  # 较小元素的索引

        for j in range(low, high):
            if _arr[j] <= pivot:
                i += 1
                _arr[i], _arr[j] = _arr[j], _arr[i]

        _arr[i + 1], _arr[high] = _arr[high], _arr[i + 1]
        return i + 1

    def insertion_sort(_arr: List[int], low: int, high: int) -> None:
        """对小数组使用插入排序进行优化"""
        for i in range(low + 1, high + 1):
            key = _arr[i]
            j = i - 1
            while j >= low and _arr[j] > key:
                _arr[j + 1] = _arr[j]
                j -= 1
            _arr[j + 1] = key

    # 创建原数组的拷贝,不改变原数组
    sorted_arr = arr.copy()
    _quick_sort(sorted_arr, 0, len(sorted_arr) - 1)
    return sorted_arr


def test_quick_sort():
    """测试快速排序的功能和性能"""
    # 测试1: 普通数组
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    expected = sorted(test_arr)
    result = quick_sort_optimized(test_arr)
    assert result == expected, f"测试1失败: 期望{expected}, 得到{result}"
    print("测试1通过!")

    # 测试2: 空数组
    assert quick_sort_optimized([]) == [], "测试2失败"
    print("测试2通过!")

    # 测试3: 已排序数组
    sorted_test = [1, 2, 3, 4, 5]
    assert quick_sort_optimized(sorted_test) == sorted_test, "测试3失败"
    print("测试3通过!")

    # 测试4: 大量重复元素
    duplicate_test = [5, 2, 8, 5, 9, 1, 5, 3]
    expected_dup = sorted(duplicate_test)
    result_dup = quick_sort_optimized(duplicate_test)
    assert result_dup == expected_dup, f"测试4失败: 期望{expected_dup}, 得到{result_dup}"
    print("测试4通过!")

    # 测试5: 随机大数组
    large_arr = [random.randint(1, 10000) for _ in range(1000)]
    expected_large = sorted(large_arr)
    result_large = quick_sort_optimized(large_arr)
    assert result_large == expected_large, "测试5失败: 大数组排序错误"
    print("测试5通过!")
    print("所有测试通过！")


if __name__ == "__main__":
    test_quick_sort()
