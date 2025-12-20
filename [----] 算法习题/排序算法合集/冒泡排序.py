
# 本文件使用python编程语言实现冒泡排序算法!

arr = [1, 2, 6, 8, 6, 2, 9, 10, 8, 8, 2, 4, 3]

def buble_arrange(data):
    # 输入的数据类型必须是列表或者元组.
    if not isinstance(data, (list,tuple)):
        print("error! please input correct data type: list or tuple !")
        return
    # 冒泡排序算法如下!
    for _ in range(len(data)-1):
        for i in range(len(data)-1):
            if data[i] > data[i+1]:
                temp = data[i+1]
                data[i+1] = data[i]
                data[i] = temp
    return data

# 运行冒泡排序函数!
res = buble_arrange(data = arr)

print(f"res: {res}")

